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
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));


/** Add movie or TV show to watchlist user clicks on add to watchlist button.
 *  Submit a POST request.
 *  Update button to signify movie or TV show already in watchlist
 *  */
async function addToWatchlist (e) {
    e.preventDefault();

    if(!(e.target.classList.contains('watchlist_add'))) {
        return
    }

    // get tmdb_id and media_type from data attribute in title header
    const tmdbId = document.querySelector('.video_title').dataset.tmdbId;
    const mediaType = document.querySelector('.video_title').dataset.mediaType;

    await fetch('/watchlist/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify({
            tmdb_id: tmdbId,
            media_type: mediaType
        })
    })
    //remove class and add new one to update the look of button and bookmark 
    e.target.classList.remove('btn-primary');
    e.target.firstElementChild.classList.remove('fa-regular');

    e.target.classList.add('btn-danger');
    e.target.firstElementChild.classList.add('fa-solid');
}
const addBtn = document.querySelector('.watchlist_add');

// Only run eventlistener if add button exist
if (addBtn) {
    addBtn.addEventListener('click', addToWatchlist);
}

///////////////////////////////////////////////////////////////////////////////////


/** Remove movie or TV show to watchlist user clicks on add to watchlist button.
 *  Submit a POST request.
 *  Update button to signify movie or TV show is no longer in watchlist
 *  */
async function removeFromWatchlist (e) {
    e.preventDefault();

    if(!(e.target.classList.contains('watchlist_remove'))) {
        return
    }

    // get tmdb_id and media_type from data attribute in title header
    const tmdbId = document.querySelector('.video_title').dataset.tmdbId;
    const mediaType = document.querySelector('.video_title').dataset.mediaType;

    await fetch('/watchlist/remove', {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify({
            tmdb_id: tmdbId,
            media_type: mediaType
        })
    })

    //remove class and add new one to update the look of button and bookmark 
    e.target.classList.remove('btn-danger');
    console.log('target: ', e.target);
    e.target.firstElementChild.classList.remove('fa-solid');

    e.target.classList.add('btn-primary');
    e.target.firstElementChild.classList.add('fa-regular');
}
const removeBtn = document.querySelector('.watchlist_remove');

// Only run eventlistener if remove button exist
if (removeBtn) {
    removeBtn.addEventListener('click', removeFromWatchlist);
}

///////////////////////////////////////////////////////////////////////////////////


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

