import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D, offset_copy


class _MultiAlign(object):

    def __init__(self,
                 data: dict,
                 base_per_line: int = 80,
                 match_color: any = 'blue',
                 match_background_color: any = None,
                 mismatch_color: any = 'red',
                 mismatch_background_color: any = None,
                 highlight_positions: list = None,
                 highlight_color: any = 'green',
                 highlight_background_color: any = None):
        self.__data = data
        self.__base_per_line = base_per_line
        self.__match_color = match_color
        self.__match_background_color = match_background_color
        self.__mismatch_color = mismatch_color
        self.__mismatch_background_color = mismatch_background_color
        if highlight_positions:
            self.__highlight_positions = set(highlight_positions)
        else:
            self.__highlight_positions = None
        self.__highlight_color = highlight_color
        self.__highlight_background_color = highlight_background_color

    @staticmethod
    def __rainbow_text(x, y, strings, colors, background_colors, ax=None, **kwargs):
        """
        Take a list of *strings* and *colors* and place them next to each
        other, with text strings[i] being shown in colors[i].

        Parameters
        ----------
        x, y : float
            Text position in data coordinates.
        strings : list of str
            The strings to draw.
        colors : list of color
            The colors to use.
        ax : Axes, optional
            The Axes to draw into. If None, the current axes will be used.
        **kwargs
            All other keyword arguments are passed to plt.text(), so you can
            set the font size, family, etc.
        """
        if ax is None:
            ax = plt.gca()
        t = ax.transData
        fig = ax.figure
        canvas = fig.canvas

        for s, c, bc in zip(strings, colors, background_colors):
            if bc:
                text = ax.text(x, y, s, color=c,
                               bbox=dict(facecolor=bc, linewidth=0, pad=0),
                               transform=t, **kwargs)
            else:
                text = ax.text(x, y, s, color=c, transform=t, **kwargs)

            # Need to draw to update the text position.
            text.draw(canvas.get_renderer())
            ex = text.get_window_extent()
            # Convert window extent from pixels to inches
            # to avoid issues displaying at different dpi
            ex = fig.dpi_scale_trans.inverted().transform_bbox(ex)
            t = text.get_transform() + offset_copy(Affine2D(), fig=fig, x=ex.width, y=0)

    def plot(self, ax, **kwargs):
        aln_len = 0
        for gid in self.__data:
            aln_len = len(self.__data[gid])
            break
        seq_cnt = len(self.__data)
        seq_list = sorted(self.__data.keys())
        row_cnt = int(aln_len * 1. / self.__base_per_line)
        if row_cnt * self.__base_per_line < aln_len:
            row_cnt += 1
        total_row_cnt = (row_cnt + 2) * seq_cnt

        divide_repeat_cnt = int(self.__base_per_line / 5.)
        if divide_repeat_cnt * 5 < self.__base_per_line:
            divide_repeat_cnt += 1

        divide = '----+' * divide_repeat_cnt
        divide = divide[:self.__base_per_line]

        y_ticks = []
        y_labels = []
        for i in range(row_cnt):
            sp = i * self.__base_per_line
            ep = min(aln_len, sp + self.__base_per_line)

            divide_and_pos = "%s %d-%d" % (divide, sp + 1, ep)
            colors = ['black' for _ in range(len(divide_and_pos))]
            background_colors = ['white' for _ in range(len(divide_and_pos))]
            self.__rainbow_text(0, i * (seq_cnt + 2), list(divide_and_pos), colors, background_colors, **kwargs)
            colors = [self.__match_color for _ in range(ep - sp)]
            background_colors = [self.__match_background_color for _ in range(ep - sp)]

            for k in range(sp, ep):
                cur_set = set()
                for j in sorted(self.__data):
                    cur_set.add(self.__data[j][k])
                if len(cur_set) > 1:
                    colors[k - sp] = self.__mismatch_color
                    background_colors[k - sp] = self.__mismatch_background_color
                if self.__highlight_positions and k in self.__highlight_positions:
                    colors[k - sp] = self.__highlight_color
                    background_colors[k - sp] = self.__highlight_background_color
            for j in range(seq_cnt):
                gid = seq_list[j]
                y_ticks.append(i * (seq_cnt + 2) + j + 1)
                y_labels.append(gid)
                self.__rainbow_text(0, i * (seq_cnt + 2) + j + 1, self.__data[gid][sp: ep],
                                    colors, background_colors, **kwargs)
        ax.set_ylim(0, total_row_cnt)
        ax.set_xticks([])
        ax.invert_yaxis()
        ax.set_yticks(y_ticks, y_labels)
        for i in ax.spines:
            ax.spines[i].set_visible(False)
        ax.tick_params('both', length=0)


def multialign(data: dict,
               base_per_line: int = 80,
               match_color: any = 'blue',
               match_background_color: any = None,
               mismatch_color: any = 'red',
               mismatch_background_color: any = None,
               highlight_positions: list = None,
               highlight_color: any = 'green',
               highlight_background_color: any = None,
               **kwargs):
    plotter = _MultiAlign(data,
                          base_per_line,
                          match_color,
                          match_background_color,
                          mismatch_color,
                          mismatch_background_color,
                          highlight_positions,
                          highlight_color,
                          highlight_background_color)

    if not plt:
        plt.figure()
    fig = plt.gcf()
    ax = plt.gca()
    plotter.plot(ax, **kwargs)

    return fig, ax
