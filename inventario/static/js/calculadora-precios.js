/* ============================================================
   CALCULADORA DE PRECIOS — reutilizable
   Requiere estos elementos en la página (por id):
     - inputCosto
     - inputMargen
     - selectTieneIva
     - inputPrecioVenta
     - inputPrecioConIva
     - labelMargenReal

   Uso: solo incluye este script en cualquier página que tenga
   esos campos, y se activa solo (no necesitas llamarlo a mano).
   ============================================================ */

const CalculadoraPrecios = (function () {
    const IVA_RATE = 0.16;

    let inputCosto, inputMargen, selectTieneIva, inputPrecioVenta, inputPrecioConIva, labelMargenReal;

    function tasaIva() {
        return selectTieneIva.value === 'True' ? (1 + IVA_RATE) : 1;
    }

    // Costo + % Utilidad -> Precio sin IVA -> Precio con IVA
    function calcularDesdeMargen() {
        const costo = parseFloat(inputCosto.value) || 0;
        const margen = parseFloat(inputMargen.value) || 0;

        const precioSinIva = costo * (1 + margen / 100);
        const precioConIva = precioSinIva * tasaIva();

        inputPrecioVenta.value = precioSinIva.toFixed(2);
        inputPrecioConIva.value = precioConIva.toFixed(2);
        labelMargenReal.innerText = margen.toFixed(1) + '%';
    }

    // Precio con IVA (escrito a mano) -> Precio sin IVA -> % Utilidad real
    function calcularDesdePrecioFinal() {
        const costo = parseFloat(inputCosto.value) || 0;
        const precioConIva = parseFloat(inputPrecioConIva.value) || 0;

        const precioSinIva = precioConIva / tasaIva();
        const margenReal = costo > 0 ? ((precioSinIva / costo) - 1) * 100 : 0;

        inputPrecioVenta.value = precioSinIva.toFixed(2);
        inputMargen.value = margenReal.toFixed(2);
        labelMargenReal.innerText = margenReal.toFixed(1) + '%';
    }

    function inicializar() {
        inputCosto = document.getElementById('inputCosto');
        inputMargen = document.getElementById('inputMargen');
        selectTieneIva = document.getElementById('selectTieneIva');
        inputPrecioVenta = document.getElementById('inputPrecioVenta');
        inputPrecioConIva = document.getElementById('inputPrecioConIva');
        labelMargenReal = document.getElementById('labelMargenReal');

        if (!inputCosto || !inputMargen || !inputPrecioVenta) {
            return; // esta página no tiene el bloque de precios, no hace nada
        }

        inputCosto.addEventListener('input', calcularDesdeMargen);
        inputMargen.addEventListener('input', calcularDesdeMargen);
        selectTieneIva.addEventListener('change', calcularDesdeMargen);
        inputPrecioConIva.addEventListener('input', calcularDesdePrecioFinal);

        // Al cargar: si ya hay costo y precio guardados (edición), calcula el % real
        const costo = parseFloat(inputCosto.value) || 0;
        const precioVentaGuardado = parseFloat(inputPrecioVenta.value) || 0;

        if (costo > 0 && precioVentaGuardado > 0) {
            const margenInicial = ((precioVentaGuardado / costo) - 1) * 100;
            inputMargen.value = margenInicial.toFixed(2);
        }

        calcularDesdeMargen();
    }

    document.addEventListener('DOMContentLoaded', inicializar);

    return { calcularDesdeMargen, calcularDesdePrecioFinal };
})();