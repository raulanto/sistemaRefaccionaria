from django.db import transaction
from inventario.models import Producto, MovimientoInventario


class InventarioService:

    @staticmethod
    @transaction.atomic
    def registrar_entrada(producto_id, cantidad, motivo, observaciones='', usuario=None):
        producto = Producto.objects.select_for_update().get(id=producto_id)
        producto.stock += cantidad
        producto.save()
        return MovimientoInventario.objects.create(
            producto=producto, tipo='ENTRADA', cantidad=cantidad,
            motivo=motivo, observaciones=observaciones, usuario=usuario,
        )

    @staticmethod
    @transaction.atomic
    def registrar_salida(producto_id, cantidad, motivo, observaciones='', usuario=None):
        producto = Producto.objects.select_for_update().get(id=producto_id)
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
        producto.stock -= cantidad
        producto.save()
        return MovimientoInventario.objects.create(
            producto=producto, tipo='SALIDA', cantidad=cantidad,
            motivo=motivo, observaciones=observaciones, usuario=usuario,
        )

    @staticmethod
    @transaction.atomic
    def registrar_multiple(tipo, items, usuario=None):
        """
        tipo: 'ENTRADA' o 'SALIDA'
        items: lista de dicts [{producto_id, cantidad, motivo, observaciones}, ...]
        Si CUALQUIER producto falla (ej. stock insuficiente), se cancela todo el lote.
        """
        resultados = []
        for item in items:
            if tipo == 'ENTRADA':
                mov = InventarioService.registrar_entrada(
                    producto_id=item['producto_id'],
                    cantidad=item['cantidad'],
                    motivo=item['motivo'],
                    observaciones=item.get('observaciones', ''),
                    usuario=usuario,
                )
            else:
                mov = InventarioService.registrar_salida(
                    producto_id=item['producto_id'],
                    cantidad=item['cantidad'],
                    motivo=item['motivo'],
                    observaciones=item.get('observaciones', ''),
                    usuario=usuario,
                )
            resultados.append(mov)
        return resultados