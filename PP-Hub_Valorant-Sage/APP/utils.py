# utils.py
import requests

def get_seeder_count(torrent_hash):
    """
    Fetch the number of seeders for a given torrent hash from a tracker.
    """
    tracker_url = f'udp://tracker.opentrackr.org:1337/announce?info_hash={torrent_hash}'
    
    try:
        response = requests.get(tracker_url)
        if response.status_code == 200:
            data = response.json()  # Assuming the tracker returns JSON data
            return data.get("seeders", 0)
        else:
            return 0
    except requests.RequestException as e:
        print(f"Error fetching seeder count: {e}")
        return 0
