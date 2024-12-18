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

document.addEventListener('DOMContentLoaded', function () {
    const zipInput = document.getElementById('id_zip_code');
    const encodedField = document.getElementById('encoded_value');
    const dataListOptions = document.querySelectorAll('#zip_codes option');

    zipInput.addEventListener('input', function () {
        const selectedValue = zipInput.value.trim();
        encodedField.value = ''; // Reset hidden field

        // Find the matching option and set the encoded value
        const matchedOption = Array.from(dataListOptions).find(option => option.value === selectedValue);
        if (matchedOption) {
            console.log("Matched Zip:", matchedOption.value);
            console.log("Encoded Value:", matchedOption.dataset.encodedValue);
            encodedField.value = matchedOption.dataset.encodedValue;
        } else {
            console.log("No match found for:", selectedValue);
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const carrierInput = document.getElementById('id_carrier_name');
    const encodedField = document.getElementById('encoded_value_carrier');
    const dataListOptions = document.querySelectorAll('#carrier_names option');

    carrierInput.addEventListener('input', function () {
        const selectedValue = carrierInput.value;
        encodedField.value = ''; // Reset hidden field

        // Find the matching option and set the encoded value
        const matchedOption = Array.from(dataListOptions).find(option => option.value === selectedValue);
        if (matchedOption) {
            console.log("Matched Carrier:", matchedOption.value);
            console.log("Encoded Value:", matchedOption.dataset.encodedValue);
            encodedField.value = matchedOption.dataset.encodedValue; // Correct dataset reference
        }
    });
});