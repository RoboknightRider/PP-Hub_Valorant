# utils.py
import os
from django.conf import settings

def generate_torrent_and_magnet(uploaded_file_instance):
    """
    Fallback function to generate a dummy torrent file and magnet link.
    This does not produce a valid torrent file but creates placeholders.
    """
    # Use a public tracker URL (or any default)
    public_tracker = "udp://tracker.opentrackr.org:1337/announce"
    
    # Determine the base filename (without extension)
    base_filename = os.path.splitext(os.path.basename(uploaded_file_instance.file.name))[0]
    
    # Create a torrent file name and path under MEDIA_ROOT/torrents
    torrent_file_name = f"{base_filename}.torrent"
    torrent_file_relative_path = f"torrents/{torrent_file_name}"
    torrent_file_path = os.path.join(settings.MEDIA_ROOT, torrent_file_relative_path)
    
    # Ensure the torrents directory exists
    os.makedirs(os.path.dirname(torrent_file_path), exist_ok=True)
    
    # Write a placeholder content into the torrent file
    with open(torrent_file_path, 'w') as torrent_file:
        torrent_file.write("This is a placeholder torrent file. Replace with a valid torrent file generation later.")
    
    # Create a dummy torrent hash (in real cases you would generate a real hash)
    dummy_hash = "abcdef1234567890abcdef1234567890abcdef12"
    
    # Build a simple dummy magnet link
    magnet_link = (f"magnet:?xt=urn:btih:{dummy_hash}"
                   f"&dn={uploaded_file_instance.name}"
                   f"&tr={public_tracker}")
    
    # Update the UploadedFile instance with our placeholder torrent information
    uploaded_file_instance.torrent_file.name = torrent_file_relative_path
    uploaded_file_instance.magnet_link = magnet_link
    uploaded_file_instance.save()
