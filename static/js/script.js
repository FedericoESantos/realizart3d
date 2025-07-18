let indice = 0;

function moverCarrusel(direccion) {
  const imagenes = document.querySelectorAll('.carrusel-inner img');
  const total = imagenes.length;

  indice += direccion;

  if (indice < 0) indice = total - 1;
  if (indice >= total) indice = 0;

  moverACarousel(indice);
}

function moverACarousel(pos) {
  const imagenes = document.querySelectorAll('.carrusel-inner img');
  const ancho = document.querySelector('.carrusel').offsetWidth;

  indice = pos;

  document.querySelector('.carrusel-inner').style.transform = `translateX(-${ancho * indice}px)`;

  const puntos = document.querySelectorAll('.puntos span');
  puntos.forEach((p, i) => {
    p.classList.toggle('activo', i === indice);
  });
}

function crearPuntos() {
  const imagenes = document.querySelectorAll('.carrusel-inner img');
  const puntosContainer = document.querySelector('.puntos');
  puntosContainer.innerHTML = '';

  imagenes.forEach((_, i) => {
    const span = document.createElement('span');
    span.addEventListener('click', () => moverACarousel(i));
    puntosContainer.appendChild(span);
  });

  moverACarousel(0);
}

window.addEventListener('resize', () => moverACarousel(indice));

crearPuntos();

