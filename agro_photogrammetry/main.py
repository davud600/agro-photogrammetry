import os
from index_calculator import IndexCalculator
from utils.cli import print_error
from geo_aligner import GeoAligner, GeoAlignerBaseException
from constants import DATASET_DIR, RESULTS_DIR, Bands, INDEX_CALCULATORS
from utils.cli import InvalidBandSelection, InvalidIndexSelection, get_bands_from_user, get_indices_from_user
from plot_builder import PlotBuilder
from utils.images import load_image
import numpy as np
import sys

def main():
    geo_alignment = '--geo-alignment' in sys.argv
    subdir_index = sys.argv.index('--subdir') + 1 if '--subdir' in sys.argv else None
    prefix_index = sys.argv.index('--prefix') + 1 if '--prefix' in sys.argv else None
    dataset_subdir = sys.argv[subdir_index] if subdir_index is not None else None
    dataset_filename_prefix = sys.argv[prefix_index] if prefix_index is not None else None

    if not os.path.exists(f"data/{dataset_subdir}"):
        print_error(f"Subdirectory '{dataset_subdir}' not found inside data folder.")
        return

    if geo_alignment:
        try:
            geo_align = GeoAligner(f"{DATASET_DIR}/{dataset_subdir}")
            images = geo_align.align_and_return_images()
            geo_align.create_stitched_map(images, RESULTS_DIR)
        except GeoAlignerBaseException as e:
            print_error(e)
        return

    while True:
        try:
            selected_bands = get_bands_from_user()
            break
        except InvalidBandSelection as e:
            print(e)

    for band in selected_bands:
        band_value = band.lower()
        band_index = list(Bands).index(Bands[band_value.upper()]) + 1
        band_path = f"{DATASET_DIR}/{dataset_subdir}/{dataset_filename_prefix}{band_index}.tif"  # noqa
        globals()[f"{band_value}_band"] = load_image(band_path)

    while True:
        try:
            selected_indices = get_indices_from_user(selected_bands)
            break
        except InvalidIndexSelection as e:
            print(e)

    index_calculators: list[IndexCalculator] = []
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

    cols = int(np.ceil(np.sqrt(len(index_calculators))))
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

if __name__ == "__main__":
    main()
