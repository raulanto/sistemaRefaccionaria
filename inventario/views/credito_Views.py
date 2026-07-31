from django.utils import timezone as django_timezone
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from inventario.models import ClienteCredito
from inventario.models.movimientoCredito_modelo import MovimientoCredito
from inventario.models.producto_modelo import Producto
from inventario.services.credito_service import CreditoService
from xhtml2pdf import pisa
from datetime import datetime
from django.db.models import ProtectedError



def buscar_clientes_credito_ajax(request):
    """Búsqueda AJAX de clientes de crédito, usada desde el punto de venta."""
    q = request.GET.get('q', '').strip()
    clientes = ClienteCredito.objects.filter(activo=True)
    if q:
        clientes = clientes.filter(Q(nombre__icontains=q) | Q(contacto__icontains=q))
    clientes = clientes.order_by('nombre')[:20]

    data = [{'id': c.id, 'nombre': c.nombre, 'contacto': c.contacto} for c in clientes]
    return JsonResponse({'clientes': data})


class ClientesCreditoListView(View):
    """Lista de clientes con su saldo actual."""
    def get(self, request):
        clientes = ClienteCredito.objects.filter(activo=True)
        clientes_con_saldo = [
            {'cliente': c, 'saldo': CreditoService.calcular_saldo(c)}
            for c in clientes
        ]
        total_general = sum(item['saldo'] for item in clientes_con_saldo)

        return render(request, 'credito/cliente_lista.html', {
            'titulo': 'Clientes de Crédito',
            'clientes_con_saldo': clientes_con_saldo,
            'total_general': total_general,
        })

    def post(self, request):
        """Crea o edita un cliente, según si llega cliente_id."""
        cliente_id = request.POST.get('cliente_id')
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono', '')
        notas = request.POST.get('notas', '')

        if not nombre:
            return redirect('inventario:clientes_credito_lista')

        if cliente_id:
            # Modo EDITAR
            cliente = get_object_or_404(ClienteCredito, id=cliente_id)
            cliente.nombre = nombre
            cliente.telefono = telefono
            cliente.notas = notas
            cliente.save()
        else:
            # Modo CREAR
            ClienteCredito.objects.create(
                nombre=nombre, telefono=telefono, notas=notas
            )

        return redirect('inventario:clientes_credito_lista')
    
class ClienteCreditoCrearView(View):
    """Página completa (sin modal) para dar de alta un cliente de crédito."""
    def get(self, request):
        return render(request, 'credito/cliente_crear.html', {
            'titulo': 'Nuevo Cliente de Crédito',
        })

    def post(self, request):
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono', '')
        contacto = request.POST.get('contacto', '')
        notas = request.POST.get('notas', '')

        if nombre:
            ClienteCredito.objects.create(
                nombre=nombre, telefono=telefono, contacto=contacto, notas=notas
            )
        return redirect('inventario:clientes_credito_lista')


def registrar_movimiento_credito(request, cliente_id):
    if request.method != "POST":
        return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'})

    try:
        data = json.loads(request.body)
        tipo = data.get('tipo')
        monto = float(data.get('monto'))
        concepto = data.get('concepto', '')
        productos = data.get('productos', [])

        if monto <= 0:
            return JsonResponse({'estado': 'error', 'mensaje': 'El monto debe ser mayor a cero.'})

        if tipo == 'CARGO':
            CreditoService.registrar_cargo(
                cliente_id=cliente_id, monto=monto, concepto=concepto,
                usuario=request.user if request.user.is_authenticated else None,
                productos=productos,
            )
        elif tipo == 'ABONO':
            CreditoService.registrar_abono(
                cliente_id=cliente_id, monto=monto, concepto=concepto,
                usuario=request.user if request.user.is_authenticated else None,
            )
        else:
            return JsonResponse({'estado': 'error', 'mensaje': 'Tipo inválido'})

        return JsonResponse({'estado': 'ok'})
    except Exception as e:
        return JsonResponse({'estado': 'error', 'mensaje': str(e)})
    
def detalle_cliente_credito_pdf(request, cliente_id):
    """PDF con el historial completo de UN cliente de crédito."""
    cliente = get_object_or_404(ClienteCredito, id=cliente_id)
    movimientos = CreditoService.historial_con_saldo(cliente)  # orden cronológico
    saldo_actual = CreditoService.calcular_saldo(cliente)
    movimientos = [m for m in movimientos if not m['cancelado']]
    
 
    html = render_to_string('credito/cliente_detalle_pdf.html', {
        'cliente': cliente,
        'movimientos': movimientos,
        'saldo_actual': saldo_actual,
        'fecha_generacion': django_timezone.localtime(),
        
    })
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="credito_{cliente.nombre}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def cancelar_movimiento_credito(request, movimiento_id):
    if request.method != "POST":
        return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'})

    try:
        CreditoService.cancelar_movimiento(movimiento_id)
        return JsonResponse({'estado': 'ok'})
    except Exception as e:
        return JsonResponse({'estado': 'error', 'mensaje': str(e)})


class DetalleClienteCreditoView(View):
    def get(self, request, cliente_id):
        cliente = get_object_or_404(ClienteCredito, id=cliente_id)

        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')

        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

        resultado = CreditoService.historial_por_periodo(cliente, fecha_inicio, fecha_fin)
        movimientos = resultado['movimientos']
        movimientos.reverse()
        movimientos = [m for m in movimientos if not m['cancelado']]

        saldo_actual = CreditoService.calcular_saldo(cliente)

        return render(request, 'credito/cliente_detalle.html', {
            'titulo': 'Detalle de Cliente',
            'cliente': cliente,
            'movimientos': movimientos,
            'saldo_actual': saldo_actual,
            'saldo_inicial_periodo': resultado['saldo_inicial'],
            'fecha_inicio': fecha_inicio_str,
            'fecha_fin': fecha_fin_str,
        })
class ClienteCreditoEditarView(View):
    """Editar los datos de un cliente de crédito."""
    def get(self, request, cliente_id):
        cliente = get_object_or_404(ClienteCredito, id=cliente_id)
        return render(request, 'credito/cliente_editar.html', {
            'titulo': 'Editar Cliente',
            'cliente': cliente,
        })

    def post(self, request, cliente_id):
        cliente = get_object_or_404(ClienteCredito, id=cliente_id)
        cliente.nombre = request.POST.get('nombre')
        cliente.telefono = request.POST.get('telefono', '')
        cliente.contacto = request.POST.get('contacto', '')
        cliente.notas = request.POST.get('notas', '')
        cliente.save()
        return redirect('inventario:detalle_cliente_credito', cliente_id=cliente.id)

        
@staticmethod
def registrar_cargo(cliente_id, monto, concepto='', usuario=None, items=None):
    """
    items: lista de dicts [{concepto, cantidad, precio}, ...] — conceptos libres,
    no necesariamente productos reales del inventario.
    """
    cliente = ClienteCredito.objects.get(id=cliente_id)
    return MovimientoCredito.objects.create(
        cliente=cliente, tipo='CARGO', monto=monto, concepto=concepto, usuario=usuario,
        productos_json=items or [],
    )

def EliminarClienteAjax(request, pk):
    if request.method == "POST":
        #cliente manda a llamar a la funcion y busca el cliente con el id que se le pasa, si no lo encuentra manda un error 404
        cliente = get_object_or_404(ClienteCredito, pk=pk)
        try:
            # Intenta eliminar el cliente de la base de datos.
            cliente.delete()
            return JsonResponse({"estado": "ok"})
        except ProtectedError:
            return JsonResponse(
                {
                    "estado": "error",
                    "mensaje": "No se puede eliminar porque el cliente ya tiene transacciones.",
                }
            )

def nota_movimiento_credito_pdf(request, movimiento_id):
    movimiento = get_object_or_404(MovimientoCredito, id=movimiento_id)
    conceptos = movimiento.productos_json or []

    # Calculamos el subtotal de cada línea aquí, no en el template
    for item in conceptos:
        item['subtotal'] = float(item.get('cantidad', 0)) * float(item.get('precio', 0))

    html = render_to_string('credito/nota_credito_pdf.html', {
        'movimiento': movimiento,
        'cliente': movimiento.cliente,
        'conceptos': conceptos,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="nota_{movimiento.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response