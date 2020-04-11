import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


__all__ = ["manhattan"]


class _Manhattan(object):
	def __init__(self, data, threshold=0.05, color=['orange', 'green'], threshold_line_color='blue', log_base=2, plus_minus=False, xticklabels=True, yticklabels=True):
		if log_base < 0:
			raise ValueError("log base must be greater than or equal 0")
		columns = []
		x_ticks = []
		x_max = 0
		y_min = 0
		y_max = 0
		tmp_y = []
		'''
		Convert data to pd.DataFrame
		'''
		if isinstance(data, pd.DataFrame):
			columns = list(data.columns)
			if isinstance(columns[0], int):
				columns = []
				x_max = max(data[0])
				if log_base != 0:
					data[1] = -np.log(data[1])/np.log(log_base)
				tmp_y.extend(data[1])
			else:
				for col in columns:
					data[col][0] = np.add(data[col][0], x_max)
					x_ticks.append((max(data[col][0])-x_max)/2+x_max)
					x_max = max(data[col][0])
					if log_base != 0:
						data[col][1] = -np.log(data[col][1])/np.log(log_base)
					tmp_y.extend(data[col][1])
		elif isinstance(data, dict):
			columns = sorted(data)
			data = pd.DataFrame(data, columns=columns)
			for col in columns:
				data[col][0] = np.add(data[col][0], x_max)
				x_ticks.append((max(data[col][0])-x_max)/2+x_max)
				x_max = max(data[col][0])
				if log_base != 0:
					data[col][1] = -np.log(data[col][1])/np.log(log_base)
				tmp_y.extend(data[col][1])
		elif isinstance(data, list) or isinstance(data, np.ndarray):
			columns = []
			data = pd.DataFrame(data)
			x_max = max(data[0])
			if log_base != 0:
				data[1] = -np.log(data[1])/np.log(log_base)
			tmp_y.extend(data[1])
		else:
			raise ValueError("Unsupport data type")
		
		if not isinstance(threshold, list):
			threshold = [threshold]
		
		if plus_minus:
			threshold_values = {'plus': {}, 'minus': {}}
			y_values = {'plus': [], 'minus': []}
			for y in tmp_y:
				if y < 0:
					y_values['minus'].append(y)
				else:
					y_values['plus'].append(y)
			idx = int(len(tmp_y)*th)
			for th in threshold:
				for type in y_values:
					if type == 'minus':
						y_values[type] = sorted(y_values[type])
					else:
						y_values[type] = sorted(y_values[type], reverse=True)
					
					threshold_values[type][th] = y_values[type][idx]
		else:
			threshold_values = {}
			if max(tmp_y) < 0:
				y_values = sorted(tmp_y)
			else:
				y_values = sorted(tmp_y, reverse=True)
			for th in threshold:
				idx = int(len(y_values)*th)
				threshold_values[th] = y_values[idx]
		if not isinstance(threshold_line_color, list):
			threshold_line_color = [threshold_line_color]
		
		self.data = data
		self.xlim = (0, x_max)
		self.xmax = x_max
		y_min = min(tmp_y)
		y_max = max(tmp_y)
		self.ymin = y_min
		self.ymax = y_max		
		if not plus_minus:
			if max(tmp_y) < 0:
				y_max = 0
			else:
				y_min = 0
		self.ylim = (y_min, y_max)
		self.x_ticks = x_ticks
		self.x_labels = columns
		self.color = color
		self.plus_minus = plus_minus
		self.threshold = threshold
		self.threshold_values = threshold_values
		self.threshold_line_color = threshold_line_color
		self.xticklabels = xticklabels
		self.yticklabels = yticklabels

	def plot(self, ax):
		data = self.data
		ax.set(xlim=self.xlim)

		if len(self.ylim) != 0:
			ax.set(ylim=self.ylim)
		if self.xticklabels:
			if self.x_ticks != []:
				ax.set(xticks=self.x_ticks)
				ax.set_xticklabels(self.x_labels)
		else:
			ax.set_xticklabels([])
		
		if not self.yticklabels:
			ax.set_yticklabels([])
		
		# Plot scatter of values
		if self.x_labels == []:
			if isinstance(self.color, list):
				color = self.color[0]
			else:
				color = self.color
			ax.scatter(data[0], data[1], color=color, marker='.', s=1)
			ax.tick_params(axis='both', which='both',length=0)
		else:
			if isinstance(self.color, list):
				color_cnt = len(self.color)
				for i in range(0, len(self.x_labels)):
					col = self.x_labels[i]
					color_idx = i%color_cnt
					ax.scatter(data[col][0], data[col][1], color=self.color[color_idx], marker='.', s=1)
					if color_cnt == 1:
						x = max(data[col][0])
						ax.plot([x, x], [self.ymin, self.ymax], color='lightgrey', linewidth=0.8, linestyle=':')
			else:
				for col in self.x_labels:
					ax.scatter(data[col][0], data[col][1], color=self.color, marker='.', s=1)
					x = max(data[col][0])
					ax.plot([x, x], [self.ymin, self.ymax], color='lightgrey', linewidth=0.8, linestyle=':')

		#Plot thresholds
		color_cnt = len(self.threshold_line_color)
		for i in range(0, len(self.threshold)):
			th = self.threshold[i]
			color_idx = i%color_cnt
			if self.plus_minus:
				ax.plot([0, self.xmax], [0, 0], color='lightgrey', linewidth=0.5)
				for type in self.threshold_values:
					ax.plot([0, self.xmax], [self.threshold_values[type][th], self.threshold_values[type][th]], color=self.threshold_line_color[color_idx], linewidth=0.8, linestyle=':')
			else:
				ax.plot([0, self.xmax], [self.threshold_values[th], self.threshold_values[th]], color=self.threshold_line_color[color_idx], linewidth=0.8, linestyle=':')

		ax.spines['top'].set_linewidth(0.5)
		ax.spines['top'].set_color('lightgrey')
		ax.spines['bottom'].set_linewidth(0.5)
		ax.spines['bottom'].set_color('lightgrey')
		ax.spines['left'].set_linewidth(0.5)
		ax.spines['left'].set_color('lightgrey')
		ax.spines['right'].set_linewidth(0.5)
		ax.spines['right'].set_color('lightgrey')
		

def manhattan(data, threshold=0.05, color=['orange', 'green'], 
              threshold_line_color='blue', log_base=2, 
			  plus_minus=False, xticklabels=True, yticklabels=True, ax=None):

	plotter = _Manhattan(data, threshold, color, threshold_line_color, 
	                     log_base, plus_minus, xticklabels, yticklabels)
	
	if ax is None:
		ax = plt.gca()
	plotter.plot(ax)

	return ax, plotter.threshold_values
