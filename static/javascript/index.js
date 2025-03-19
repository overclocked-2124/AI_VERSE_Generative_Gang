// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Add animation when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Hero section fade-in
    const hero = document.querySelector('.hero');
    hero.style.opacity = 0;
    
    setTimeout(() => {
        hero.style.transition = 'opacity 1s ease-in-out';
        hero.style.opacity = 1;
    }, 100);
    
    // Cards animation
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 300 + (index * 200));
    });
});

// Demo button functionality
document.getElementById('demo-btn').addEventListener('click', (e) => {
    e.preventDefault();
    alert('Choose a character: 1. Rude Banker, 2. Humble Actor');
});
