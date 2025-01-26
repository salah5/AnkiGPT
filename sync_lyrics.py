import os
import syncedlyrics

# Directory containing your MP3 files
mp3_directory = "."

# Directory to save the .lrc files
output_directory = "."
os.makedirs(output_directory, exist_ok=True)  # Create the output directory if it doesn't exist

def extract_track_and_artist(filename):
    """
    Extracts the track and artist name from a filename formatted as 'TrackName - ArtistName.mp3'.
    Adjust this function if the filename structure is different.
    """
    if "-" in filename:
        parts = filename.rsplit("-", 1)
        track = parts[0].strip()
        artist = parts[1].replace(".mp3", "").strip()
        return track, artist
    return None, None

def save_lyrics_to_file(track, artist, lyrics, output_path):
    """
    Save lyrics to a .lrc file.
    """
    filename = f"{track} - {artist}.lrc"
    filepath = os.path.join(output_path, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(lyrics)
    print(f"Lyrics saved: {filepath}")

def generate_lyrics_for_directory(mp3_dir, output_dir):
    """
    Process each .mp3 file in the directory and generate corresponding .lrc files.
    """
    for file in os.listdir(mp3_dir):
        if file.endswith(".mp3"):
            track, artist = extract_track_and_artist(file)
            if track and artist:
                print(f"Searching lyrics for: {track} by {artist}")
                try:
                    lrc = syncedlyrics.search(f"{track} {artist}")
                    if lrc:
                        save_lyrics_to_file(track, artist, lrc, output_dir)
                    else:
                        print(f"No lyrics found for: {track} by {artist}")
                except Exception as e:
                    print(f"Error fetching lyrics for {track} by {artist}: {e}")
            else:
                print(f"Invalid file name format: {file}")

if __name__ == "__main__":
    generate_lyrics_for_directory(mp3_directory, output_directory)
