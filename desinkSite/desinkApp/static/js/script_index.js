

document.addEventListener("DOMContentLoaded", () => {
  // Lógica para la sección de "Categorías"
  const categoriesCarousel = document.getElementById("categories-carousel");
  const categoryItems = categoriesCarousel ? Array.from(categoriesCarousel.children) : [];
  const categoriesArrow = document.querySelector(".categories-section .carousel-arrow");
  let currentCategoryIndex = 0;

  function updateCategoriesCarousel() {
    categoryItems.forEach((item, index) => {
      item.classList.toggle("active", index === currentCategoryIndex);
    });
  }

  if (categoriesArrow) {
    categoriesArrow.addEventListener("click", () => {
      currentCategoryIndex = (currentCategoryIndex + 1) % categoryItems.length;
      updateCategoriesCarousel();
    });
  }

  if (categoryItems.length > 0) {
    updateCategoriesCarousel(); // Inicia con el primer ítem activo
  }

  // Lógica para la sección de "Antes y Después"
  const beforeAfterTrack = document.querySelector(".carousel-track");
  const beforeAfterSlides = beforeAfterTrack ? Array.from(beforeAfterTrack.children) : [];
  const beforeAfterNextBtn = document.querySelector(".antes-despues .arrow-right");
  const beforeAfterDotsContainer = document.querySelector(".center-bottom-dots");

  let currentSlideIndex = 0;

  if (beforeAfterDotsContainer) {
    beforeAfterDotsContainer.innerHTML = beforeAfterSlides
      .map((_, i) => `<span class="${i === 0 ? "active" : ""}"></span>`)
      .join("");
    const beforeAfterDots = Array.from(beforeAfterDotsContainer.children);

    beforeAfterNextBtn.addEventListener("click", () => {
      currentSlideIndex = (currentSlideIndex + 1) % beforeAfterSlides.length;
      updateBeforeAfterCarousel();
    });

    beforeAfterDots.forEach((dot, index) => {
      dot.addEventListener("click", () => {
        currentSlideIndex = index;
        updateBeforeAfterCarousel();
      });
    });

    function updateBeforeAfterCarousel() {
      const slideWidth = beforeAfterSlides[0].getBoundingClientRect().width;
      beforeAfterTrack.style.transform = `translateX(-${currentSlideIndex * slideWidth}px)`;

      beforeAfterDots.forEach((dot, i) => {
        dot.classList.toggle("active", i === currentSlideIndex);
      });
    }
  }
});

//ANTES Y DESPUES CARROUSEL

document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const slides = Array.from(track.children);
  const nextButton = document.querySelector(".arrow-right");
  const dotsContainer = document.querySelector(".center-bottom-dots");
  
  // Crear puntitos dinámicamente según la cantidad de slides
  dotsContainer.innerHTML = slides.map((_, i) =>
    `<span class="${i === 0 ? "active" : ""}"></span>`
  ).join("");

  const dots = Array.from(dotsContainer.children);
  let currentIndex = 0;

  function updateCarousel() {
    const slideWidth = slides[0].getBoundingClientRect().width;
    track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;

    // Actualizar puntitos
    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === currentIndex);
    });
  }

  // Evento para avanzar con la flecha
  nextButton.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % slides.length;
    updateCarousel();
  });

  // Evento para cambiar al hacer clic en los puntitos
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      currentIndex = index;
      updateCarousel();
    });
  });

  // Auto-play opcional (cada 5 segundos)

});