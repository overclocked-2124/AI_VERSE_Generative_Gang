// Particle.js configuration for animated background
document.addEventListener('DOMContentLoaded', function() {
    // Initialize particles
    if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#667eea" },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: false },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#667eea",
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: "none",
                    random: false,
                    straight: false,
                    out_mode: "out",
                    bounce: false
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "grab" },
                    onclick: { enable: true, mode: "push" },
                    resize: true
                },
                modes: {
                    grab: { distance: 140, line_linked: { opacity: 1 } },
                    push: { particles_nb: 4 }
                }
            },
            retina_detect: true
        });
    }

    // Typing animation for the heading
    const title = document.querySelector('.typing-effect');
    const text = title.textContent;
    title.textContent = '';
    let i = 0;
    
    function typeWriter() {
        if (i < text.length) {
            title.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    
    setTimeout(typeWriter, 500);
    
    // Form submit animation
    const form = document.getElementById('modelForm');
    const submitBtn = document.getElementById('submitBtn');
    const notification = document.getElementById('notification');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Add loading animation
        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').textContent = 'Processing...';
        submitBtn.querySelector('.btn-icon i').classList.remove('fa-cog');
        submitBtn.querySelector('.btn-icon i').classList.add('fa-spinner', 'fa-spin');
        
        // Simulate processing (replace with actual form submission)
        setTimeout(function() {
            // Submit the form
            form.submit();
            
            // Show notification
            notification.classList.add('show');
            
            // Hide notification after 3 seconds
            setTimeout(function() {
                notification.classList.remove('show');
            }, 3000);
        }, 1500);
    });
    
    // Custom select animation
    const select = document.getElementById('model');
    select.addEventListener('change', function() {
        updateModelDetail(this.value);
    });
    
    function updateModelDetail(model) {
        const modelDetail = document.getElementById('modelDetail');
        modelDetail.classList.add('update');
        
        setTimeout(function() {
            document.querySelector('.current-model').textContent = model;
            document.querySelector('.model-detail h3').textContent = model;
            
            // Different descriptions based on model
            let description = "An advanced AI language model ready to assist you.";
            if (model.includes('llama')) {
                description = "A powerful open-source model from Meta AI with strong reasoning abilities.";
            } else if (model.includes('gemma')) {
                description = "Google's lightweight and efficient conversational AI model.";
            } else if (model.includes('mistral')) {
                description = "An expertly trained model with excellent natural language understanding.";
            } else if (model.includes('phi3')) {
                description = "Microsoft's compact and efficient model with remarkable capabilities.";
            }
            
            document.querySelector('.model-description').textContent = description;
            modelDetail.classList.remove('update');
        }, 300);
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    let darkMode = false;
    
    themeToggle.addEventListener('click', function() {
        darkMode = !darkMode;
        if (darkMode) {
            document.body.classList.add('dark-theme');
            themeToggle.querySelector('i').classList.remove('fa-moon');
            themeToggle.querySelector('i').classList.add('fa-sun');
        } else {
            document.body.classList.remove('dark-theme');
            themeToggle.querySelector('i').classList.remove('fa-sun');
            themeToggle.querySelector('i').classList.add('fa-moon');
        }
    });
    
    // Logo animation
    const logo = document.querySelector('.logo-animation');
    setInterval(function() {
        logo.classList.add('pulse');
        setTimeout(function() {
            logo.classList.remove('pulse');
        }, 1000);
    }, 3000);
    
    // Button hover effects
    submitBtn.addEventListener('mouseenter', function() {
        this.querySelector('.btn-icon i').classList.add('fa-spin');
    });
    
    submitBtn.addEventListener('mouseleave', function() {
        this.querySelector('.btn-icon i').classList.remove('fa-spin');
    });
});
