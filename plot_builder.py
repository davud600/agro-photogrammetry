import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import RectangleSelector
from functools import partial
import numpy as np

class PlotBuilder:
    def __init__(self, num_of_indices_to_show):
        self.num_of_indices_to_show = num_of_indices_to_show
        self.plt = plt
        self.subplots = {}
        self.indices = {}
        self.press = None

    def show_plot(self):
        self.plt.show()

    def create_plot(self):
        self.fig = self.plt.figure(figsize=(16, 10), dpi=120, facecolor=(0.8, 0.8, 0.8))
        if self.num_of_indices_to_show == 1:
            self.gs = gridspec.GridSpec(1, 1)
        elif self.num_of_indices_to_show == 2:
            self.gs = gridspec.GridSpec(1, 2)
        elif self.num_of_indices_to_show == 3 or self.num_of_indices_to_show == 4:
            self.gs = gridspec.GridSpec(2, 2)
        elif self.num_of_indices_to_show == 5 or self.num_of_indices_to_show == 6:
            self.gs = gridspec.GridSpec(2, 3)
        elif self.num_of_indices_to_show == 7 or self.num_of_indices_to_show == 8:
            self.gs = gridspec.GridSpec(3, 3)
        self.plt.subplots_adjust(left=0.02, bottom=0.075, right=0.98, top=0.925, wspace=0.05, hspace=0.25)

    def create_subplot(self, row_index, col_index, index, index_type, index_label):
        colors = [(0, 'red'), (0.5, 'yellow'), (1, 'green')]
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)
        
        self.indices[index_type] = index
        self.subplots[index_type] = self.fig.add_subplot(self.gs[row_index, col_index], facecolor=(0.9, 0.9, 0.9))
        img = self.subplots[index_type].imshow(index, cmap=custom_cmap)
        self.subplots[index_type].set_xticks([])
        self.subplots[index_type].set_yticks([])
        self.subplots[index_type].set_title(f"{index_type} - {index_label}", fontsize=10)

        flatten_index = np.array(index).flatten()
        flatten_index_len = len(flatten_index)
        flatten_index.sort()

        # median_index = 0
        if flatten_index_len % 2 != 0:
            median = flatten_index[int((flatten_index_len + 1) / 2)]
            # median_index = int((flatten_index_len + 1) / 2)
        else:
            median = (int(flatten_index[int(flatten_index_len / 2)]) + int(flatten_index[int(flatten_index_len / 2) + 1])) / 2
            # median_index = int(flatten_index_len / 2)

        sum = np.sum(flatten_index)
        mean = sum / len(flatten_index)
        # mean_index = 0
        # for i, value in enumerate(flatten_index):
        #     if np.round(value) == np.round(mean):
        #         mean_index = i
        #         break
        
        self.subplots[index_type].text(0, -0.06, f'Mean: {mean}', ha='left', transform=self.subplots[index_type].transAxes, fontsize=8)
        self.subplots[index_type].text(0, -0.12, f'Median: {median}', ha='left', transform=self.subplots[index_type].transAxes, fontsize=8)

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
        cbar = self.fig.colorbar(img, ax=self.subplots[index_type], orientation='vertical')
        cbar.ax.set_position([cbar.ax.get_position().x0, self.subplots[index_type].get_position().y0, cbar.ax.get_position().width, self.subplots[index_type].get_position().height])
        
        # Connect event handlers for zoom and pan
        self.fig.canvas.mpl_connect('scroll_event', partial(self.on_scroll, index_type))
        self.fig.canvas.mpl_connect('button_press_event', partial(self.on_press, index_type))
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', partial(self.on_motion, index_type))
        self.rect_selector = RectangleSelector(self.subplots[index_type], onselect=None, useblit=True, button=[0], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    def on_scroll(self, index_type, event):
        if event.inaxes != self.subplots[index_type]:
            return
        scale_factor = 1 / 1.2 if event.button == 'up' else 1.2
        self.zoom(event.xdata, event.ydata, scale_factor, index_type)

    def zoom(self, x, y, scale_factor, index_type):
        cur_xlim = self.subplots[index_type].get_xlim()
        cur_ylim = self.subplots[index_type].get_ylim()
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - x) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - y) / (cur_ylim[1] - cur_ylim[0])

        new_xlim = [x - new_width * (1 - relx), x + new_width * relx]
        new_ylim = [y - new_height * (1 - rely), y + new_height * rely]

        # Constrain to be within the image bounds
        new_xlim[0] = max(new_xlim[0], 0)
        new_xlim[1] = min(new_xlim[1], self.indices[index_type].shape[1])
        new_ylim[0] = max(new_ylim[0], 0)
        new_ylim[1] = min(new_ylim[1], self.indices[index_type].shape[0])

        self.subplots[index_type].set_xlim(new_xlim)
        self.subplots[index_type].set_ylim(new_ylim)
        self.fig.canvas.draw()

    def on_scroll(self, index_type, event):
        if event.inaxes != self.subplots[index_type]:
            return
        scale_factor = 1 / 1.2 if event.button == 'up' else 1.2
        self.zoom(event.xdata, event.ydata, scale_factor, index_type)

    def zoom(self, x, y, scale_factor, index_type):
        cur_xlim = self.subplots[index_type].get_xlim()
        cur_ylim = self.subplots[index_type].get_ylim()
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - x) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - y) / (cur_ylim[1] - cur_ylim[0])

        self.subplots[index_type].set_xlim([x - new_width * (1 - relx), x + new_width * relx])
        self.subplots[index_type].set_ylim([y - new_height * (1 - rely), y + new_height * rely])
        self.fig.canvas.draw()

    def on_press(self, index_type, event):
        if event.inaxes != self.subplots[index_type]:
            return
        self.press = event.x, event.y, self.subplots[index_type].get_xlim(), self.subplots[index_type].get_ylim()

    def on_motion(self, index_type, event):
        if event.inaxes != self.subplots[index_type] or self.press is None:
            return
        x, y = event.x, event.y
        xpress, ypress, xlims, ylims = self.press
        dx = x - xpress
        dy = y - ypress

        # Invert the vertical movement
        self.subplots[index_type].set_xlim(xlims[0] - dx, xlims[1] - dx)
        self.subplots[index_type].set_ylim(ylims[0] + dy, ylims[1] + dy)
        self.fig.canvas.draw()

    def on_release(self, event):
        self.press = None

    def on_select(self, eclick, erelease):
        pass

