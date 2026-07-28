from django.utils import timezone as django_timezone
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from inventario.models import ClienteCredito
from inventario.services.credito_service import CreditoService
from xhtml2pdf import pisa


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
        """Crear un cliente nuevo desde el modal propio."""
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono', '')
        contacto = request.POST.get('contacto', '')
        notas = request.POST.get('notas', '')

        if nombre:
            ClienteCredito.objects.create(
                nombre=nombre, telefono=telefono, contacto=contacto, notas=notas
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


class DetalleClienteCreditoView(View):
    """Historial de movimientos de un cliente, tipo Kardex de dinero."""
    def get(self, request, cliente_id):
        cliente = get_object_or_404(ClienteCredito, id=cliente_id)
        movimientos = CreditoService.historial_con_saldo(cliente)
        movimientos.reverse()  # más reciente arriba
        saldo_actual = CreditoService.calcular_saldo(cliente)

        return render(request, 'credito/cliente_detalle.html', {
            'titulo': 'Detalle de Cliente',
            'cliente': cliente,
            'movimientos': movimientos,
            
            'saldo_actual': saldo_actual,
        })


def registrar_movimiento_credito(request, cliente_id):
    """AJAX: registra un cargo o un abono."""
    if request.method != "POST":
        return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'})

    try:
        data = json.loads(request.body)
        tipo = data.get('tipo')  # 'CARGO' o 'ABONO'
        monto = float(data.get('monto'))
        concepto = data.get('concepto', '')

        if monto <= 0:
            return JsonResponse({'estado': 'error', 'mensaje': 'El monto debe ser mayor a cero.'})

        if tipo == 'CARGO':
            CreditoService.registrar_cargo(
                cliente_id=cliente_id, monto=monto, concepto=concepto,
                usuario=request.user if request.user.is_authenticated else None,
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