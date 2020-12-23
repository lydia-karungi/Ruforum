"""
Charting engine which takes the input and routes it to the proper Chart sublcass.
"""
from .line import LineChart
from .bar import BarChart
from .column import ColumnChart
from .pie import PieChart
from .base import Chart
from .datatable import DataTable


class ChartEngine(object):
	"""An engine to make all of the charts necessary"""

	def __init__(self, **kwargs):
		"""take in chart options and decide what kind of chart to make"""
		charts = {
			'line': LineChart,
			'bar': BarChart,
			'column': ColumnChart,
			'pie': PieChart,
		}

		self.chart = charts[kwargs['chart_type']](
			chart_name=kwargs['chart_name'],
			chart_labels=kwargs['chart_labels'],
			# Options is not used but left for possible future use
			options=kwargs.get('options') or {},
			datasets=kwargs['datasets'])


	def make_chart(self):
		"""Render the proper chart from the given"""
		return self.chart.to_string()


class TableEngine(object):
	"""An engine to make all of the charts necessary"""

	def __init__(self, **kwargs):
		"""take in chart options and decide what kind of chart to make"""
		self.table = DataTable(
			table_name=kwargs['table_name'],
			table_columns=kwargs['table_columns'],
			# Options is not used but left for possible future use
			options=kwargs.get('options'),
			dataset=kwargs['dataset'])


	def make_table(self):
		"""Render the proper chart from the given"""
		return self.datatable.to_string()