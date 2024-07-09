from constants import DATASET_DIR, Bands, INDEX_CALCULATORS
from utils.cli import InvalidBandSelection, InvalidIndexSelection, get_bands_from_user, get_indices_from_user
from plot_builder import PlotBuilder
from utils.images import load_image
import numpy as np

dataset_subdir = "rededge_raw_example3"
dataset_filename_prefix = "IMG_0666_"

# Load multispectral images
while True:
    try:
        selected_bands = get_bands_from_user()
        break
    except InvalidBandSelection as e:
        print(e)

blue_band = green_band = red_band = nir_band = None
for band in selected_bands:
    band_value = band.lower()
    band_index = list(Bands).index(Bands[band_value.upper()]) + 1
    band_path = f"{DATASET_DIR}/{dataset_subdir}/{dataset_filename_prefix}{band_index}.tif"  # noqa
    globals()[f"{band_value}_band"] = load_image(band_path)

# Plot builder & index calculators
while True:
    try:
        selected_indices = get_indices_from_user(selected_bands)
        break
    except InvalidIndexSelection as e:
        print(e)

index_calculators = []
for index_type in selected_indices:
    if index_type.upper() in INDEX_CALCULATORS:
        calculator_class, required_args = INDEX_CALCULATORS[index_type.upper()]
        args = {arg_name: globals()[arg_name] for arg_name in required_args}
        calculator = calculator_class(**args)
        index_calculators.append(calculator)
    else:
        print(f"Unsupported index type: {index_type}")
plot_builder = PlotBuilder(len(index_calculators))
plot_builder.create_plot()

# Calculate and visualize indices
cols = int(np.ceil(np.sqrt(len(index_calculators))))
rows = int(np.ceil(len(index_calculators) / cols))
row, col = 0, 0
for i, index_calculator in enumerate(index_calculators):
    index = index_calculator.calculate_index()
    index_type = index_calculator.get_index_type()
    index_label = index_calculator.get_index_label()
    plot_builder.create_subplot(row, col, index, index_type, index_label)

    col += 1
    if col >= cols:
        col = 0
        row += 1

plot_builder.show_plot()
