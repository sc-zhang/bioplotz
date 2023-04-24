import matplotlib as mpl
import matplotlib.pyplot as plt


class _GeneCluster(object):

    def __init__(self,
                 gene_list: list,
                 edgecolor: any = None,
                 edgewidth: int = 1,
                 lw: int = 3):

        self.__gene_list = gene_list
        self.__edgecolor = edgecolor
        self.__edgewidth = edgewidth
        self.__lw = lw

    def plot(self, ax, fig):
        fig_w, fig_h = fig.get_size_inches() * fig.dpi
        ymax = fig_h * 10. / fig_w
        xticks = []
        xlabels = []
        min_pos = None
        max_pos = None
        for gn, sp, ep, _, _ in self.__gene_list:
            if not min_pos or sp < min_pos:
                min_pos = sp
            if not max_pos or ep > max_pos:
                max_pos = ep

            xticks.append((ep + sp) / 2.)
            xlabels.append(gn)
        for i in range(len(self.__gene_list)):
            gn, sp, ep, direct, color = self.__gene_list[i]
            if self.__edgecolor:
                if isinstance(self.__edgecolor, list):
                    edgecolor = self.__edgecolor[i]
                else:
                    edgecolor = self.__edgecolor
            else:
                edgecolor = None
            if direct == '+':
                ax.arrow(sp, 0, ep - sp + 1, 0, length_includes_head=True, head_length=min(max_pos / 50., ep - sp + 1),
                         width=0.4, head_width=0.75, facecolor=color, edgecolor=edgecolor,
                         zorder=99, lw=self.__edgewidth)
            else:
                ax.arrow(ep, 0, -(ep - sp + 1), 0, length_includes_head=True,
                         head_length=min(max_pos / 50., ep - sp + 1), width=0.4, head_width=0.75, facecolor=color,
                         edgecolor=edgecolor, zorder=99, lw=self.__edgewidth)
        ax.plot([min_pos, max_pos], [0, 0], color='lightgrey', lw=self.__lw, zorder=1)
        ax.set_ylim(-.5, max(.5, ymax - .5))
        ax.set_yticks([])
        ax.set_xticks(xticks, xlabels, rotation=-45, ha='center')
        for i in ax.spines:
            ax.spines[i].set_visible(False)
        ax.tick_params('both', length=0)


def gene_cluster(gene_list: list,
                 edgecolor: any = None,
                 edgewidth: int = 1,
                 lw: int = 3
                 ):

    plotter = _GeneCluster(gene_list, edgecolor, edgewidth, lw)

    if not plt:
        plt.figure()
    plotter.plot(plt.gca(), plt.gcf())

    return plt.gca()
