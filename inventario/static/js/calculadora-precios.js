/* ===========================================================
   BUSCADOR DE CATEGORIA / MARCA
   Las listas `categorias` y `marcas` se definen en el template
   (necesitan datos de Django), este archivo solo las consume.
   =========================================================== */
function buscarYSeleccionarLista(input, selectId, lista) {
    const encontrado = lista.find(item => item.nombre === input.value.trim());
    document.getElementById(selectId).value = encontrado ? encontrado.id : '';
    input.classList.toggle('is-invalid', !encontrado);
}

/* ===========================================================
   CALCULADORA DE PRECIOS (bidireccional)
   Costo / IVA / Margen  ->  Precio de Venta
   Precio de Venta       ->  Margen
   =========================================================== */
(function () {
    'use strict';

    function iniciar() {
        const inputCosto = document.getElementById('inputCosto');
        const selectTieneIva = document.getElementById('selectTieneIva');
        const inputIva = document.getElementById('inputIva');
        const inputCostoConIva = document.getElementById('inputCostoConIva');
        const inputMargen = document.getElementById('inputMargen');
        const inputPrecioVenta = document.getElementById('inputPrecioVenta');

        // Si no estamos en el formulario de producto, no hacemos nada.
        if (!inputCosto || !inputPrecioVenta || !inputMargen) {
            return;
        }

        function numero(valor) {
            const n = parseFloat(valor);
            return isNaN(n) ? 0 : n;
        }

        function obtenerCostoConIva() {
            const costo = numero(inputCosto.value);
            const tieneIva = selectTieneIva.value === 'True';
            return tieneIva ? costo * (1 + numero(inputIva.value) / 100) : costo;
        }

        function calcularDesdeMargen() {
            const costoConIva = obtenerCostoConIva();
            const precioVenta = costoConIva * (1 + numero(inputMargen.value) / 100);

            inputCostoConIva.value = costoConIva.toFixed(2);
            inputPrecioVenta.value = precioVenta.toFixed(2);
        }

        function calcularDesdePrecioVenta() {
            const costoConIva = obtenerCostoConIva();
            const precioVenta = numero(inputPrecioVenta.value);

            inputCostoConIva.value = costoConIva.toFixed(2);
            inputMargen.value = costoConIva > 0
                ? ((precioVenta / costoConIva - 1) * 100).toFixed(2)
                : '0.00';
        }

        // Modo edicion: reconstruye el margen real a partir de los
        // valores ya guardados, en vez de dejar el 30% por defecto.
        function inicializarMargen() {
            const costoConIva = obtenerCostoConIva();
            const precioVentaGuardado = numero(inputPrecioVenta.value);

            if (costoConIva > 0 && precioVentaGuardado > 0) {
                const margenReal = (precioVentaGuardado / costoConIva - 1) * 100;
                if (margenReal >= 0) {
                    inputMargen.value = margenReal.toFixed(2);
                }
            }
        }

        [inputCosto, selectTieneIva, inputIva, inputMargen].forEach(function (campo) {
            campo.addEventListener('input', calcularDesdeMargen);
            campo.addEventListener('change', calcularDesdeMargen);
        });

        inputPrecioVenta.addEventListener('input', calcularDesdePrecioVenta);
        inputPrecioVenta.addEventListener('change', calcularDesdePrecioVenta);

        // Al enfocar un campo de dinero, selecciona todo el contenido
        // para escribir encima sin tener que borrar lo que ya esta.
        document.querySelectorAll('.campo-dinero').forEach(function (campo) {
            campo.addEventListener('focus', function () {
                this.select();
            });
        });

        // Estado inicial de los campos calculados.
        inicializarMargen();
        if (numero(inputCosto.value) > 0 || numero(inputPrecioVenta.value) > 0) {
            calcularDesdeMargen();
        } else {
            inputCostoConIva.value = '';
        }
    }

    // Si el script se carga al final del body, DOMContentLoaded ya paso
    // y el listener nunca dispararia. Por eso se verifica el estado.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', iniciar);
    } else {
        iniciar();
    }
})();