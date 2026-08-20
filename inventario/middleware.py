from django.shortcuts import redirect, render
from django.urls import reverse


class LoginRequeridoMiddleware:
    """
    1. Exige login para cualquier página que no sea pública.
    2. Cada rol restringido (Bodega, Mostrador, Oficina) solo puede ver
       las rutas de su lista blanca.
       Los superusuarios y usuarios sin ningún rol restringido ven todo, sin límite.
    """

    RUTAS_PUBLICAS = [
        '/login/',
        '/logout/',
        '/admin/',
        '/static/',
        '/media/',
    ]

    RUTAS_PERMITIDAS_POR_ROL = {
        'Bodega': [
            '/inventarioMovimiento/salida/',
            '/producto/producto_lista/',
            '/producto/producto_detalle/',
            '/productos/buscar_ajax/',
        ],
        'Mostrador': [
            '/producto/producto_lista/',
            '/producto/producto_detalle/',
            '/productos/exportar/',
            '/inventarioMovimiento/salida/',
            '/inventarioMovimiento/historial/',
            '/productos/buscar_ajax/',
            '/dashboard/dashboard/',
            '/credito/cliente_lista/',
            '/credito/cliente_detalle/',
            '/credito/clientes/',
            '/credito/movimiento/',
            '/credito/cliente/',
            

        ],
        'Oficina': [
            '/dashboard/dashboard/',
            '/producto/producto_lista/',
            '/producto/producto_detalle/',
            '/producto/producto_crear/',
            '/producto/producto_editar/',
            '/eliminarProducto/',
            '/productos/buscar_ajax/',
            '/inventarioMovimiento/salida/',
            '/inventarioMovimiento/entrada/',
            '/inventarioMovimiento/historial/',
            '/proveedorEmpresa/proveedorEmpresa_lista/',
            '/proveedorEmpresa/proveedorEmpresa_detalle/',
            '/proveedorEmpresa/proveedorEmpresa_editar/',
            '/eliminarProveedor/',
            '/contactoProveedor/contactoProveedor_lista/',
            '/contactoProveedor/contactoProveedor_detalle/',
            '/contactoProveedor/contactoProveedor_crear/',
            '/contactoProveedor/contactoProveedor_editar/',
            '/contacto_proveedor/',
            '/categoriaProducto/categoria_lista/',
            '/categoriaProducto/categoria_detalle/',
            '/categoriaProducto/categoria_crear/',
            '/categoriaProducto/categoria_editar/',
            '/categoriaProducto/',
        ],
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ruta_es_publica = any(request.path.startswith(r) for r in self.RUTAS_PUBLICAS)

        # 1. Sin sesión y ruta no pública -> manda a login
        if not request.user.is_authenticated and not ruta_es_publica:
            return redirect(f"{reverse('login')}?next={request.path}")

        # 2. Con sesión: revisa si pertenece a un rol restringido
        if request.user.is_authenticated and not ruta_es_publica:
            if request.user.is_superuser:
                return self.get_response(request)

            grupos_usuario = set(request.user.groups.values_list('name', flat=True))
            roles_restringidos = set(self.RUTAS_PERMITIDAS_POR_ROL.keys())
            grupos_restrictivos_del_usuario = grupos_usuario & roles_restringidos

            if grupos_restrictivos_del_usuario:
                permitido = False
                for rol in grupos_restrictivos_del_usuario:
                    rutas_del_rol = self.RUTAS_PERMITIDAS_POR_ROL[rol]
                    if any(request.path.startswith(r) for r in rutas_del_rol):
                        permitido = True
                        break

                if not permitido:
                    return render(request, 'errors/sin_permiso.html', status=403)

        return self.get_response(request)