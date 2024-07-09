import numpy
from constants import RESULTS_DIR, DATASET_DIR
from utils.images import get_images_in_directory, load_metadata
import cv2
import rawpy


class GeoAlignerBaseException(Exception):
    def __init__(self, message="Error in GeoAligner class."):
        self.message = message
        super().__init__(self.message)


class InsufficientGpsImagesException(GeoAlignerBaseException):
    def __init__(self, message="Insufficient images with GPS data for stitching."):
        self.message = message
        super().__init__(self.message)


class ReadDngFileException(GeoAlignerBaseException):
    def __init__(self, message="Could not read .dng file."):
        self.message = message
        super().__init__(self.message)


class CreateStitchedMapException(GeoAlignerBaseException):
    def __init__(self, message="Could not create stitched map."):
        self.message = message
        super().__init__(self.message)


class GeoAligner:
    def __init__(self, images_dir: str):
        self.result_filename = images_dir.replace(f"{DATASET_DIR}/", "")
        self.images = get_images_in_directory(images_dir)
        self.image_data = self.get_image_data()

    def get_image_data(self) -> list:
        """Read images and return list."""

        image_data = []
        for image_path in self.images:
            # Only .dng files supported
            if image_path.lower().endswith('.dng'):
                try:
                    image = self.read_dng(image_path)
                except ReadDngFileException as e:
                    print(e.message)
                    continue

            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            metadata = load_metadata(image_path)
            if 'GPS' not in metadata:
                print(f"Image {image_path} does not have GPS metadata.")
                continue

            image_data.append((image, metadata['GPS']))

        if len(image_data) < 2:
            raise InsufficientGpsImagesException

        return image_data

    def read_dng(self, image_path: str) -> numpy.ndarray:
        """Read a DNG file and return an RGB image."""

        try:
            with rawpy.imread(image_path) as raw:
                rgb = raw.postprocess()
                return rgb
        except Exception as e:
            raise ReadDngFileException(
                f"Error reading DNG file {image_path}: {e}")

    def align_and_return_images(self) -> numpy.ndarray:
        """Align images based on GPS metadata and return list."""

        self.image_data.sort(key=lambda x: (
            x[1]['latitude'], x[1]['longitude']))
        images = [img[0] for img in self.image_data]

        return images

    def create_stitched_map(self, images: numpy.ndarray, results_dir: str) -> None:
        """Stitch images and save output file in results directory."""

        stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
        stitcher.setRegistrationResol(0.6)
        stitcher.setSeamEstimationResol(0.1)
        stitcher.setCompositingResol(-1)
        stitcher.setPanoConfidenceThresh(0.8)

        try:
            status, stitched = stitcher.stitch(images)
        except cv2.error as e:
            raise cv2.error(f"OpenCV error during stitching: {e}")

        if status == cv2.Stitcher_OK:
            cv2.imwrite(f"{results_dir}/{self.result_filename}.jpg",
                        stitched, [cv2.IMWRITE_JPEG_QUALITY, 100])
            print(
                f"Stitching completed and saved as '{self.result_filename}.jpg'")
        else:
            raise CreateStitchedMapException(
                f"Error during stitching: {status}")


try:
    geo_align = GeoAligner(f"{DATASET_DIR}/geotagged")
    images = geo_align.align_and_return_images()
    geo_align.create_stitched_map(images, RESULTS_DIR)
except GeoAlignerBaseException as e:
    print(e.message)
