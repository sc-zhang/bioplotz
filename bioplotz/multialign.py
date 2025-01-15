import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D, offset_copy


class _MultiAlign(object):

    def __init__(self,
                 data: dict,
                 base_per_line: int = 80,
                 color_mode: str = 'match',
                 color_kws: dict = None):
        self.__data = data
        self.__base_per_line = base_per_line
        self.__color_mode = color_mode
        self.__color_kws = None

        # set default values of sel.__color_kws
        if self.__color_mode == "match":
            self.__color_kws = {
                "match_color": 'blue',
                "match_background_color": None,
                "mismatch_color": 'red',
                "mismatch_background_color": None,
                "highlight_positions": None,
                "highlight_color": 'green',
                "highlight_background_color": None
            }
        elif self.__color_mode == "base":
            self.__color_kws = {
                "base_color": {},
                "base_background_color": {
                    "A": "salmon", "a": "salmon",
                    "T": "lightgreen", "t": "lightgreen",
                    "G": "orange", "g": "orange",
                    "C": "steelblue", "c": "steelblue",
                    "U": "tomato", "u": "tomato",
                    "F": "khaki", "f": "khaki",
                    "D": "cadetblue", "d": "cadetblue",
                    "N": "coral", "n": "coral",
                    "E": "yellowgreen", "e": "yellowgreen",
                    "Q": "plum", "q": "plum",
                    "H": "orchid", "h": "orchid",
                    "L": "darkseagreen", "l": "darkseagreen",
                    "I": "yellow", "i": "yellow",
                    "K": "lightseagreen", "k": "lightseagreen",
                    "O": "darkkhaki", "o": "darkkhaki",
                    "M": "palevioletred", "m": "palevioletred",
                    "P": "sandybrown", "p": "sandybrown",
                    "R": "palegreen", "r": "palegreen",
                    "S": "peru", "s": "peru",
                    "V": "violet", "v": "violet",
                    "W": "mediumturquoise", "w": "mediumturquoise",
                    "Y": "deepskyblue", "y": "deepskyblue"
                }
            }

        else:
            raise ValueError("Value of color_mode should be \"match\" or \"base\"")

        if color_kws:
            if self.__color_mode == "match":
                for key in color_kws:
                    if key in self.__color_kws:
                        self.__color_kws[key] = color_kws[key]
                    else:
                        raise KeyError("%s not support with color_kws in %s mode" % (key, self.__color_mode))
            elif self.__color_mode == "base":
                if "base_color" in color_kws:
                    for key in color_kws["base_color"]:
                        self.__color_kws["base_color"][key] = color_kws["base_color"][key]
                if "base_background_color" in color_kws:
                    for key in color_kws["base_background_color"]:
                        self.__color_kws["base_background_color"][key] = color_kws["base_background_color"][key]

        if "highlight_positions" in self.__color_kws and self.__color_kws["highlight_positions"]:
            self.__color_kws["highlight_positions"] = set(self.__color_kws["highlight_positions"])

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

            colors = ["black" for _ in range(ep - sp)]
            background_colors = ["white" for _ in range(ep - sp)]

            if self.__color_mode == "match":
                for k in range(sp, ep):
                    cur_set = set()
                    for j in sorted(self.__data):
                        cur_set.add(self.__data[j][k])
                    if len(cur_set) > 1:
                        colors[k - sp] = self.__color_kws["mismatch_color"]
                        background_colors[k - sp] = self.__color_kws["mismatch_background_color"]
                    else:
                        colors[k - sp] = self.__color_kws["match_color"]
                        background_colors[k - sp] = self.__color_kws["match_background_color"]
                    if self.__color_kws["highlight_positions"] and k in self.__color_kws["highlight_positions"]:
                        colors[k - sp] = self.__color_kws["highlight_color"]
                        background_colors[k - sp] = self.__color_kws["highlight_background_color"]

                for j in range(seq_cnt):
                    gid = seq_list[j]
                    y_ticks.append(i * (seq_cnt + 2) + j + 1)
                    y_labels.append(gid)
                    self.__rainbow_text(0, i * (seq_cnt + 2) + j + 1, self.__data[gid][sp: ep],
                                        colors, background_colors, **kwargs)
            elif self.__color_mode == "base":
                for j in range(seq_cnt):
                    gid = seq_list[j]
                    y_ticks.append(i * (seq_cnt + 2) + j + 1)
                    y_labels.append(gid)
                    for k in range(sp, ep):
                        colors[k - sp] = self.__color_kws["base_color"][self.__data[gid][k]] \
                            if self.__data[gid][k] in self.__color_kws["base_color"] \
                            else "black"
                        background_colors[k - sp] = self.__color_kws["base_background_color"][self.__data[gid][k]] \
                            if self.__data[gid][k] in self.__color_kws["base_background_color"] \
                            else "white"
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
               color_mode: str = "match",
               color_kws: dict = None,
               **kwargs):
    plotter = _MultiAlign(data,
                          base_per_line,
                          color_mode,
                          color_kws)

    if not plt:
        plt.figure()
    fig = plt.gcf()
    ax = plt.gca()
    plotter.plot(ax, **kwargs)

    return fig, ax
