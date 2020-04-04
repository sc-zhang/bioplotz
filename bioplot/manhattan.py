import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


__all__ = ["manhattan"]


class _Manhattan(object):
	def __init__(self, data, threshold=0.05, value_type="p-value", color=['orange', 'green'], threshold_line_color='blue', log_base=2, plus_minus=False, xticklabels=True, yticklabels=True):
		if log_base < 0:
			raise ValueError("log base must be greater than or equal 0")
		'''
		data can be types show follow:
			{'x': [], 'y': []}
			{'chr': [[], []]}
			{'chr': {'x': [], 'y': []}}
			[[], []]
		'''
		if isinstance(data, pd.DataFrame):
			continue
		elif isinstance(data, dict):
			base = 0
			columns = sorted(data)
			if '-'.join(sorted(columns)).lower() == 'x-y':
				if not isinstance(data[columns[0]], list):
					raise ValueError("Data must be two list for x values and y values")
				for key in columns:
					if key.lower() == 'y' and log_base != 0:
						data[key] = np.log(data[key])/np.log(log_base)		
			elif isinstance(data[columns[0]], list):
				for key in columns:
					if not isinstance(data[key][0], list):
						raise ValueError("Data must be two list for x values and y values")
					data[key][0] = np.add(data[key][0], base)
					base = max(data[key][0])
					if log_base != 0:
						data[key][1] = np.log(data[key][1])/np.log(log_base)
			elif isinstance(data[columns[0]], dict):
				for key in columns:
					if len(data[key]) != 2 or '-'.join(sorted(data[key])).lower() != 'x-y':
						raise KeyError("Keys must be 'X/x' and 'Y/y'")
					for sub_key in data[key]:
						if sub_key.lower() == 'x':
							data[key][sub_key] = np.add(data[key][sub_key], base)
							base = max(data[key][sub_key])
						else:
							if log_base != 0:
								data[key][sub_key] = np.log(data[key][sub_key])/np.log(log_base)
			else:
				raise ValueError("Unsupport data type")
			data = pd.DataFrame(data, columns=columns)
		elif isinstance(data, list):
			if not isinstance(data[0], list):
				raise ValueError("Data must be two list for x values and y values")
			if log_base != 0:
				data[1] = np.log(data[1])/np.log(log_base)
		else:
			raise ValueError("Unsupport data type")

			
