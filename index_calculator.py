from enum import Enum
import numpy as np

class Band(Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    NIR = 'nir'

AVAILABLE_BANDS = [band.value for band in Band]

class Index(Enum):
    NDVI = 'ndvi'
    VARI = 'vari'
    RI = 'ri'
    BI = 'bi'
    IPVI = 'ipvi'
    SAVI = 'savi'
    EVI = 'evi'

AVAILABLE_INDICES = [index.value for index in Index]


class IndexCalculator:
    def calculate_index(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def normalize_and_return_index(self, index):
        normalized_index = ((index + 1) / 2 * 255).astype(np.uint8)
        return normalized_index

    def get_index_type(self):
        return self.index_type

    def get_index_label(self):
        return self.label


class NDVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'NDVI'
        self.label = 'Normalized difference vegetation index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        ndvi = (self.nir_band - self.red_band) / (self.nir_band + self.red_band + 0.0001)
        return self.normalize_and_return_index(ndvi)


class VARICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'VARI'
        self.label = 'Visible atmospherically resistant index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        vari = (self.green_band - self.red_band) / (self.green_band + self.red_band - self.blue_band + 0.0001)
        return self.normalize_and_return_index(vari)


class RICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'RI'
        self.label = 'Redness index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        ri = np.power(self.red_band, 2) / (self.blue_band * np.power(self.green_band, 2) + 0.0001)
        return self.normalize_and_return_index(ri)


class BICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'BI'
        self.label = 'Brightness index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        bi = (np.power(self.red_band, 2) + np.power(self.green_band, 2) + np.power(self.blue_band, 2)) / 3
        return self.normalize_and_return_index(bi)


class IPVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'IPVI'
        self.label = 'Infrared percentage vegetation index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        ipvi = self.nir_band / (self.nir_band + self.red_band + 0.0001)
        return self.normalize_and_return_index(ipvi)


class SAVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'SAVI'
        self.label = 'Soil adjusted vegetation index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        L = 0.5
        savi = ((self.nir_band - self.red_band) / (self.nir_band + self.red_band + L)) * (1 + L)
        return self.normalize_and_return_index(savi)


class EVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band, blue_band):
        self.index_type = 'EVI'
        self.label = 'Enhanced vegetation index'
        self.nir_band = nir_band
        self.red_band = red_band
        self.blue_band = blue_band

    def calculate_index(self):
        C1 = 6
        C2 = 7.5
        G = 2.5
        L = 1
        evi = G * ((self.nir_band - self.red_band) / (self.nir_band + C1 * self.red_band - C2 * self.blue_band + L + 0.0001))
        return self.normalize_and_return_index(evi)
