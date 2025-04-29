// Initialize AOS
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true,
    mirror: false
});

// Navbar Scroll Effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.padding = '0.5rem 0';
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
    } else {
        navbar.style.padding = '1rem 0';
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    }
});

// Active Navigation Link
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
        
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLink?.classList.add('active');
        } else {
            navLink?.classList.remove('active');
        }
    });
});

// Form Validation
const form = document.getElementById('enrollmentForm');
if (form) {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            event.preventDefault();
            // Show success message
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Success!';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('enrollmentModal'));
                modal.hide();
                // Reset form
                form.reset();
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        }
        form.classList.add('was-validated');
    });
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Counter Animation
function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 20);
}

// Initialize counters when they come into view
const counterElements = document.querySelectorAll('.hero-stats h3');
const observerOptions = {
    threshold: 1,
    rootMargin: '0px'
};

const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.textContent);
            animateCounter(entry.target, target);
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

counterElements.forEach(counter => {
    counterObserver.observe(counter);
});

// Floating Cards Animation
const cards = document.querySelectorAll('.floating-card');
cards.forEach(card => {
    let yPosition = 0;
    let yDirection = 1;
    
    function animate() {
        yPosition += 0.3 * yDirection;
        if (yPosition >= 10) yDirection = -1;
        if (yPosition <= -10) yDirection = 1;
        
        card.style.transform = `translateY(${yPosition}px)`;
        requestAnimationFrame(animate);
    }
    
    animate();
});

// Roadmap Path Switching
document.addEventListener('DOMContentLoaded', function() {
    const roadmapFilters = document.querySelectorAll('.roadmap-filters .btn');
    const roadmapPaths = document.querySelectorAll('.roadmap-path');

    roadmapFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            // Remove active class from all filters
            roadmapFilters.forEach(f => f.classList.remove('active'));
            // Add active class to clicked filter
            this.classList.add('active');

            // Hide all paths
            roadmapPaths.forEach(path => {
                path.style.display = 'none';
                path.classList.remove('active');
            });

            // Show selected path
            const selectedPath = document.getElementById(`${this.dataset.path}-path`);
            if (selectedPath) {
                selectedPath.style.display = 'block';
                setTimeout(() => {
                    selectedPath.classList.add('active');
                }, 50);

                // Animate cards
                const cards = selectedPath.querySelectorAll('.roadmap-card');
                cards.forEach((card, index) => {
                    card.style.animationDelay = `${index * 100}ms`;
                });
            }
        });
    });

    // Initialize progress indicators
    const progressBars = document.querySelectorAll('.progress-indicator');
    progressBars.forEach(bar => {
        const progress = bar.dataset.progress || '0';
        bar.style.setProperty('--progress', `${progress}%`);
    });
});

// Add hover effect to roadmap cards
const roadmapCards = document.querySelectorAll('.roadmap-card');
roadmapCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});
