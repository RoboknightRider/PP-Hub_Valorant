# utils.py
import requests
import hashlib
import bencodepy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from django.http import JsonResponse
import json

def get_peers_count(torrent_hash):
    """
    Fetch the number of seeders and leechers for a given torrent hash from an HTTP tracker.
    """
    tracker_url = f'http://tracker.opentrackr.org:1337/announce?info_hash={torrent_hash}'
    
    try:
        # Send a GET request to the tracker
        response = requests.get(tracker_url, timeout=10)
        if response.status_code == 200:
            # Parse the response (if the tracker returns structured data)
            # This is a placeholder; actual parsing depends on the tracker's response format
            data = response.json()  # Replace with appropriate parsing logic
            seeders = data.get("seeders", 0)
            leechers = data.get("leechers", 0)
            return seeders, leechers
        else:
            print(f"Tracker returned status code {response.status_code}")
            return 0, 0
    except requests.RequestException as e:
        print(f"Error fetching peers count: {e}")
        return 0, 0

def calculate_torrent_hash(torrent_file_path):
    try:
        with open(torrent_file_path, 'rb') as f:
            torrent_data = bencodepy.decode(f.read())
            info = torrent_data[b'info']
            info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()
            return info_hash
    except Exception as e:
        print(f"Error calculating torrent hash: {e}")
        return None
    
@login_required
def get_messages(request):
    messages = ChatMessage.objects.order_by('timestamp').values('user__username', 'message', 'timestamp')
    return JsonResponse(list(messages), safe=False)

# Save chat message
@csrf_exempt
@login_required
def save_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                ChatMessage.objects.create(user=request.user, message=message)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Message is empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)  