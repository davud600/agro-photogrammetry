import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

class PlotBuilder:
    def __init__(self, num_of_indices_to_show):
        self.num_of_indices_to_show = num_of_indices_to_show
        self.plt = plt

    def show_plot(self):
        self.plt.show()

    def create_plot(self):
        self.fig = self.plt.figure(figsize=(16, 9), dpi=120, facecolor=(0.8, 0.8, 0.8))
        if self.num_of_indices_to_show == 1:
            self.gs = gridspec.GridSpec(1, 1)
        elif self.num_of_indices_to_show == 2:
            self.gs = gridspec.GridSpec(1, 2)
        elif self.num_of_indices_to_show == 3 or self.num_of_indices_to_show == 4:
            self.gs = gridspec.GridSpec(2, 2)
        elif self.num_of_indices_to_show == 5 or self.num_of_indices_to_show == 6:
            self.gs = gridspec.GridSpec(2, 3)
        self.plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.05, hspace=0.25)

    def create_subplot(self, row_index, col_index, index, index_type):
        colors = [(0, 'red'), (0.5, 'yellow'), (1, 'green')]
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)
        subplot = self.fig.add_subplot(self.gs[row_index, col_index], facecolor=(0.9, 0.9, 0.9))
        img = subplot.imshow(index, cmap=custom_cmap)
        subplot.set_xticks([])
        subplot.set_yticks([])
        subplot.set_title(index_type)
        
        # Create a colorbar
        cbar = self.fig.colorbar(img, ax=subplot, orientation='vertical')
