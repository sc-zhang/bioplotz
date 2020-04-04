import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


__all__ = ["manhattan"]


class _Manhattan(object):
	def __init__(self, data, threshold=0.05, value_type="p-value", log_scale=2, plus_minus=False, xticklabels=True, yticklabels=True):