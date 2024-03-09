import requests


def get_movie_poster(url):
    base_url = "https://image.tmdb.org/t/p/original"
    try:
        image_url = f"{base_url}{url}"
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        return None
