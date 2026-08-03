import json

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from inventario.forms.configuracionTicket import ConfiguracionTicketForm
from inventario.models.catalogo.marca_producto import MarcaProducto
from inventario.models.configuracionTicket_modelo import ConfiguracionTicket
from inventario.models.detalleVenta_modelo import DetalleVenta
from inventario.models.producto_modelo import Producto
from inventario.models.venta_modelo import Venta
from django.http import JsonResponse
from django.db.models import F, ProtectedError
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

import json
from django.http import JsonResponse
from django.db import transaction

from inventario.models import Producto, Venta, DetalleVenta
from inventario.services.credito_service import CreditoService

def VentaView(request):
    productos = Producto.objects.all()
    data = {
        "titulo": "Venta de Productos",
        "mensaje": "Bienvenido al sistema de venta de productos.",
        "productos": productos,
    }
    return render(request, "venta.html", context=data)


def guardar_venta(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método no permitido"})

    try:
        data = json.loads(request.body)
        carrito = data.get("carrito", [])
        total = data.get("total")
        es_credito = data.get("es_credito", False)
        cliente_credito_id = data.get("cliente_credito_id")

        if not carrito:
            return JsonResponse({"ok": False, "error": "El carrito está vacío."})

        if es_credito and not cliente_credito_id:
            return JsonResponse(
                {"ok": False, "error": "Selecciona un cliente de crédito."}
            )

        with transaction.atomic():
            # Descuenta stock — igual para venta de contado o a crédito
            for item in carrito:
                producto = Producto.objects.select_for_update().get(id=item["id"])
                if producto.stock < item["cantidad"]:
                    raise ValueError(f"Stock insuficiente para {producto.nombre}.")
                producto.stock -= item["cantidad"]
                producto.save()

            if es_credito:
                # Registra el CARGO en la cuenta del cliente
                nombres = ", ".join(
                    [f"{item['cantidad']}x {item['nombre']}" for item in carrito]
                )
                concepto = f"Venta a crédito: {nombres}"

                # 👇 Esto es lo nuevo: armamos una lista con los productos vendidos
                # para poder regresarlos al stock si algún día se cancela este cargo
                productos_detalle = [
                    {
                        "producto_id": item["id"],
                        "cantidad": item["cantidad"],
                        "precio": item["precio"],
                    }
                    for item in carrito
                ]

                CreditoService.registrar_cargo(
                    cliente_id=cliente_credito_id,
                    monto=total,
                    concepto=concepto,
                    usuario=request.user if request.user.is_authenticated else None,
                    productos=productos_detalle,  # 👈 esto es lo único que se agregó a la llamada
                )
                return JsonResponse({"ok": True, "tipo": "credito"})
            else:
                # Flujo normal: crea la Venta y sus DetalleVenta
                venta = Venta.objects.create(
                    total=total,
                    estado="activa",
                    usuario=request.user if request.user.is_authenticated else None,
                )
                for item in carrito:
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto_id=item["id"],
                        cantidad=item["cantidad"],
                        precio=item["precio"],
                        subtotal=item["subtotal"],
                    )
                return JsonResponse(
                    {"ok": True, "venta_id": venta.id, "tipo": "contado"}
                )

    except ValueError as e:
        return JsonResponse({"ok": False, "error": str(e)})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})


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


from django.http import JsonResponse
from django.db.models import Q


def buscar_productos_ajax(request):
    """ ""
    Busca productos por código o nombre para el modal de búsqueda del punto de venta.
    GET /productos/buscar_ajax/?q=balata
    """
    q = request.GET.get("q", "").strip()

    productos = Producto.objects.all()

    if q:
        productos = productos.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q))

    productos = productos.order_by("nombre")[:20]

    data = [
        {
            "id": p.id,
            "codigo": p.codigo,
            "nombre": p.nombre,
            "precio": float(p.precio_venta),
            "stock": p.stock,
            'marca': p.marca.nombre,
        }
        for p in productos
    ]
    return JsonResponse({"productos": data})


