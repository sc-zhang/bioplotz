import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class _Chromosome(object):

    def __init__(self,
                 chr_len_db: dict,
                 chr_order: list = None,
                 bed_data: list = None,
                 centro_db: dict = None,
                 value_type: str = "numeric",
                 orientation: str = "vertical"):

        self.__chr_len_db = chr_len_db
        self.__chr_order = chr_order
        self.__bed_data = bed_data
        self.__centro_db = centro_db
        self.__value_type = value_type.lower()
        self.__avail_types = {'numeric', 'color', 'marker'}

        if self.__value_type not in self.__avail_types:
            raise ValueError("value_type must in %s" % ','.join(list(self.__avail_types)))

        self.__orientation = orientation

    # pos: 0~3, means top_right, top_left, buttom_left, buttom_right
    @staticmethod
    def __generate_arc(r, c, pos, ratio):
        x = []
        y = []
        theta = pos * np.pi / 2.0
        while theta <= (pos + 1) * np.pi / 2.0:
            x.append(r * np.cos(theta) + c[0])
            y.append(r * np.sin(theta) * ratio + c[1])
            theta += 0.01
        return x, y

    def plot(self, ax, fig, kwargs):
        if self.__orientation != "vertical" and self.__orientation != "horizontal":
            print("Warning: orientation must be \"vertical\" or \"horizontal\", reset to \"vertical\"")
            self.__orientation = "vertical"
        for i in ax.spines:
            ax.spines[i].set_visible(False)
        ax.tick_params('both', length=0)
        chr_list = sorted(self.__chr_len_db)
        chr_cnt = len(chr_list)
        max_height = 0
        for _ in self.__chr_len_db:
            if max_height < self.__chr_len_db[_]:
                max_height = self.__chr_len_db[_]

        # Plot chromosomes
        fig_w, fig_h = fig.get_size_inches() * fig.dpi
        if self.__orientation == 'horizontal':
            ratio = max_height * 1. / chr_cnt * (fig_h * 1. / fig_w)
        else:
            ratio = max_height * 1. / chr_cnt * (fig_w * 1. / fig_h)
        for i in range(chr_cnt):
            if self.__chr_order:
                chrn = self.__chr_order[i]
            else:
                chrn = chr_list[i]
            x = i
            r = 0.35

            height = self.__chr_len_db[chrn]

            # Draw two end arc
            for j in [2, 3]:
                arc_x, arc_y = self.__generate_arc(r, [x, 0], j, ratio)
                if self.__orientation == "horizontal":
                    arc_x, arc_y = arc_y, arc_x
                plt.plot(arc_x, arc_y, **kwargs)
            for j in [0, 1]:
                arc_x, arc_y = self.__generate_arc(r, [x, height], j, ratio)
                if self.__orientation == "horizontal":
                    arc_x, arc_y = arc_y, arc_x
                plt.plot(arc_x, arc_y, **kwargs)

            if self.__centro_db and chrn in self.__centro_db:
                # if centromere found, draw it
                x_start = x - 0.35
                x_end = x - 0.35
                y_start = 0
                y_end = self.__centro_db[chrn] - r * ratio
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

                x_start = x - 0.35
                x_end = x - 0.35
                y_start = self.__centro_db[chrn] + r * ratio
                y_end = height
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

                x_start = x + 0.35
                x_end = x + 0.35
                y_start = 0
                y_end = self.__centro_db[chrn] - r * ratio
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

                x_start = x + 0.35
                x_end = x + 0.35
                y_start = self.__centro_db[chrn] + r * ratio
                y_end = height
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

                for j in [2, 3]:
                    arc_x, arc_y = self.__generate_arc(r, [x, self.__centro_db[chrn] + r * ratio], j, ratio)
                    if self.__orientation == "horizontal":
                        arc_x, arc_y = arc_y, arc_x
                    plt.plot(arc_x, arc_y, **kwargs)
                for j in [0, 1]:
                    arc_x, arc_y = self.__generate_arc(r, [x, self.__centro_db[chrn] - r * ratio], j, ratio)
                    if self.__orientation == "horizontal":
                        arc_x, arc_y = arc_y, arc_x
                    plt.plot(arc_x, arc_y, **kwargs)
            else:
                x_start = x - 0.35
                x_end = x - 0.35
                y_start = 0
                y_end = height
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

                x_start = x + 0.35
                x_end = x + 0.35
                y_start = 0
                y_end = height
                if self.__orientation == "horizontal":
                    x_start, y_start = y_start, x_start
                    x_end, y_end = y_end, x_end
                plt.plot([x_start, x_end], [y_start, y_end], **kwargs)

        # set default color
        if not kwargs.get("color") and not kwargs.get("c"):
            for line in ax.get_lines():
                line.set_color("black")

        xticks = []
        for i in range(chr_cnt):
            xticks.append(i)
        xlabels = self.__chr_order

        yticks = []
        ylabels = []
        # add label each Mb
        for pos in range(0, int(max_height), int(1e6)):
            yticks.append(pos)
            ylabels.append("%.0fMb" % (pos / 1e6))

        if self.__orientation == 'horizontal':
            xticks, yticks = yticks, xticks
            xlabels, ylabels = ylabels, xlabels
        ax.set_xticks(xticks, xlabels, rotation=90 if self.__orientation == "vertical" else 0)
        ax.set_yticks(yticks, ylabels)

        clb = None

        if not self.__bed_data:
            return None

        chr_idx_db = {self.__chr_order[_]: _ for _ in range(chr_cnt)}
        if self.__value_type == 'numeric':
            # Init colormap
            max_val = None
            min_val = None
            for _, _, _, val in self.__bed_data:
                if not max_val or val > max_val:
                    max_val = val
                if not min_val or val < min_val:
                    min_val = val
            norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val, clip=True)
            mapper = mpl.cm.ScalarMappable(norm=norm, cmap=plt.get_cmap("gist_rainbow"))
            mapper.set_array(np.arange(min_val, max_val, 0.1))

            # Plot regions
            for chrn, sp, ep, val in self.__bed_data:
                x = chr_idx_db[chrn] - 0.35
                y = sp
                w = .7
                h = ep - sp + 1
                if self.__orientation == 'horizontal':
                    x, y = y, x
                    w, h = h, w
                color = mapper.to_rgba(val)
                ax.add_patch(
                    plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='none'))
            clb = plt.colorbar(mapper, shrink=0.5)
        elif self.__value_type == 'color':
            for chrn, sp, ep, color in self.__bed_data:
                x = chr_idx_db[chrn] - 0.35
                y = sp
                w = .7
                h = ep - sp + 1
                if self.__orientation == 'horizontal':
                    x, y = y, x
                    w, h = h, w
                ax.add_patch(
                    plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='none'))
        elif self.__value_type == 'marker':
            for chrn, sp, ep, marker, color in self.__bed_data:
                x = chr_idx_db[chrn]
                y = sp
                if self.__orientation == 'horizontal':
                    x, y = y, x
                plt.scatter(x, y, color=color, marker=marker)
        return clb


def chromosome(chr_len_db: dict,
               chr_order: list = None,
               bed_data: list = None,
               centro_db: dict = None,
               value_type: str = "numeric",
               orientation: str = "vertical",
               **kwargs):

    plotter = _Chromosome(chr_len_db, chr_order, bed_data, centro_db, value_type, orientation)

    if not plt:
        plt.figure()
    clb = plotter.plot(plt.gca(), plt.gcf(), kwargs)

    return plt.gca(), clb
