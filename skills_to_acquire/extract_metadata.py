from pymediainfo import MediaInfo

def extract_mkv_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    duration = None

    for track in media_info.tracks:
        if track.track_type == 'General':
            duration = track.duration
            print(duration/3600)
        elif track.track_type == 'Audio':
            print(f"Audio Track: {track.title} (Language: {track.other_language})")
        elif track.track_type == 'Text':
            print(f"Subtitle Track: {track.title} (Language: {track.other_language})")

    print(duration)
    if duration:
        print("duration is a bool")
    if duration:
        print(f"Duration: {duration}")

def convert_milliseconds(milliseconds):
    # Calculate total seconds
    total_seconds = milliseconds // 1000

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds

# Example usage
duration_ms = 4509576
hours, minutes, seconds = convert_milliseconds(duration_ms)
print(f"Duration: {hours}h {minutes}mn {seconds}s")


# Example usage
file_path = "C:\\colin_films\\TIME_MASTERS\\time_masters.mkv"
extract_mkv_metadata(file_path)
