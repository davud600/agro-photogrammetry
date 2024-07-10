# agro-photogrammetry

Python-based tool designed for agricultural data analysis using multispectral imagery. It helps farmers and researchers monitor crop health and make data-driven decisions by providing two core functionalities: vegetation index calculation and geospatial image alignment.

## Features

### 1. Vegetation Index Calculation

Processes already aligned multispectral aerial images from different color bands to calculate various vegetation indices. These indices help in assessing crop health and are displayed using `matplotlib`.

**Example Outputs:**
![Vegetation Indices](https://raw.githubusercontent.com/davud600/agro-photogrammetry/main/media/veg-ind-showcase.jpg?raw=true)
**_Example data set is from: [MicaSense RedEdge Sample Data](https://sample.micasense.com/)_**

### 2. Geospatial Image Alignment

This feature processes raw image files containing GPS metadata, aligns them based on their geospatial coordinates, and stitches them together.

**Example Outputs:**
![Geospatial Alignment](https://raw.githubusercontent.com/davud600/agro-photogrammetry/main/media/geo-alg-showcase.jpg?raw=true)

## Installation

1. Clone repo:

   ```sh
   git clone https://github.com/davud600/agro-photogrammetry.git
   cd agro-photogrammetry
   ```

2. Virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Vegetation Index Calculation

1. Place your aligned multispectral images in data/subdir (create subdir for each dataset).

![Subdirectory Example]()

2. Run the main script, replace `dataset_subdir` with the name of your dataset subdirectory and `filename_prefix` with the prefix of the files (only supports .tif) inside the subdirectory. The files should follow the naming convention `prefix_1.tif`, `prefix_2.tif`, etc., where:

   - `1` is blue
   - `2` is green
   - `3` is red
   - `4` is nir

   ```sh
   python agro_photogrammetry/main.py --subdir dataset_subdir --prefix filename_prefix
   ```

3. Follow cli instructions and select bands you want to use aswell as indices you need (make sure your dataset subdir contains the bands you select and are ordered in this manner: blue, green, red, nir).

### Geospatial Image Alignment

1. Place your raw image files (only supports .dng) in data/subdir (create subdir for each dataset, naming of files isn't important as long as they're geotagged).

2. Run the geospatial alignment script (replace subdir with the name of your dataset sub directory):

   ```sh
   python agro_photogrammetry/main.py --geo-alignment --subdir dataset_subdir
   ```

3. Result image should be saved inside the results directory.
