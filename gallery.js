// gallery.js
const API_URL = 'https://ai-image-generator-r93p.onrender.com';

document.addEventListener('DOMContentLoaded', async function() {
    const galleryGrid = document.getElementById('gallery-grid');
    
    try {
        const response = await fetch(`${API_URL}/api/images`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        const images = await response.json();
        
        if (images.length === 0) {
            galleryGrid.innerHTML = `
                <div class="no-images">
                    <p>No images generated yet. Go to the Create page to generate some!</p>
                </div>
            `;
            return;
        }
        
        galleryGrid.innerHTML = '';
        
        images.forEach(item => {
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';
            
            galleryItem.innerHTML = `
                <img src="${item.imageUrl}" alt="${item.prompt}" class="gallery-image">
                <div class="gallery-content">
                    <p class="gallery-prompt">${item.prompt || 'No prompt provided'}</p>
                    <p class="gallery-date">${new Date(item.createdAt).toLocaleDateString()}</p>
                </div>
            `;
            
            galleryGrid.appendChild(galleryItem);
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
        galleryGrid.innerHTML = `
            <div class="error">
                <p>Failed to load images. Please try again later.</p>
            </div>
        `;
    }
});