import json

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from inventario.form.configuracionTicket import ConfiguracionTicketForm
from inventario.models.catalogo.marca_producto import MarcaProducto
from inventario.models.configuracionTicket_modelo import ConfiguracionTicket
from inventario.models.detalleVenta_modelo import DetalleVenta
from inventario.models.producto_modelo import Producto
from inventario.models.venta_modelo import Venta
from django.http import JsonResponse
from django.db.models import F, ProtectedError
from django.views.generic import ListView
from django.shortcuts import get_object_or_404



def VentaView(request):
    productos = Producto.objects.all()
    data = {
        "titulo": "Venta de Productos",
        "mensaje": "Bienvenido al sistema de venta de productos.",
        "productos": productos,
    }
    return render(request, "venta.html", context=data)


def guardar_venta(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            carrito = data.get("carrito", [])
            total = data.get("total", 0)

            # 1. Aseguramos crear la venta convirtiendo el total a float/decimal
            venta = Venta.objects.create(total=float(total))

            # 2. Barremos los artículos
            for item in carrito:
                # Forzamos que el ID se maneje como un entero por si llega como string
                producto_id = int(item["id"])
                producto = get_object_or_404(Producto, id=producto_id)

                cantidad = int(item["cantidad"])
                # Forzamos que el precio sea un flotante/decimal puro
                precio_unitario = float(item["precio"])

                if producto.stock < cantidad:
                    return JsonResponse(
                        {
                            "ok": False,
                            "error": f"Stock insuficiente para {producto.nombre}",
                        },
                        status=400,
                    )

                # 3. Guardamos el detalle con tipos de datos limpios
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio=precio_unitario,
                    subtotal=cantidad * precio_unitario,
                )

                # 4. Descontamos stock
                producto.stock -= cantidad
                producto.save()

            return JsonResponse({"ok": True, "venta_id": venta.id})

        except Exception as e:
            # Si algo falla, esto te dirá EXACTAMENTE qué línea o variable rompió el código
            return JsonResponse(
                {"ok": False, "error": f"Error en backend: {str(e)}"}, status=400
            )
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            carrito = data["carrito"]
            total = data["total"]

            # 1. Creamos la cabecera de la venta
            venta = Venta.objects.create(total=total)

            # 2. Iteramos sobre los artículos enviados desde el Javascript
            for item in carrito:
                # 🟢 Buscamos el objeto Producto real usando su ID enviado por el frontend
                # (Asegúrate de que tu Javascript mande el 'id' del producto)
                producto = get_object_or_404(Producto, id=item["id"])

                # Opcional: Validar stock antes de vender
                if producto.stock < int(item["cantidad"]):
                    return JsonResponse(
                        {
                            "ok": False,
                            "error": f"Stock insuficiente para {producto.nombre}",
                        },
                        status=400,
                    )

                # 🟢 Creamos el registro del renglón usando la instancia del producto
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,  # <-- Ahora sí le pasamos el objeto Producto real
                    cantidad=item["cantidad"],
                    precio=item["precio"],
                    subtotal=float(item["cantidad"]) * float(item["precio"]),
                )

                # 🟢 Descontamos las refacciones vendidas de tu inventario
                producto.stock -= int(item["cantidad"])
                producto.save()

            return JsonResponse({"ok": True, "venta_id": venta.id})

        except Exception as e:
            return JsonResponse({"ok": False, "error": str(e)}, status=400)

def ventas_historial(request):
    """Trae todas las ventas del punto de venta ordenadas desde la más reciente"""
    ventas = Venta.objects.all().order_by("-fecha")
    return render(request, "ventas_historial.html", {"ventas": ventas})

def cancelar_venta(request, id):

    # 🔴 Solo permitimos que se ejecute con método POST
    # (evita que cualquiera lo ejecute desde la URL)
    if request.method == "POST":

        # 🔍 Buscamos la venta en la base de datos
        # si no existe, devuelve error 404 automático
        venta = get_object_or_404(Venta, id=id)

        # ⚠️ Verificamos si la venta ya está cancelada
        # para evitar duplicar devoluciones de stock
        if venta.estado == "cancelada":
            return JsonResponse(
                {"estado": "error", "mensaje": "La venta ya está cancelada"}
            )

        # 📦 Obtenemos todos los productos de esa venta
        detalles = DetalleVenta.objects.filter(venta=venta)

        # 🔁 Recorremos cada producto vendido
        for d in detalles:

            # 🔄 Obtenemos el producto relacionado
            producto = d.producto

            # 📈 Regresamos el stock que se había descontado
            producto.stock += d.cantidad

            # 💾 Guardamos el nuevo stock en la base de datos
            producto.save()

        # ❌ Marcamos la venta como cancelada (NO la borramos)
        venta.estado = "cancelada"

        # 💾 Guardamos el cambio de estado
        venta.save()

        # 📤 Respondemos al frontend (JavaScript)
        return JsonResponse({"estado": "ok"})
