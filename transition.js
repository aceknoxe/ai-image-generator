document.addEventListener('DOMContentLoaded', () => {
    // Reset scroll position
    window.scrollTo(0, 0);
    
    // Add transition class when page loads
    document.body.classList.add('page-transition');

    // Handle navigation links
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            // Start exit animation
            const container = document.querySelector('.container');
            container.style.opacity = '0';
            
            // Navigate after animation and reset scroll
            setTimeout(() => {
                window.scrollTo(0, 0);
                window.location.href = target;
            }, 300);
        });
    });
}); 