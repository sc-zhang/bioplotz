import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D, offset_copy


class _MultiAlign(object):

    def __init__(self,
                 data: dict,
                 match_color: any = 'blue',
                 mismatch_color: any = 'red'):
        self.__data = data
        self.__match_color = match_color
        self.__mismatch_color = mismatch_color

    @staticmethod
    def __rainbow_text(x, y, strings, colors, ax=None, **kwargs):
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

        for s, c in zip(strings, colors):
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
        row_cnt = int(aln_len / 80.)
        if row_cnt * 80 < aln_len:
            row_cnt += 1
        total_row_cnt = (row_cnt + 2) * seq_cnt

        divide = '----+' * 16
        y_ticks = []
        y_labels = []
        for i in range(row_cnt):
            sp = i * 80
            ep = min(aln_len, sp + 80)

            divide_and_pos = "%s %d-%d" % (divide, sp + 1, ep)
            colors = ['black' for _ in range(len(divide_and_pos))]
            self.__rainbow_text(0, i * (seq_cnt + 2), list(divide_and_pos), colors, **kwargs)
            colors = [self.__match_color for _ in range(ep - sp)]

            for k in range(sp, ep):
                cur_set = set()
                for j in sorted(self.__data):
                    cur_set.add(self.__data[j][k])
                if len(cur_set) > 1:
                    colors[k - sp] = self.__mismatch_color

            for j in range(seq_cnt):
                gid = seq_list[j]
                y_ticks.append(i * (seq_cnt + 2) + j + 1)
                y_labels.append(gid)
                self.__rainbow_text(0, i * (seq_cnt + 2) + j + 1, self.__data[gid][sp: ep], colors, **kwargs)
        ax.set_ylim(0, total_row_cnt)
        ax.set_xticks([])
        ax.invert_yaxis()
        ax.set_yticks(y_ticks, y_labels)
        for i in ax.spines:
            ax.spines[i].set_visible(False)
        ax.tick_params('both', length=0)


def multialign(data: dict,
               match_color: any = 'blue',
               mismatch_color: any = 'red',
               **kwargs):

    plotter = _MultiAlign(data, match_color, mismatch_color)

    if not plt:
        plt.figure()
    fig = plt.gcf()
    ax = plt.gca()
    plotter.plot(ax, **kwargs)

    return fig, ax
