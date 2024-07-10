import exifread
import cv2
import os


def load_image(path: str) -> cv2.typing.MatLike:
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def load_metadata(path: str) -> dict:
    with open(path, 'rb') as f:
        tags = exifread.process_file(f)

    metadata = {}
    gps_info = {}

    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        lat = tags['GPS GPSLatitude']
        lon = tags['GPS GPSLongitude']

        lat_values = [float(x.num) / float(x.den) for x in lat.values]
        lon_values = [float(x.num) / float(x.den) for x in lon.values]

        lat_ref = tags['GPS GPSLatitudeRef'].values
        lon_ref = tags['GPS GPSLongitudeRef'].values

        latitude = lat_values[0] + lat_values[1] / 60 + lat_values[2] / 3600
        if lat_ref != 'N':
            latitude = -latitude

        longitude = lon_values[0] + lon_values[1] / 60 + lon_values[2] / 3600
        if lon_ref != 'E':
            longitude = -longitude

        gps_info['latitude'] = latitude
        gps_info['longitude'] = longitude

    if gps_info:
        metadata['GPS'] = gps_info

    for tag in tags.keys():
        metadata[tag] = tags[tag]

    return metadata


def get_images_in_directory(directory: str, extensions: list[str] = ['.dng', '.jpg', '.jpeg', '.png']) -> list[str]:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' not found.")
    
    images = []
    for file in os.listdir(directory):
        if file.lower().endswith(tuple(extensions)):
            images.append(os.path.join(directory, file))
    return images
