from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from inventario.models import Producto, MovimientoInventario


def _calcular_kardex(producto):
    """Devuelve la lista de movimientos de un producto con su saldo acumulado."""
    movimientos_qs = MovimientoInventario.objects.filter(producto=producto).order_by('fecha')

    saldo = 0
    movimientos = []
    for m in movimientos_qs:
        if m.tipo == 'ENTRADA':
            saldo += m.cantidad
        else:
            saldo -= m.cantidad
        movimientos.append({
            'fecha': m.fecha,
            'tipo': m.tipo,
            'motivo': m.get_motivo_display(),
            'entrada': m.cantidad if m.tipo == 'ENTRADA' else None,
            'salida': m.cantidad if m.tipo == 'SALIDA' else None,
            'saldo': saldo,
            'usuario': m.usuario,
            'observaciones': m.observaciones,
        })
    return movimientos, saldo


class KardexProductoView(View):
    """Pantalla: busca un producto y muestra su kardex completo en pantalla."""

    def get(self, request):
        producto_id = request.GET.get('producto_id')
        producto = None
        movimientos = []
        saldo_actual = 0

        if producto_id:
            producto = get_object_or_404(Producto, id=producto_id)
            movimientos, saldo_actual = _calcular_kardex(producto)
            movimientos.reverse()  # el más reciente arriba, para lectura en pantalla

        context = {
            'titulo': 'Kardex de producto',
            'producto': producto,
            'movimientos': movimientos,
            'saldo_actual': saldo_actual,
        }
        return render(request, 'kardex/kardex.html', context)


def kardex_pdf(request, producto_id):
    """Genera el PDF del kardex de un producto, en orden cronológico."""
    producto = get_object_or_404(Producto, id=producto_id)
    movimientos, saldo_actual = _calcular_kardex(producto)  # orden cronológico, ideal para PDF

    html = render_to_string('kardex/kardex_pdf.html', {
        'producto': producto,
        'movimientos': movimientos,
        'saldo_actual': saldo_actual,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="kardex_{producto.codigo}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response