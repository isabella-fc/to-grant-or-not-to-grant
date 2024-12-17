document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('prediction-form');
    const overlay = document.getElementById('loading-overlay');
    const resultSection = document.getElementById('result-section');

    // Show overlay on form submit
    if (form) {
        form.addEventListener('submit', function () {
            overlay.style.display = 'flex'; // Show the loading overlay
        });
    }

    // Scroll to result section if it exists
    if (resultSection) {
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.searchable-dropdown');

    if (dropdown) {
        // Create a wrapper for styling consistency
        const wrapper = document.createElement('div');
        wrapper.classList.add('dropdown-wrapper');
        dropdown.parentNode.insertBefore(wrapper, dropdown);
        wrapper.appendChild(dropdown);

        // Add a search input field above the dropdown
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.classList.add('dropdown-search');
        searchInput.placeholder = 'Search...';
        wrapper.insertBefore(searchInput, dropdown);

        // Filter options based on input
        searchInput.addEventListener('input', function () {
            const filter = this.value.toLowerCase();
            const options = dropdown.options;

            for (let i = 0; i < options.length; i++) {
                const optionText = options[i].text.toLowerCase();
                options[i].style.display = optionText.includes(filter) ? 'block' : 'none';
            }
        });
    }
});