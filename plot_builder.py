import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


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
        self.plt.subplots_adjust(left=0.02, bottom=0.1, right=0.98, top=0.9, wspace=0.05, hspace=0.05)

    def create_subplot(self, row_index, col_index, index, index_type, index_label):
        colors = [(0, 'red'), (0.5, 'yellow'), (1, 'green')]
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)
        subplot = self.fig.add_subplot(self.gs[row_index, col_index], facecolor=(0.9, 0.9, 0.9))
        img = subplot.imshow(index, cmap=custom_cmap)
        subplot.set_xticks([])
        subplot.set_yticks([])
        subplot.set_title(f"{index_type} - {index_label}")

        # flatten_index = np.array(index).flatten()
        # flatten_index_len = len(flatten_index)
        # flatten_index.sort()

        # median_index = 0
        # if flatten_index_len % 2 != 0:
        #     median = flatten_index[int((flatten_index_len + 1) / 2)]
        #     median_index = int((flatten_index_len + 1) / 2)
        # else:
        #     median = (int(flatten_index[int(flatten_index_len / 2)]) + int(flatten_index[int(flatten_index_len / 2) + 1])) / 2
        #     median_index = int(flatten_index_len / 2)

        # sum = 0
        # for value in flatten_index:
        #     sum += value
        # mean_index = 0
        # mean = sum / len(flatten_index)
        # for i, value in enumerate(flatten_index):
        #     if np.round(value) == np.round(mean):
        #         mean_index = i
        #         break
        
        # # subplot.text(0, -0.025, f'Mean: {mean}', ha='left', transform=subplot.transAxes)
        # # subplot.text(0.25, -0.025, f'Median: {median}', ha='left', transform=subplot.transAxes)

        # # test graph subplot
        # smol_arr = flatten_index[:]

        # graph_subplot = self.fig.add_subplot(self.gs[0, 1], facecolor=(0.9, 0.9, 0.9))
        # graph_subplot.set_xlim(0, len(smol_arr))
        # graph_subplot.set_ylim(0, 256)
        # graph_subplot.set_xticks(np.arange(0, len(smol_arr), 100000))
        # graph_subplot.set_yticks(np.arange(0, 255, 50))

        # # median function

        # graph_subplot.plot(np.arange(0, len(smol_arr), 1), smol_arr[:], linewidth=2, color='b')
        # graph_subplot.plot([mean_index, mean_index], [0, mean], linewidth=2, color='r')
        # graph_subplot.plot([median_index, median_index], [0, median], linewidth=2, color='y')
        # graph_subplot.grid(True)
        
        # Create a colorbar
        cbar = self.fig.colorbar(img, ax=subplot, orientation='vertical')
