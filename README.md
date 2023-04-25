## Introduction

This is a package for plotting some images for bioinformatics.

## Dependencies
Python modules:  
&ensp;&ensp;&ensp;&ensp;numpy  
&ensp;&ensp;&ensp;&ensp;matplotlib  
&ensp;&ensp;&ensp;&ensp;pandas  

## Installation
```bash
pip install git+https://github.com/sc-zhang/bioplotz.git --user
```

## Usage

### Manhanttan Plot

```python
import bioplotz as bp

fig, ax = bp.manhattan(data, threshold=0, color=['orange', 'green'], threshold_line_color='blue', log_base=0,
                       reverse=False, xtick_labels=True, ytick_labels=True, ax=None, marker='.', s=1, **kwargs)
```
| parameter                | value type    | explain                                                                                                                                                                                                                                                                                                                                                              |
|--------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **data**                 | dict<br>list  | **dict** key: block name<br>&ensp;&ensp;&ensp;&ensp;value: [[x1,x2,...,xn], [y1,y2,...,yn]]<br>**list** is a list like: [[x1,y1], [x2, y2], ..., [xn, yn]]                                                                                                                                                                                                           |
| **threshold**            | value<br>list | **value** if only one threshold line to plot, Notice: if log_base was set, threshold values should be calculated with same log_base manunally, if reverse is True, threshold values should be set to its opposite number<br>**list** if more than one threshold line need to plot, a list can be used for different lines, like: [threshold_value1, threshol_value2] |
| **color**                | list          | **color** is a list used for blocks, if the count of block greater than color count, it will be used circularly                                                                                                                                                                                                                                                      |
| **threshold_line_color** | value<br>list | **value** if **threshold** is a single value<br>**list** if **threshold** is a list                                                                                                                                                                                                                                                                                  |
| **threshold_line_width** | value         | **value** the line width of threshold lines                                                                                                                                                                                                                                                                                                                          |
| **block_line_width**     | value         | **value** if there are only one color, the block line will display as border, the width is set by this parameter                                                                                                                                                                                                                                                     |
| **log_base**             | value         | log_base = 0 means not calucate value with log<br>log_base != 0 means log base for log values with it                                                                                                                                                                                                                                                                |
| **reverse**              | Boolean       | if all data lower than 0, you may use it to show opposite values                                                                                                                                                                                                                                                                                                     |
| **other parameters**     | value         | same with parameters used in **pyplot.scatter**                                                                                                                                                                                                                                                                                                                      |

<table align="center">
<tr>
<td><img width=600 src="examples/manhattan.png"></td>
</tr>
</table>

### Chromosome Plot

```python
import bioplotz as bp

fig, ax, clb = bp.chromosome(chr_len_db, bed_data, centro_pos, value_type="numeric", orientation="vertical", **kwargs)
```
| parameter            | value type                     | Optional | Default      | explain                                                                                                                                                                                                                                                                                                           |
|----------------------|--------------------------------|----------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **chr_len_db**       | dict                           | No       | -            | **key**: chromosome name<br>**value**: chromosome length                                                                                                                                                                                                                                                          |
| **chr_order**        | list                           | Yes      | None         | **list**: the custom chromosome order, like: ["Chr1", "Chr3", "Chr2"]<br>must same with keys in chr_len                                                                                                                                                                                                           |
| **bed_data**         | list                           | Yes      | None         | **list**: two dimension list, like: [[chrome name, start pos, end pos, value/color]]                                                                                                                                                                                                                              |
| **centro_pos**       | dict                           | Yes      | None         | **key**: chromosome name<br>**value**: middle position of centromere                                                                                                                                                                                                                                              |
| **value_type**       | str                            | Yes      | numeric      | **numeric**: the 4th column of bed_data should be value<br>**color**: the 4th column of bed_data is color<br>**marker**: different with other two types, it need 5 columns, the 4th column of bed_data is marker, the 5th column is color (marker is same with the parameter which be used in **pyplot.scatter**) |
| **orientation**      | str                            | Yes      | vertical     | "vertical" or "horizontal"                                                                                                                                                                                                                                                                                        |
| **cmap**             | str                            | Yes      | gist_rainbow | **cmap** for colorbar                                                                                                                                                                                                                                                                                             |
| **cmap_parts**       | int                            | Yes      | 100          | how many parts for splitting cmap                                                                                                                                                                                                                                                                                 |
| **s**                | float or array-like, shape(n,) | Yes      | None         | same with parameter s use in **pyplot.scatter**                                                                                                                                                                                                                                                                   |
| **other parameters** | value                          | Yes      | None         | same with parameters used in **pyplot.plot**                                                                                                                                                                                                                                                                      |

- If value_type is numeric, the return value clb will be colorbar, else None
<table align="center">
<tr>
<td><img width=500 height=270 src="examples/chromosome.png"></td>
<td><img width=500 height=270 src="examples/chromosome_h.png"></td>
</tr>
</table>

### Gene Cluster Plot

```python
import bioplotz as bp

fig, ax = bp.gene_cluster(gene_list)
```
| parameter     | value type  | Optional | Default | explain                                                                                                                                          |
|---------------|-------------|----------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **gene_list** | list        | No       | -       | **list**: 2-dimension list, like [[gene name, start pos, end pos, direct(+/-), color], ..., [gene name, start pos, end pos, direct(+/-), color]] |
| **edgecolor** | list<br>str | Yes      | None    | **list**: same length with gene_list, like: ["green", "blue", ..., "red"]<br>**str**: common edge color for all genes                            |
| **edgewidth** | int         | Yes      | 1       | edge width for all genes                                                                                                                         |
| **lw**        | int         | Yes      | 3       | line width to show the genome backbone                                                                                                           |

**Notice**, the best figsize should be (gene count, 1), for example: plt.figure(figsize=(16, 1)), and the bbox_inches parameter which in savefig should be 'tight'.

<table align="center">
<tr>
<td><img width=600 src="examples/genecluster.png"></td>
</tr>
</table>
