## Introduction

This is a package for plotting some images for bioinformatics.

## Dependencies
Python modules:  
&ensp;&ensp;&ensp;&ensp;numpy  
&ensp;&ensp;&ensp;&ensp;matplotlib  
&ensp;&ensp;&ensp;&ensp;pandas  

## Usage

### Manhanttan Plot

```python
import bioplot.manhattan as mh

man_plot = mh.manhattan(data, threshold=0, color=['orange', 'green'], threshold_line_color='blue', log_base=0,
                        reverse=False, xtick_labels=True, ytick_labels=True, ax=None, marker='.', s=1, **kwargs)
```
| parameter                | value type                | explain                                                                                                                                                                                                                                                                                                                                                              |
|--------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **data**                 | DataFrame<br>dict<br>list | **DataFrame** row header means x, column header means each block and values means y<br>**dict** key means block, value should contain a list like: [[x1,x2,...,xn], [y1,y2,...,yn]]<br>**list** is a list like: [[x1,x2,...,xn], [y1,y2,...,yn]]                                                                                                                     |
| **threshold**            | value<br>list             | **value** if only one threshold line to plot, Notice: if log_base was set, threshold values should be calculated with same log_base manunally, if reverse is True, threshold values should be set to its opposite number<br>**list** if more than one threshold line need to plot, a list can be used for different lines, like: [threshold_value1, threshol_value2] |
| **color**                | list                      | **color** is a list used for blocks, if the count of block greater than color count, it will be used circularly                                                                                                                                                                                                                                                      |
| **threshold_line_color** | value<br>list             | **value** if **threshold** is a single value<br>**list** if **threshold** is a list                                                                                                                                                                                                                                                                                  |
| **log_base**             | value                     | log_base = 0 means not calucate value with log<br>log_base != 0 means log base for log values with it                                                                                                                                                                                                                                                                |
| **reverse**              | Boolean                   | if all data lower than 0, you may use it to show opposite values                                                                                                                                                                                                                                                                                                     |
| **other parameters**     | value                     | same with parameters used in **pyplot.scatter**                                                                                                                                                                                                                                                                                                                      |

### Chromosome Plot

```python
import bioplot.chromosome as chrp

chr_plot = chrp.chromosome(chr_len, bed_data, centro_pos, byval, orientation="vertical", "**kwargs)
```
| parameter            | value type | explain                                                                                                |
|----------------------|------------|--------------------------------------------------------------------------------------------------------|
| **chr_len**          | Directory  | **key**: chromosome name<br>**value**: chromosome length                                               |
| **bed_data**         | list       | **list**: two dimension list, like: [[chrome name, start pos, end pos, value/color]]                   |
| **centro_pos**       | Directory  | **key**: chromosome name<br>**value**: middle position of centromere                                   |
| **byval**            | boolean    | **True**: the 4th column of bed_data should be value<br>**False**: the 4th column of bed_data is color |
| **orientation**      | str        | "vertical" or "horizontal"                                                                             |
| **other parameters** | value      | same with parameters used in **pyplot.scatter**                                                        |

If byval is True, the return value is (ax, colorbar), otherwise (ax, None)
