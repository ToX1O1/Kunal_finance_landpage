document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const nav = document.querySelector('.navbar-inner nav');
    const navLinks = document.querySelector('.nav-links'); // use class selector

    if (!menuToggle || !nav) return;

    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('open');
        const icon = menuToggle.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        }
    });

    // Close menu when a link is clicked (for mobile)
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('open');
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            });
        });
    }

    // --- 2. Modal/Join Us Functionality ---
    const modal = document.getElementById('leadModal');
    const modalTriggers = document.querySelectorAll('.modal-trigger');
    const modalClose = modal.querySelector('.modal-close');
    const modalBackdrop = modal.querySelector('.modal-backdrop');

    // Function to open the modal
    const openModal = () => {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
    };

    // Function to close the modal
    const closeModal = () => {
        modal.classList.remove('open');
        document.body.style.overflow = ''; // Restore scrolling
    };

    // Attach event listeners to all modal-trigger buttons (Hero & CTA Banner)
    modalTriggers.forEach(button => {
        button.addEventListener('click', openModal);
    });

    // Close modal via the 'X' button
    modalClose.addEventListener('click', closeModal);

    // Close modal by clicking the backdrop
    modalBackdrop.addEventListener('click', closeModal);

    // Close modal via Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('open')) {
            closeModal();
        }
    });

    // Handle form submission (prevent default and provide success message)
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
        leadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Show a simple success message inside the modal (instead of alert)
            const modalContent = modal.querySelector('.modal-content');
            modalContent.innerHTML = `
                <button class="modal-close">&times;</button>
                <div class="modal-header">
                    <h3>Success! 🎉</h3>
                    <p>Thank you for joining us! We've received your request and will contact you shortly to activate your free trial access.</p>
                </div>
                <button class="btn btn-primary w-full mt-5" onclick="window.location.reload()">Return to Site</button>
            `;
            // Reattach close functionality to the new close button
            modalContent.querySelector('.modal-close').addEventListener('click', closeModal);
            // After 5 seconds, close the modal automatically
            setTimeout(closeModal, 5000);
        });
    }

    // --- 3. Chart.js Initialization (Mock Trading Chart) ---
    const ctx = document.getElementById('heroChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['9:15', '10:00', '10:45', '11:30', '12:15', '13:00', '13:45', '14:30', '15:15'],
                datasets: [{
                    label: 'BANKNIFTY Price',
                    data: [47800, 48050, 47900, 48200, 48150, 48350, 48300, 48500, 48450],
                    borderColor: '#00f2fe',
                    backgroundColor: 'rgba(0, 242, 254, 0.2)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 3,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { mode: 'index', intersect: false }
                },
                scales: {
                    x: { 
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'white' }
                    },
                    y: {
                        beginAtZero: false,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'white' }
                    }
                }
            }
        });
    }
    
    // --- 4. Dynamic Year Update ---
    document.getElementById('year').textContent = new Date().getFullYear();

    // --- 5. Fade-Up Scroll Animation ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1, // Trigger when 10% of the element is visible
    });

    document.querySelectorAll('.fade-up').forEach(element => {
        observer.observe(element);
    });
});