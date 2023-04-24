import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class _Manhattan(object):
    def __init__(self, data, threshold=0, color=None, threshold_line_color='blue', threshold_line_width=1,
                 block_line_width=1, log_base=0, reverse=False, xtick_labels=True, ytick_labels=True):
        if color is None:
            color = ['orange', 'green']
        if log_base < 0:
            raise ValueError("log base must be greater than or equal to 0")
        x_ticks = []
        x_max = 0
        tmp_y = []
        if not color:
            color = ['orange', 'green']
        '''
        Convert __data to pd.DataFrame
        '''
        if isinstance(data, dict):
            columns = sorted(data)
            data = pd.DataFrame(data, columns=columns)
            for col in columns:
                data[col][0] = np.add(data[col][0], x_max)
                x_ticks.append((max(data[col][0]) - x_max) / 2 + x_max)
                x_max = max(data[col][0])
                if log_base != 0:
                    data[col][1] = np.log(data[col][1]) / np.log(log_base)
                if reverse:
                    data[col][1] = -data[col][1]
                tmp_y.extend(data[col][1])
        elif isinstance(data, list) or isinstance(data, np.ndarray):
            columns = []
            data = pd.DataFrame(data)
            x_max = max(data[0])
            if log_base != 0:
                data[1] = np.log(data[1]) / np.log(log_base)
            if reverse:
                data[1] = -data[1]
            tmp_y.extend(data[1])
        else:
            raise ValueError("Unsupported data type")

        if not isinstance(threshold, list):
            threshold = np.array([threshold])
        else:
            threshold = np.array(threshold)

        if log_base != 0:
            threshold = np.log(threshold) / np.log(log_base)
        if reverse:
            threshold = -threshold

        if not isinstance(threshold_line_color, list):
            threshold_line_color = [threshold_line_color]

        self.__data = data
        self.__xlim = (0, x_max)
        self.__xmax = x_max
        y_min = min(tmp_y)
        y_max = max(tmp_y)
        self.__ymin = y_min
        self.__ymax = y_max
        if y_max < 0:
            y_max = 0
        if y_min > 0:
            y_min = 0
        self.__ylim = (y_min, y_max)
        self.__x_ticks = x_ticks
        self.__x_labels = columns
        self.__color = color
        self.__threshold = threshold
        self.__threshold_line_color = threshold_line_color
        self.__threshold_line_width = threshold_line_width
        self.__block_line_width = block_line_width
        self.__xtick_labels = xtick_labels
        self.__ytick_labels = ytick_labels

    def plot(self, ax, marker, s, kws):
        data = self.__data
        ax.set(xlim=self.__xlim)

        if len(self.__ylim) != 0:
            ax.set(ylim=self.__ylim)
        if self.__xtick_labels:
            if self.__x_ticks:
                ax.set(xticks=self.__x_ticks)
                ax.set_xticklabels(self.__x_labels)
        else:
            ax.set_xticklabels([])

        if not self.__ytick_labels:
            ax.set_yticklabels([])

        # Plot scatter of values
        if not self.__x_labels:
            if isinstance(self.__color, list):
                color = self.__color[0]
            else:
                color = self.__color
            ax.scatter(data[0], data[1], color=color, marker=marker, s=s, **kws)
        else:
            if isinstance(self.__color, list):
                color_cnt = len(self.__color)
                for i in range(0, len(self.__x_labels)):
                    col = self.__x_labels[i]
                    color_idx = i % color_cnt
                    ax.scatter(data[col][0], data[col][1], color=self.__color[color_idx], marker=marker, s=s, **kws)
                    if color_cnt == 1:
                        x = max(data[col][0])
                        ax.plot([x, x], [self.__ymin, self.__ymax], color='lightgrey', lw=self.__block_line_width,
                                linestyle=':')
            else:
                for col in self.__x_labels:
                    ax.scatter(data[col][0], data[col][1], color=self.__color, **kws)
                    x = max(data[col][0])
                    ax.plot([x, x], [self.__ymin, self.__ymax], color='lightgrey', lw=self.__block_line_width,
                            linestyle=':')

        ax.plot([0, self.__xmax], [0, 0], color='lightgrey', lw=self.__block_line_width)
        # Plot thresholds
        if not (len(self.__threshold) == 1 and self.__threshold[0] == 0):
            color_cnt = len(self.__threshold_line_color)
            for i in range(0, len(self.__threshold)):
                th = self.__threshold[i]
                color_idx = i % color_cnt
                ax.plot([0, self.__xmax], [th, th], color=self.__threshold_line_color[color_idx],
                        lw=self.__threshold_line_width, linestyle=':')

        ax.tick_params(axis='both', which='both', length=0)
        ax.spines['top'].set_linewidth(0.5)
        ax.spines['top'].set_color('lightgrey')
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['bottom'].set_color('lightgrey')
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['left'].set_color('lightgrey')
        ax.spines['right'].set_linewidth(0.5)
        ax.spines['right'].set_color('lightgrey')


def manhattan(data, threshold=0, color=None,
              threshold_line_color='blue', threshold_line_width=1,
              block_line_width=1, log_base=0, reverse=False,
              xtick_labels=True, ytick_labels=True, ax=None, marker='.',
              s=1, **kwargs):
    if color is None:
        color = ['orange', 'green']
    plotter = _Manhattan(data, threshold, color, threshold_line_color, threshold_line_width, block_line_width,
                         log_base, reverse, xtick_labels, ytick_labels)

    if ax is None:
        ax = plt.gca()
    plotter.plot(ax, marker, s, kwargs)

    return ax
