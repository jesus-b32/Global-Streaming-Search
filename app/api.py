import requests


############# Movie API calls ###############################
def movie_search(search):
    url = f"https://api.themoviedb.org/3/search/movie?query={search}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def movie_details(movie_id):
    """Returns JSON of movie detials including streaming provider data for that movies from TMDB API

    Returns:
        _type_: JSON
    """
    # url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=watch%2Fproviders&language=en-US"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=watch%2Fproviders%2Crecommendations&language=en-US"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    response = requests.get(url, headers=headers)
    return response.json() 


def movie_provider_list():
    """Returns JSON of streaming providers for movies from TMDB API

    Returns:
        _type_: JSON
    """
    url = "https://api.themoviedb.org/3/watch/providers/movie?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }

    response = requests.get(url, headers=headers)
    return response.json()    
##############################################################################


############# TV show API calls #############################################
def tv_search(search):
    url = f"https://api.themoviedb.org/3/search/tv?query={search}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    
    # tv shows request
    response = requests.get(url, headers=headers)
    return response.json()

def tv_details(tv_id):
    """Returns JSON of movie detials including streaming provider data for that movies from TMDB API

    Returns:
        _type_: JSON
    """
    # url = f"https://api.themoviedb.org/3/tv/{tv_id}?append_to_response=watch%2Fproviders&language=en-US"
    
    url = f"https://api.themoviedb.org/3/tv/{tv_id}?append_to_response=watch%2Fproviders%2Crecommendations"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    response = requests.get(url, headers=headers)
    return response.json() 


def tv_provider_list():
    """Returns JSON of streaming providers for movies from TMDB API

    Returns:
        _type_: JSON
    """
    url = "https://api.themoviedb.org/3/watch/providers/tv?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }

    response = requests.get(url, headers=headers)
    return response.json()    
##############################################################################




############# Watch Provider API calls ###################################
def country_list():
    """Returns JSON of countries with streaming data from TMDB API

    Returns:
        _type_: JSON
    """
    url = "https://api.themoviedb.org/3/watch/providers/regions?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    response = requests.get(url, headers=headers)
    return response.json()    


############# Configuration API calls ###################################
def all_countries():
    """Returns JSON of countries (ISO 3166-1 tags) used throughout TMDB

    Returns:
        _type_: JSON
    """
    url = "https://api.themoviedb.org/3/configuration/countries?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }

    response = requests.get(url, headers=headers)
    return response.json()


#Helper functions for API##############################################
def get_provider_name(id, provider_data):
    for provider in provider_data['results']:
        if provider['provider_id'] == id:
            return provider['provider_name']
        
        
def get_video_detail(tmdb_id, media_type):
    if media_type == 'movie':
        return movie_details(tmdb_id)
    return tv_details(tmdb_id)
            
