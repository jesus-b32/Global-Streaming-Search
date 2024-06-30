import requests, os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

api_key = os.environ.get('API_KEY')
base_url = 'https://api.themoviedb.org/3'

# helper function for making API request and error handling
def api_request(url):
    try:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers, timeout=3)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.HTTPError as errh:
        print ("Http Error: ", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting: ", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error: ", errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong: ", err)

    return response.json()

############# Movie API calls ###############################
def movie_search(search, page):
    """Returns a list of movies based on user entered search term

    Args:
        search (str): search term for API movie search endpoint
        page (int): page number of search result

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/search/movie?query={search}&include_adult=false&language=en-US&page={page}"
    return api_request(url)


def movie_details(movie_id):
    """Returns JSON of movie detials including streaming provider data and recommendation list for that movies from TMDB API

    Args:
        movie_id (int): It is the TMDB id for a movie

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/movie/{movie_id}?append_to_response=watch%2Fproviders%2Crecommendations&language=en-US"
    return api_request(url)


def movie_provider_list():
    """Returns JSON of streaming providers for movies from TMDB API

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/watch/providers/movie?language=en-US"
    return api_request(url)
##############################################################################


############# TV show API calls #############################################
def tv_search(search, page):
    """Returns a list of tv shows based on user entered search term

    Args:
        search (str): search term for API movie search endpoint
        page (int): page number of search result

    Returns:
        _type_: JSON
    """    
    url = f"{base_url}/search/tv?query={search}&include_adult=false&language=en-US&page={page}"
    return api_request(url)


def tv_details(tv_id):
    """Returns JSON of tv show detials including streaming provider data for that tv show from TMDB API

    Args:
        tv_id (int): It is the TMDB id for a tv show

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/tv/{tv_id}?append_to_response=watch%2Fproviders%2Crecommendations"
    return api_request(url)


def tv_provider_list():
    """Returns JSON of streaming providers for tv shows from TMDB API

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/watch/providers/tv?language=en-US"
    return api_request(url)

##############################################################################



############# Discover Movie API calls ###############################
def movie_popular(page):
    """Get a list of movies ordered by popularity.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/movie/popular?page={page}"
    return api_request(url)


def movie_top_rated(page):
    """Get a list of movies ordered by rating.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """    
    url = f"{base_url}/movie/top_rated?page={page}"
    return api_request(url)


def movie_now_playing(page):
    """Get a list of movies that are currently in theatres.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """      
    url = f"{base_url}/movie/now_playing?page={page}&region=US"
    return api_request(url)


def movie_upcoming(page):
    """Get a list of movies that are being released soon.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """      
    url = f"{base_url}/movie/upcoming?page={page}&region=US"
    return api_request(url)


############# Discover TV API calls ###############################
def tv_popular(page):
    """Get a list of TV shows ordered by popularity.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """       
    url = f"{base_url}/tv/popular?page={page}"
    return api_request(url)


def tv_top_rated(page):
    """Get a list of TV shows ordered by rating.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """      
    url = f"{base_url}/tv/top_rated?page={page}"
    return api_request(url)


def tv_on_the_air(page):
    """Get a list of TV shows that air in the next 7 days.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """       
    url = f"{base_url}/tv/on_the_air?page={page}"
    return api_request(url)


def tv_airing_today(page):
    """Get a list of TV shows airing today.

    Args:
        page (int): page number of search result

    Returns:
        _type_: JSON
    """      
    url = f"{base_url}/tv/airing_today?page={page}"
    return api_request(url)




############# Watch Provider API calls ###################################
def country_list():
    """Returns JSON of countries with streaming data from TMDB API

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/watch/providers/regions?language=en-US"
    return api_request(url)

###############################################################################

############# Configuration API calls ###################################
def all_countries():
    """Returns JSON of countries (ISO 3166-1 tags) used throughout TMDB

    Returns:
        _type_: JSON
    """
    url = f"{base_url}/configuration/countries?language=en-US"
    return api_request(url)




#Helper functions for API##############################################
def get_provider_name(id, provider_data):
    """Retrieve the name of provider from TMDB using provider id

    Args:
        id (int): TMDB id
        provider_data (JSON): JSON data from movie or TV show detail API endpoint 

    Returns:
        str: return the name of provider associated with the provider ID
    """
    for provider in provider_data['results']:
        if provider['provider_id'] == id:
            return provider['provider_name']
        
        
def get_video_detail(tmdb_id, media_type):
    """Return details of a movie or TV show based on TMDB id

    Args:
        tmdb_id (int): TMDB ID for movie or TV show
        media_type (str): Can be 'movie' or 'tv'

    Returns:
        JSON: JSON data from movie or TV show detail TMDB API endpoint
    """
    if media_type == 'movie':
        return movie_details(tmdb_id)
    return tv_details(tmdb_id)