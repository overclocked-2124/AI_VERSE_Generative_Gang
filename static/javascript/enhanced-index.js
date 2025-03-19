// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all animations and effects
    initSmoothScrolling();
    initParticleBackground();
    initCustomCursor();
    initScrollIndicator();
    initRevealAnimations();
    initHeroAnimation();
    initCardAnimations();
    initLogoAnimation();
    initDemoButton();
    initTypingEffect();
});

// Smooth scrolling with enhanced easing
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                // Add active class to clicked nav item
                document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
                this.classList.add('active');
                
                // Smooth scroll with easing
                const startPosition = window.pageYOffset;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
                const distance = targetPosition - startPosition;
                const duration = 1000;
                let start = null;
                
                function step(timestamp) {
                    if (!start) start = timestamp;
                    const progress = timestamp - start;
                    const percentage = Math.min(progress / duration, 1);
                    
                    // Easing function: easeInOutCubic
                    const easing = percentage < 0.5
                        ? 4 * percentage * percentage * percentage
                        : 1 - Math.pow(-2 * percentage + 2, 3) / 2;
                    
                    window.scrollTo(0, startPosition + distance * easing);
                    
                    if (progress < duration) {
                        window.requestAnimationFrame(step);
                    }
                }
                
                window.requestAnimationFrame(step);
            }
        });
    });
}

// Create particle background effect
function initParticleBackground() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    document.body.appendChild(particlesContainer);
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random particle styling
    const size = Math.random() * 5 + 1;
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;
    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 5;
    
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background-color: rgba(214, 255, 133, ${Math.random() * 0.3 + 0.1});
        border-radius: 50%;
        top: ${posY}%;
        left: ${posX}%;
        animation: float ${duration}s ease-in-out ${delay}s infinite;
        opacity: ${Math.random() * 0.5 + 0.1};
    `;
    
    container.appendChild(particle);
}

// Custom cursor effect
function initCustomCursor() {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    
    const cursorDot = document.createElement('div');
    cursorDot.className = 'cursor-dot';
    
    document.body.appendChild(cursor);
    document.body.appendChild(cursorDot);
    
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // The dot follows with no delay
        cursorDot.style.left = e.clientX + 'px';
        cursorDot.style.top = e.clientY + 'px';
    });
    
    // Cursor effects on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .card, .logo');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.width = '50px';
            cursor.style.height = '50px';
            cursor.style.backgroundColor = 'rgba(214, 255, 133, 0.2)';
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.style.width = '20px';
            cursor.style.height = '20px';
            cursor.style.backgroundColor = 'rgba(214, 255, 133, 0.5)';
        });
    });
}

// Scroll progress indicator
function initScrollIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'scroll-indicator';
    document.body.appendChild(indicator);
    
    window.addEventListener('scroll', () => {
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercentage = (scrollTop / scrollHeight) * 100;
        
        indicator.style.width = scrollPercentage + '%';
    });
}

// Reveal animations on scroll
function initRevealAnimations() {
    // Add reveal class to elements we want to animate
    const sections = document.querySelectorAll('section, .card');
    sections.forEach(section => {
        if (!section.classList.contains('hero')) {
            section.classList.add('reveal');
        }
    });
    
    // Check if elements are in viewport and animate them
    function checkReveal() {
        const reveals = document.querySelectorAll('.reveal');
        const windowHeight = window.innerHeight;
        
        reveals.forEach(reveal => {
            const revealTop = reveal.getBoundingClientRect().top;
            const revealPoint = 150;
            
            if (revealTop < windowHeight - revealPoint) {
                reveal.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', checkReveal);
    // Initial check
    checkReveal();
}

// Hero section animation
function initHeroAnimation() {
    const hero = document.querySelector('.hero');
    const heading = hero.querySelector('h1');
    const paragraph = hero.querySelector('p');
    const button = hero.querySelector('.btn');
    
    // Initial state
    hero.style.opacity = 0;
    heading.style.opacity = 0;
    heading.style.transform = 'translateY(-20px)';
    paragraph.style.opacity = 0;
    paragraph.style.transform = 'translateY(-20px)';
    button.style.opacity = 0;
    button.style.transform = 'translateY(-20px)';
    
    // Animate in sequence
    setTimeout(() => {
        hero.style.transition = 'opacity 1s ease';
        hero.style.opacity = 1;
        
        setTimeout(() => {
            heading.style.transition = 'all 0.8s ease';
            heading.style.opacity = 1;
            heading.style.transform = 'translateY(0)';
            
            setTimeout(() => {
                paragraph.style.transition = 'all 0.8s ease';
                paragraph.style.opacity = 1;
                paragraph.style.transform = 'translateY(0)';
                
                setTimeout(() => {
                    button.style.transition = 'all 0.8s ease';
                    button.style.opacity = 1;
                    button.style.transform = 'translateY(0)';
                }, 200);
            }, 200);
        }, 200);
    }, 300);
}

// Card animations
function initCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        // 3D tilt effect on hover
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const angleX = (y - centerY) / 20;
            const angleY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateY(-10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
        
        // Initial animation
        card.style.opacity = 0;
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 600 + (index * 200));
    });
}

// Logo animation
function initLogoAnimation() {
    const logo = document.querySelector('.logo-container');
    
    logo.addEventListener('mouseenter', () => {
        const logoText = document.querySelector('.logo:nth-child(2)');
        logoText.style.animation = 'pulse 1s infinite';
    });
    
    logo.addEventListener('mouseleave', () => {
        const logoText = document.querySelector('.logo:nth-child(2)');
        logoText.style.animation = 'none';
    });
}

// Enhanced demo button
function initDemoButton() {
    const demoBtn = document.getElementById('demo-btn');
    
    demoBtn.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Create modal for character selection
        const modal = document.createElement('div');
        modal.className = 'character-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close-modal">&times;</span>
                <h2>Choose Your AI Character</h2>
                <div class="character-options">
                    <div class="character-card" data-character="banker">
                        <div class="character-icon">💼</div>
                        <h3>Rude Banker</h3>
                        <p>A no-nonsense financial expert with little patience for basic questions.</p>
                    </div>
                    <div class="character-card" data-character="actor">
                        <div class="character-icon">🎭</div>
                        <h3>Humble Actor</h3>
                        <p>A thoughtful performer who explains concepts with creative metaphors.</p>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add modal styles
        const style = document.createElement('style');
        style.textContent = `
            .character-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .modal-content {
                background-color: var(--dark-gray);
                border-radius: 8px;
                padding: 30px;
                max-width: 600px;
                width: 90%;
                position: relative;
                transform: translateY(20px);
                transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border: 1px solid rgba(214, 255, 133, 0.3);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            }
            
            .close-modal {
                position: absolute;
                top: 15px;
                right: 20px;
                font-size: 28px;
                cursor: pointer;
                color: white;
                transition: color 0.3s ease;
            }
            
            .close-modal:hover {
                color: var(--orange);
            }
            
            .character-options {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 20px;
            }
            
            .character-card {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 1px solid transparent;
            }
            
            .character-card:hover {
                transform: translateY(-5px);
                border-color: var(--lime);
            }
            
            .character-icon {
                font-size: 40px;
                margin-bottom: 10px;
            }
            
            @media (max-width: 600px) {
                .character-options {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        document.head.appendChild(style);
        
        // Animate modal in
        setTimeout(() => {
            modal.style.opacity = 1;
            modal.querySelector('.modal-content').style.transform = 'translateY(0)';
        }, 10);
        
        // Close modal functionality
        const closeModal = () => {
            modal.style.opacity = 0;
            modal.querySelector('.modal-content').style.transform = 'translateY(20px)';
            setTimeout(() => {
                document.body.removeChild(modal);
            }, 300);
        };
        
        modal.querySelector('.close-modal').addEventListener('click', closeModal);
        
        // Close when clicking outside the modal content
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
        
        // Character selection
        const characterCards = modal.querySelectorAll('.character-card');
        characterCards.forEach(card => {
            card.addEventListener('click', () => {
                const character = card.getAttribute('data-character');
                closeModal();
                
                // Show a loading animation
                const loadingOverlay = document.createElement('div');
                loadingOverlay.className = 'loading-overlay';
                loadingOverlay.innerHTML = `
                    <div class="loading-spinner"></div>
                    <p>Initializing ${character === 'banker' ? 'Rude Banker' : 'Humble Actor'} AI...</p>
                `;
                
                const loadingStyle = document.createElement('style');
                loadingStyle.textContent = `
                    .loading-overlay {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(0, 0, 0, 0.9);
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        z-index: 1000;
                    }
                    
                    .loading-spinner {
                        width: 50px;
                        height: 50px;
                        border: 5px solid rgba(214, 255, 133, 0.3);
                        border-radius: 50%;
                        border-top-color: var(--lime);
                        animation: spin 1s ease-in-out infinite;
                        margin-bottom: 20px;
                    }
                    
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                `;
                
                document.head.appendChild(loadingStyle);
                document.body.appendChild(loadingOverlay);
                
                // Simulate loading and then show a chat interface
                setTimeout(() => {
                    document.body.removeChild(loadingOverlay);
                    
                    // Here you would normally initialize your actual AI chat interface
                    // For demo purposes, we'll just show an alert
                    alert(`${character === 'banker' ? 'Rude Banker' : 'Humble Actor'} is ready to chat!`);
                }, 2000);
            });
        });
    });
}

// Typing effect for hero heading
function initTypingEffect() {
    const heading = document.querySelector('.hero h1');
    const originalText = heading.innerHTML;
    const highlight = heading.querySelector('.highlight');
    const highlightText = highlight.textContent;
    
    // Replace the heading content with an empty string
    heading.innerHTML = '';
    
    // Get the text before and after the highlight
    const textParts = originalText.split(`<span class="highlight">${highlightText}</span>`);
    
    let charIndex = 0;
    const textToType = textParts[0] + highlightText + textParts[1];
    
    function typeText() {
        if (charIndex < textToType.length) {
            // Check if we're at the highlight part
            if (charIndex === textParts[0].length) {
                heading.innerHTML = textParts[0] + `<span class="highlight">`;
            }
            
            // Check if we're at the end of highlight part
            if (charIndex === textParts[0].length + highlightText.length) {
                heading.innerHTML += `</span>`;
            }
            
            // Add the next character
            if (charIndex >= textParts[0].length && charIndex < textParts[0].length + highlightText.length) {
                // We're in the highlight section
                heading.querySelector('.highlight').textContent += textToType.charAt(charIndex);
            } else {
                // We're in the regular text
                heading.innerHTML += textToType.charAt(charIndex);
            }
            
            charIndex++;
            setTimeout(typeText, 50);
        }
    }
    
    // Start typing after the hero animation begins
    setTimeout(typeText, 800);
}
