from index_calculator import NDVICalculator, VARICalculator, RICalculator, BICalculator, IPVICalculator, SAVICalculator, EVICalculator
from enum import Enum


DATASET_DIR = "data"
RESULTS_DIR = "results"


class Bands(Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    NIR = 'nir'


AVAILABLE_BANDS = [band.value for band in Bands]


class Indices(Enum):
    NDVI = 'ndvi'
    VARI = 'vari'
    RI = 'ri'
    BI = 'bi'
    IPVI = 'ipvi'
    SAVI = 'savi'
    EVI = 'evi'


AVAILABLE_INDICES = [index.value for index in Indices]


INDEX_CALCULATORS = {
    'NDVI': (NDVICalculator, ['nir_band', 'red_band']),
    'VARI': (VARICalculator, ['red_band', 'green_band', 'blue_band']),
    'RI': (RICalculator, ['red_band', 'green_band', 'blue_band']),
    'BI': (BICalculator, ['red_band', 'green_band', 'blue_band']),
    'IPVI': (IPVICalculator, ['nir_band', 'red_band']),
    'SAVI': (SAVICalculator, ['nir_band', 'red_band']),
    'EVI': (EVICalculator, ['nir_band', 'red_band', 'blue_band']),
}
