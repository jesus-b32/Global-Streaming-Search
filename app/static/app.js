// JS script using Tom Select Plugin for selecting country or providers in detail page
new TomSelect('#country', {
    maxOptions: null,
    sortField: {
        field: "text",
        direction: "asc"
    }
});

new TomSelect('#streamingProvider', {
    maxOptions: null,
    sortField: {
        field: "text",
        direction: "asc"
    }
});

// Enabling tootips for bootstrap
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


//toggeling the display of streaming data by country or provider
const visibility_selection = document.querySelector('#visibility_selection');
const country_section = document.querySelector('#country_section');
const provider_section = document.querySelector('#provider_section');
const country_checked = document.getElementById('country_view');
const provider_checked = document.getElementById('provider_view');

function streaming_data_display(e) {
    console.log(e.target);
    if (e.target === country_checked) {
        console.log('Inside country section');
        provider_section.classList.add('d-none');
        country_section.classList.remove('d-none');
    } else if(e.target === provider_checked) {
        console.log('Inside country section');
        provider_section.classList.remove('d-none');
        country_section.classList.add('d-none');    
    }
}

visibility_selection.addEventListener('click', streaming_data_display);

