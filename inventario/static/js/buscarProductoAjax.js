/* ============================================================
   BUSCADOR DE PRODUCTOS REUTILIZABLE
   Requiere: Bootstrap 5 JS, y el partial modal_buscar_producto.html
   incluido en la página.

   Uso desde cualquier pantalla:

       BuscadorProducto.abrir(function(producto) {
           console.log(producto.id, producto.codigo, producto.nombre, producto.stock);
       });

   Opcional: si solo quieres productos con stock disponible,
   pasa un segundo argumento en true:

       BuscadorProducto.abrir(callback, { soloConStock: true });
   ============================================================ */

const BuscadorProducto = (function () {
  let modal = null;
  let inputBuscar = null;
  let resultadosContainer = null;
  let sinResultados = null;

  let resultados = [];
  let indiceActivo = -1;
  let debounceTimer = null;
  let callbackActual = null;
  let opcionesActuales = {};

  function init() {
    const modalEl = document.getElementById('modalBuscarProductoGlobal');
    if (!modalEl) return; // la página no incluyó el partial, no hace nada

    modal = new bootstrap.Modal(modalEl);
    inputBuscar = document.getElementById('inputBuscarProductoGlobal');
    resultadosContainer = document.getElementById('resultadosBusquedaGlobal');
    sinResultados = document.getElementById('sinResultadosBusquedaGlobal');

    modalEl.addEventListener('shown.bs.modal', () => inputBuscar.focus());

    inputBuscar.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => buscar(this.value.trim()), 250);
    });

    inputBuscar.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (indiceActivo < resultados.length - 1) indiceActivo++;
        render();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (indiceActivo > 0) indiceActivo--;
        render();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (indiceActivo >= 0) seleccionar(indiceActivo);
      } else if (e.key === 'Escape') {
        modal.hide();
      }
    });
  }

  function abrir(callback, opciones = {}) {
    if (!modal) {
      console.error('BuscadorProducto: falta incluir partials/modal_buscar_producto.html en esta página.');
      return;
    }
    callbackActual = callback;
    opcionesActuales = opciones;
    inputBuscar.value = '';
    resultadosContainer.innerHTML = '';
    sinResultados.style.display = 'none';
    modal.show();
    buscar('');
  }

  function buscar(query) {
    fetch(`/productos/buscar_ajax/?q=${encodeURIComponent(query)}`)
      .then((r) => r.json())
      .then((data) => {
        resultados = data.productos;
        indiceActivo = resultados.length > 0 ? 0 : -1;
        render();
      })
      .catch(() => {
        resultadosContainer.innerHTML = '<div class="text-danger p-3">Error al buscar productos.</div>';
      });
  }

  function render() {
    if (resultados.length === 0) {
      resultadosContainer.innerHTML = '';
      sinResultados.style.display = '';
      return;
    }
    sinResultados.style.display = 'none';

    resultadosContainer.innerHTML = resultados.map((p, i) => {
      const sinStock = p.stock <= 0;
      const bloqueado = sinStock && opcionesActuales.soloConStock; // solo bloquea si la pantalla lo pidió
      return `
        <button type="button"
            class="list-group-item list-group-item-action resultado-item-global ${i === indiceActivo ? 'activo' : ''} ${bloqueado ? 'agotado' : ''}"
            onclick="BuscadorProducto._seleccionar(${i})">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <span class="badge bg-light text-dark border me-2">${p.codigo}</span>
              <strong>${p.nombre}</strong>
              ${p.marca ? '<span class="badge bg-secondary-subtle text-black ms-1">' + p.marca + '</span>' : ''}
            </div>
            <div class="text-end">
              <div class="small ${sinStock ? 'text-danger' : 'text-muted'}">
                ${sinStock ? 'Agotado' : 'Stock: ' + p.stock}
              </div>
            </div>
          </div>
        </button>`;
    }).join('');

    const activo = resultadosContainer.querySelector('.activo');
    if (activo) activo.scrollIntoView({ block: 'nearest' });
  }

  function seleccionar(index) {
    const producto = resultados[index];
    if (!producto) return;
    if (opcionesActuales.soloConStock && producto.stock <= 0) return;

    modal.hide();
    if (callbackActual) callbackActual(producto);
  }

  document.addEventListener('DOMContentLoaded', init);

  // API pública. _seleccionar es semi-privado (lo usan los onclick generados).
  return { abrir, _seleccionar: seleccionar };
})();