import cv2
import numpy as np
from utils.images import get_images_in_directory, load_image, load_metadata

dir = "dataset/geotagged"

class GeoAlign:
    def __init__(self, dir):
        self.images = get_images_in_directory(dir)
    
    def align_images(self):
        # Load images and their metadata
        image_data = []
        for image_path in self.images:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                return None
            metadata = load_metadata(image_path)
            if 'GPS' not in metadata:
                print(f"Image {image_path} does not have GPS metadata.")
                return None
            image_data.append((image, metadata['GPS']))
        
        if len(image_data) < 2:
            print("Insufficient images with GPS data for stitching.")
            return None
        
        # Find the bounding box for all images based on their GPS coordinates
        min_lat = min(img[1]['latitude'] for img in image_data)
        max_lat = max(img[1]['latitude'] for img in image_data)
        min_lon = min(img[1]['longitude'] for img in image_data)
        max_lon = max(img[1]['longitude'] for img in image_data)
        
        # Calculate the canvas size based on the GPS coordinates
        scale_factor = 200000
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon
        max_height = max(image.shape[0] for image, _ in image_data)
        max_width = max(image.shape[1] for image, _ in image_data)
        canvas_height = int(lat_range * scale_factor) + max_height
        canvas_width = int(lon_range * scale_factor) + max_width
        canvas_size = (canvas_height, canvas_width, 3)
        canvas = np.zeros(canvas_size, dtype=np.uint8)
        
        # Place each image on the canvas based on its GPS coordinates
        for image, metadata in image_data:
            lat_offset = int((metadata['latitude'] - min_lat) * scale_factor)
            lon_offset = int((metadata['longitude'] - min_lon) * scale_factor)
            h, w, _ = image.shape
            if lat_offset + h <= canvas_height and lon_offset + w <= canvas_width:
                canvas[lat_offset:lat_offset + h, lon_offset:lon_offset + w] = image
            else:
                print(f"Image {image_path} exceeds canvas size and cannot be placed.")
        
        # Use the Stitcher to stitch the canvas images
        stitcher = cv2.Stitcher_create()
        # status, stitched = stitcher.stitch([canvas])
        status, stitched = stitcher.stitch([image_data[0]])
        
        if status == cv2.Stitcher_OK:
            cv2.imwrite('stitched_output.jpg', stitched)
            print("Stitching completed and saved as 'stitched_output.jpg'")
        else:
            print(f"Error during stitching: {status}")

# Initialize and run the stitching process
geo_align = GeoAlign(dir)
geo_align.align_images()
