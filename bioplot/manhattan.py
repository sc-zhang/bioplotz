import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


__all__ = ["manhattan"]


class _Manhattan(object):
	def __init__(self, data, threshold=0.05, value_type="P-value", color=['orange', 'green'], threshold_line_color='blue', log_base=2, plus_minus=False, xticklabels=True, yticklabels=True):
		if log_base < 0:
			raise ValueError("log base must be greater than or equal 0")
		'''
		data can be types show follow:
			{'x': [], 'y': []}
			{'chr': [[], []]}
			{'chr': {'x': [], 'y': []}}
			[[], []]
		'''
		base = 0
		columns = []
		x_ticks = []
		'''
		Convert data to common data
		'''
		if isinstance(data, pd.DataFrame):
			
		elif isinstance(data, dict):

		elif isinstance(data, list):

		else:
			raise ValueError("Unsupport data type")
		
		self.data = data
		self.xmax = base
		self.x_ticks = x_ticks
		self.x_labels = columns
		self.threshold = threshold
		self.value_type = value_type
		self.color = color
		self.threshold_line_color = threshold_line_color
		self.plus_minus = plus_minus
		self.xticklabels = xticklabels
		self.yticklabels = yticklabels

	def plot(self, ax, kws):
		ax.set(xlim=(0, self.xmax))
		if self.xticklabels:
			if self.x_ticks != []:
				ax.set(xticks=self.xticks)
				ax.set_xticklabels(self.x_labels)
		else:
			ax.set_xticklabels([])
		
		if not yticklabels:
			ax.set_yticklabels([])
		

		
