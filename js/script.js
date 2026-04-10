// ===========================
// Cart Management
// ===========================

let cart = [];

function addToCart(productName, price) {
    const existingItem = cart.find(item => item.name === productName);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    updateCartCount();
    showNotification(`${productName} added to cart!`);
}

function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelector('.cart-count').innerText = totalItems;
    localStorage.setItem('cart', JSON.stringify(cart));
}

function showCart() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    let cartSummary = 'FINE JEWELS - CART SUMMARY\n===========================\n\n';
    let total = 0;
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        cartSummary += `${index + 1}. ${item.name}\n`;
        cartSummary += `   Quantity: ${item.quantity}\n`;
        cartSummary += `   Price: ₹${item.price.toLocaleString('en-IN')}\n`;
        cartSummary += `   Total: ₹${itemTotal.toLocaleString('en-IN')}\n\n`;
    });
    
    cartSummary += '===========================\n';
    cartSummary += `GRAND TOTAL: ₹${total.toLocaleString('en-IN')}\n`;
    cartSummary += '===========================\n\n';
    cartSummary += 'Contact us for checkout and delivery details!\n';
    cartSummary += 'Phone: +1 (555) 123-4567\n';
    cartSummary += 'Email: info@finejewels.com';
    
    alert(cartSummary);
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerText = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: #4caf50;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 2000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ===========================
// Product Filtering
// ===========================

function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter products
    products.forEach(product => {
        if (category === 'all' || product.getAttribute('data-category') === category) {
            product.style.display = 'block';
            product.style.animation = 'fadeInUp 0.5s ease';
        } else {
            product.style.display = 'none';
        }
    });
}

// ===========================
// Navigation
// ===========================

const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Toggle mobile menu
if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close mobile menu when a link is clicked
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        navMenu.classList.remove('active');
        hamburger?.classList.remove('active');
        
        // Update active link
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Update active link based on scroll position
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// ===========================
// Form Handling
// ===========================

function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Simulate form submission
    console.log('Form submitted:', Object.fromEntries(formData));
    
    showNotification('Thank you! We will contact you soon.');
    form.reset();
}

function handleNewsletterSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = form.querySelector('input[type="email"]').value;
    
    console.log('Newsletter subscription:', email);
    showNotification('Thank you for subscribing!');
    form.reset();
}

// ===========================
// Load Cart from Storage
// ===========================

window.addEventListener('load', () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartCount();
    }
});

// ===========================
// Smooth Scroll Animation
// ===========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#home') {
            // Handled by browser's smooth scroll
        }
    });
});

// ===========================
// Add animations when elements come into view
// ===========================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all product cards and collection cards
document.querySelectorAll('.product-card, .collection-card, .stat').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
});

// ===========================
// Add keyframe animations dynamically
// ===========================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .hamburger.active span:nth-child(1) {
        transform: rotate(-45deg) translate(-5px, 6px);
    }
    
    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger.active span:nth-child(3) {
        transform: rotate(45deg) translate(-5px, -6px);
    }
`;
document.head.appendChild(style);

// ===========================
// Enhanced Shop Now Button
// ===========================

const shopNowBtn = document.querySelector('.hero .btn-primary');
if (shopNowBtn) {
    shopNowBtn.addEventListener('click', () => {
        document.querySelector('#collections').scrollIntoView({ behavior: 'smooth' });
    });
}

// ===========================
// Explore Buttons
// ===========================

document.querySelectorAll('.collection-card .btn-secondary').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelector('#featured-products, .featured-products').scrollIntoView({ behavior: 'smooth' });
        showNotification('Check out our featured collection!');
    });
});

// ===========================
// Initialize on page load
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Fine Jewels website loaded successfully!');
    
    // Highlight active nav link on page load
    const hash = window.location.hash.slice(1) || 'home';
    const activeLink = document.querySelector(`.nav-link[href="#${hash}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
});
