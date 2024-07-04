from index_calculator import Band, Index, NDVICalculator, VARICalculator, RICalculator, BICalculator, IPVICalculator
from plot_builder import PlotBuilder
from utils.cli import InvalidBandSelection, InvalidIndexSelection, get_bands_from_user, get_indices_from_user
from utils.images import load_image
import numpy as np

# Load multispectral images
while True:
    try:
        selected_bands = get_bands_from_user()
        break
    except InvalidBandSelection as e:
        print(e)

blue_band = green_band = red_band = nir_band = None
if Band.BLUE.value in selected_bands:
    blue_band = load_image('dataset/rededge_raw_example1/IMG_0455_1.tif')
if Band.GREEN.value in selected_bands:
    green_band = load_image('dataset/rededge_raw_example1/IMG_0455_2.tif')
if Band.RED.value in selected_bands:
    red_band = load_image('dataset/rededge_raw_example1/IMG_0455_3.tif')
if Band.NIR.value in selected_bands:
    nir_band = load_image('dataset/rededge_raw_example1/IMG_0455_4.tif')

# Plot builder & index calculators
while True:
    try:
        selected_indices = get_indices_from_user(selected_bands)
        break
    except InvalidIndexSelection as e:
        print(e)

index_calculators = []
if Index.NDVI.value in selected_indices:
    index_calculators.append(NDVICalculator(nir_band, red_band))
if Index.VARI.value in selected_indices:
    index_calculators.append(VARICalculator(red_band, green_band, blue_band))
if Index.RI.value in selected_indices:
    index_calculators.append(RICalculator(red_band, green_band, blue_band))
if Index.BI.value in selected_indices:
    index_calculators.append(BICalculator(red_band, green_band, blue_band))
if Index.IPVI.value in selected_indices:
    index_calculators.append(IPVICalculator(nir_band, red_band))
plot_builder = PlotBuilder(len(index_calculators))
plot_builder.create_plot()

# Calculate and visualize indices
row, col = 0, 0
for i, index_calculator in enumerate(index_calculators):
    index = index_calculator.calculate_index()
    index_type = index_calculator.get_index_type()
    plot_builder.create_subplot(row, col, index, index_type)
    if col >= np.round(len(index_calculators) / 2):
        row += 1
        col = 0
    else:
        col += 1

plot_builder.show_plot()
