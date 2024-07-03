import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def calculate_ndvi(red_band, nir_band):
    red_band = red_band.astype(float)
    nir_band = nir_band.astype(float)
    ndvi = (nir_band - red_band) / ((nir_band + red_band + 1e-6) + 0.000001)
    ndvi = ((ndvi + 1) / 2 * 255).astype(np.uint8)
    return ndvi

def calculate_vari(red_band, green_band, blue_band):
    red_band = red_band.astype(float)
    green_band = green_band.astype(float)
    blue_band = blue_band.astype(float)
    vari = (green_band - red_band) / ((green_band + red_band - blue_band) + 0.000001)
    # vari = ((vari + 1) / 2 * 255).astype(np.uint8)
    return vari

def calculate_ri(red_band, green_band, blue_band):
    red_band = red_band.astype(float)
    green_band = green_band.astype(float)
    blue_band = blue_band.astype(float)
    ri = np.power(red_band, 2) / ((blue_band * np.power(green_band, 2)) + 0.000001)
    # ri = ((ri + 1) / 2 * 255).astype(np.uint8)
    return ri

def calculate_bi(red_band, green_band, blue_band):
    red_band = red_band.astype(float)
    green_band = green_band.astype(float)
    blue_band = blue_band.astype(float)
    bi = (np.power(red_band, 2) + np.power(green_band, 2) + np.power(blue_band, 2)) / 3
    # bi = ((bi + 1) / 2 * 255).astype(np.uint8)
    return bi

def calculate_ipvi(red_band, nir_band):
    red_band = red_band.astype(float)
    nir_band = nir_band.astype(float)
    ipvi = nir_band / (nir_band + red_band)
    # ipvi = ((ipvi + 1) / 2 * 255).astype(np.uint8)
    return ipvi

def visualize_index(index, index_type = 'NDVI'):
    plt.imshow(index, cmap='RdYlGn')
    plt.colorbar()
    plt.title(index_type)
    plt.show()

# Load multispectral images
blue_band = load_image('dataset/rededge_raw_example1/IMG_0455_1.tif')  # blue
green_band = load_image('dataset/rededge_raw_example1/IMG_0455_2.tif')  # green
red_band = load_image('dataset/rededge_raw_example1/IMG_0455_3.tif')  # red
nir_band = load_image('dataset/rededge_raw_example1/IMG_0455_4.tif')  # nir

# Calculate NDVI
ndvi = calculate_ndvi(red_band, nir_band)

# Calculate VARI
vari = calculate_vari(red_band, green_band, blue_band)

# Calculate RI
ri = calculate_ri(red_band, green_band, blue_band)

# Calculate BI
bi = calculate_bi(red_band, green_band, blue_band)

# Calculate ipvi
ipvi = calculate_ipvi(red_band, nir_band)

# Visualize
visualize_index(ndvi, 'NDVI')
# visualize_index(vari, 'VARI')
# visualize_index(ri, 'RI')
# visualize_index(bi, 'BI')
# visualize_index(ipvi, 'IPVI')
