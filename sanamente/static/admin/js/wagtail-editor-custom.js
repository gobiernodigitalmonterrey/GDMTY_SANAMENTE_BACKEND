/**
 * Función de resize forzado al termino al inicializar para redibujar OSM Widget
 */
window.addEventListener('DOMContentLoaded', (event) => {
    window.dispatchEvent(new Event('resize'))
})
