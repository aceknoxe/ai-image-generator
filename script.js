document.addEventListener('DOMContentLoaded', () => {
    // Menu toggle functionality
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = menuToggle.querySelector('i');
        if (navLinks.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-links') && !e.target.closest('.menu-toggle')) {
            navLinks.classList.remove('active');
            const icon = menuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Grab references for cat generation
    const catImg = document.getElementById('cat-img');
    const generateBtn = document.getElementById('generate-btn');
    const catContainer = document.querySelector('.cat-container');

    // Create and append loader (if you actually have .cat-container in HTML)
    if (catContainer) {
        const loader = document.createElement('div');
        loader.className = 'loader';
        loader.innerHTML = `
            <div></div>
            <div></div>
            <div></div>
        `;
        catContainer.appendChild(loader);
    }

    // Function to fetch random cat image
    async function generateCat() {
        try {
            if (catContainer) {
                catContainer.querySelector('.loader').style.display = 'block';
            }
            const response = await fetch('https://api.thecatapi.com/v1/images/search');
            const data = await response.json();
            if (catImg) {
                catImg.src = data[0].url;
            }
        } catch (error) {
            console.error('Error fetching cat image:', error);
        } finally {
            if (catContainer) {
                catContainer.querySelector('.loader').style.display = 'none';
            }
        }
    }

    // Single generateImage function for prompt-based AI images
    async function generateImage() {
        const promptInput = document.getElementById('prompt-input');
        const imageDisplay = document.getElementById('generated-img');

        if (!promptInput || !promptInput.value) {
            alert('Please enter a prompt');
            return;
        }

        try {
            if (generateBtn) {
                generateBtn.disabled = true;
                generateBtn.textContent = 'Generating...';
            }

            const response = await fetch('http://localhost:5000/api/images', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: promptInput.value })
            });

            if (!response.ok) {
                throw new Error(`Failed to generate image (status: ${response.status})`);
            }

            const data = await response.json();
            if (imageDisplay) {
                imageDisplay.src = data.imageUrl;
                imageDisplay.style.display = 'block';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate image. Please try again.');
        } finally {
            if (generateBtn) {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate';
            }
        }
    }

    // Attach event listeners only if the targeted elements exist
    if (generateBtn) {
        generateBtn.addEventListener('click', () => {
            // If you want to generate cat images, call generateCat()
            // otherwise, call generateImage() for AI images.
            generateImage();
        });
    }
});