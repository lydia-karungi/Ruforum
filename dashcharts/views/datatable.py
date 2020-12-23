from django.template.loader import render_to_string
import json

class DataTable(object):
    """A base class for tables, init will store all the data needed for subclasses"""

    def __init__(self, table_name=None, options=None, \
        table_columns=None, dataset=None):
        """
        Setting all of the settings that will be needed in the tables subclasses
        """
        self.dataset = dataset
        self.table_name = table_name
        self.options = options or {}
        self.table_columns = table_columns
        
        # Figure out how to access the kwargs as a list and make sure none of them
        # are None. Raise exception if they are and test.
        if not all([self.table_name, self.table_columns, self.dataset]):
            raise Exception(
                "Chart class needs to have all keyword arguments specified")

    def get_options(self):
        """Gets the options for the datatable"""
        return self.options

    def get_data(self):
        """Populating self.data with self.datasets"""
        self.data = self.dataset
        return self.data

    def make_context(self):
        """Making the context to be returned to the render functions"""
        self.context = {
            'table_name': self.table_name,
            'table_columns': json.dumps(self.table_columns),
            'data': json.dumps(self.data),
            'options': json.dumps(self.options)
        }
        return self.context

    def get_datatable_options(self):
        """Making the context to be returned to the render functions"""
        self.get_data()
        print("series", self.data)
        return {
            "columns": self.table_columns,
            "data": self.data
        }

    def to_string(self):
        self.get_options()
        self.get_data()
        self.make_context()
        return render_to_string('dashcharts/table.html', self.context)