"""
The pie/doughnut chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json



class PieDoughnutChart(Chart):
    """
    Making the JSON necessary for a pie or doughnut chart
    DOCS: http://www.chartjs.org/docs/#doughnut-pie-chart-introduction
    """

    """
The bar chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json


class PieChart(Chart):
    def __init__(self, **kwargs):
        super().__init__(chart_type="pie", **kwargs)

    def get_options(self):
        """Gets the options for the chart"""
        return self.options

    def get_data(self):
        """Populating self.data with self.datasets"""
        data = []
        for i, name in enumerate(self.datasets):
            dataset = {'name': name, 'y': self.datasets[name]}
            data.append(dataset)
        self.data = [{'data': data}]
        return self.data

    def make_context(self):
        """Making the context to be returned to the render functions"""
        self.context = {
            'chart_type': self.chart_type,
            'chart_name': self.chart_name,
            'chart_labels': json.dumps(self.chart_labels),
            'data': json.dumps(self.data),
            'options': json.dumps(self.options)
        }
        self.context.update(self.options)
        return self.context

    def get_hc_options(self):
        self.get_data()
        print("series", self.data)
        options = {    
            "chart": {"type": self.chart_type},
            "series": self.data
        }
        options.update(self.options)
        return options

    def to_string(self):
        """Rendering bar chart data to a template, returning string"""
        self.get_options()
        self.get_data()
        self.make_context()
        return render_to_string('dashcharts/chart.html', self.context)
