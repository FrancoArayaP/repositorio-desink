// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('serviceCarousel');
    const nextBtn = document.getElementById('carouselNext');
    const indicators = document.querySelectorAll('.indicator');
    
    // Verificar que los elementos existen
    if (!carousel || !nextBtn) {
        console.error('No se encontraron los elementos del carrusel');
        return;
    }
    
    let isDown = false;
    let startX;
    let scrollLeft;
    
    // Funcionalidad de arrastre
    carousel.addEventListener('mousedown', (e) => {
        isDown = true;
        carousel.style.cursor = 'grabbing';
        startX = e.pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
    });
    
    carousel.addEventListener('mouseleave', () => {
        isDown = false;
        carousel.style.cursor = 'grab';
    });
    
    carousel.addEventListener('mouseup', () => {
        isDown = false;
        carousel.style.cursor = 'grab';
    });
    
    carousel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 2;
        carousel.scrollLeft = scrollLeft - walk;
    });
    
    // Botón de navegación
    nextBtn.addEventListener('click', () => {
        const scrollAmount = carousel.offsetWidth;
        carousel.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
        console.log('Botón clickeado'); // Para debug
    });
    
    // Actualizar indicadores según scroll
    carousel.addEventListener('scroll', () => {
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        const currentScroll = carousel.scrollLeft;
        const percentage = currentScroll / maxScroll;
        
        indicators.forEach((indicator, index) => {
            indicator.classList.remove('active');
        });
        
        if (percentage < 0.33) {
            indicators[0]?.classList.add('active');
        } else if (percentage < 0.66) {
            indicators[1]?.classList.add('active');
        } else {
            indicators[2]?.classList.add('active');
        }
    });
    
    // Click en indicadores
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            const scrollAmount = (carousel.scrollWidth - carousel.clientWidth) * (index / (indicators.length - 1));
            carousel.scrollTo({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });
    });
});