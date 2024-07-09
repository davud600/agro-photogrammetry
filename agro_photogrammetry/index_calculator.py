import numpy as np


class IndexCalculator:
    def calculate_index(self):
        raise NotImplementedError("Subclasses should implement this method")

    def normalize_and_return_index(self, index):
        normalized_index = ((index + 1) / 2 * 255).astype(np.uint8)
        return normalized_index

    def get_index_type(self) -> str:
        return self.index_type if self.index_type is not None else ""

    def get_index_label(self) -> str:
        return self.label if self.label is not None else ""


class NDVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'NDVI'
        self.label = 'Normalized Difference Vegetation Index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        ndvi = (self.nir_band - self.red_band) / \
            (self.nir_band + self.red_band + 0.0001)
        return self.normalize_and_return_index(ndvi)


class VARICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'VARI'
        self.label = 'Visible Atmospherically Resistant Index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        vari = (self.green_band - self.red_band) / \
            (self.green_band + self.red_band - self.blue_band + 0.0001)
        return self.normalize_and_return_index(vari)


class RICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'RI'
        self.label = 'Redness Index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        ri = np.power(self.red_band, 2) / (self.blue_band *
                                           np.power(self.green_band, 2) + 0.0001)
        return self.normalize_and_return_index(ri)


class BICalculator(IndexCalculator):
    def __init__(self, red_band, green_band, blue_band):
        self.index_type = 'BI'
        self.label = 'Brightness Index'
        self.red_band = red_band
        self.green_band = green_band
        self.blue_band = blue_band

    def calculate_index(self):
        bi = (np.power(self.red_band, 2) +
              np.power(self.green_band, 2) + np.power(self.blue_band, 2)) / 3
        return self.normalize_and_return_index(bi)


class IPVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'IPVI'
        self.label = 'Infrared Percentage Vegetation Index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        ipvi = self.nir_band / (self.nir_band + self.red_band + 0.0001)
        return self.normalize_and_return_index(ipvi)


class SAVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band):
        self.index_type = 'SAVI'
        self.label = 'Soil Adjusted Vegetation Index'
        self.nir_band = nir_band
        self.red_band = red_band

    def calculate_index(self):
        L = 0.5
        savi = ((self.nir_band - self.red_band) /
                (self.nir_band + self.red_band + L)) * (1 + L)
        return self.normalize_and_return_index(savi)


class EVICalculator(IndexCalculator):
    def __init__(self, nir_band, red_band, blue_band):
        self.index_type = 'EVI'
        self.label = 'Enhanced Vegetation Index'
        self.nir_band = nir_band
        self.red_band = red_band
        self.blue_band = blue_band

    def calculate_index(self):
        C1 = 6
        C2 = 7.5
        G = 2.5
        L = 1
        evi = G * ((self.nir_band - self.red_band) / (self.nir_band +
                   C1 * self.red_band - C2 * self.blue_band + L + 0.0001))
        return self.normalize_and_return_index(evi)
