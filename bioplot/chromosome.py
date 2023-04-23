import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class _Chromosome(object):

    def __init__(self, chr_len_db: dict, bed_data: list, centro_db: dict = None, byval: bool = True, lw: int = 3):
        self.__chr_len_db = chr_len_db
        self.__bed_data = bed_data
        self.__centro_db = centro_db
        self.__byval = byval
        self.__lw = lw

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

    def plot(self, ax, fig):
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
        ratio = max_height * 1. / chr_cnt * (fig_w * 1. / fig_h)
        for i in range(chr_cnt):
            chrn = chr_list[i]
            x = i + 0.5
            r = 0.35

            height = self.__chr_len_db[chrn]

            # Draw two end arc
            for j in [2, 3]:
                arc_x, arc_y = self.__generate_arc(r, [x, 0], j, ratio)
                plt.plot(arc_x, arc_y, color='black', lw=self.__lw)
            for j in [0, 1]:
                arc_x, arc_y = self.__generate_arc(r, [x, height], j, ratio)
                plt.plot(arc_x, arc_y, color='black', lw=self.__lw)

            if self.__centro_db and chrn in self.__centro_db:
                # if centromere found, draw it
                plt.plot([x - 0.35, x - 0.35], [0, self.__centro_db[chrn] - r * ratio], color='black', lw=self.__lw)
                plt.plot([x - 0.35, x - 0.35], [self.__centro_db[chrn] + r * ratio, height],
                         color='black', lw=self.__lw)
                plt.plot([x + 0.35, x + 0.35], [0, self.__centro_db[chrn] - r * ratio], color='black', lw=self.__lw)
                plt.plot([x + 0.35, x + 0.35], [self.__centro_db[chrn] + r * ratio, height],
                         color='black', lw=self.__lw)
                for j in [2, 3]:
                    arc_x, arc_y = self.__generate_arc(r, [x, self.__centro_db[chrn] + r * ratio], j, ratio)
                    plt.plot(arc_x, arc_y, color='black', lw=self.__lw)
                for j in [0, 1]:
                    arc_x, arc_y = self.__generate_arc(r, [x, self.__centro_db[chrn] - r * ratio], j, ratio)
                    plt.plot(arc_x, arc_y, color='black', lw=self.__lw)
            else:
                plt.plot([x - 0.35, x - 0.35], [0, height], color='black', lw=self.__lw)
                plt.plot([x + 0.35, x + 0.35], [0, height], color='black', lw=self.__lw)

        clb = None
        if self.__byval:
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
            chr_idx_db = {chr_list[_]: _ for _ in range(chr_cnt)}
            for chrn, sp, ep, val in self.__bed_data:
                color = mapper.to_rgba(val)
                ax.add_patch(
                    plt.Rectangle((chr_idx_db[chrn] + 0.15, sp), .7, ep - sp + 1, facecolor=color, edgecolor='none'))
            clb = plt.colorbar(mapper, shrink=0.5)
        else:
            chr_idx_db = {chr_list[_]: _ for _ in range(chr_cnt)}
            for chrn, sp, ep, color in self.__bed_data:
                ax.add_patch(
                    plt.Rectangle((chr_idx_db[chrn] + 0.15, sp), .7, ep - sp + 1, facecolor=color, edgecolor='none'))
        xticks = []
        for i in range(chr_cnt):
            xticks.append(i + 0.5)
        ax.set_xticks(xticks, sorted(self.__chr_len_db), rotation=90)
        yticks = []
        ylabels = []
        # add label each Mb
        for pos in range(0, int(max_height), int(1e6)):
            yticks.append(pos)
            ylabels.append("%.0fMb" % (pos / 1e6))
        ax.set_yticks(yticks, ylabels)

        return clb


def chromosome(chr_len_db: dict, bed_data: list, centro_db: dict = None, byval: bool = True, lw: int = 3):
    plotter = _Chromosome(chr_len_db, bed_data, centro_db, byval, lw)

    if not plt:
        plt.figure()
    clb = plotter.plot(plt.gca(), plt.gcf())

    return plt.gca(), clb
