import cv2

def load_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)