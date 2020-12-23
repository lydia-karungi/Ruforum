class Chart(object):
    """A base class for charts, init will store all the data needed for subclasses"""

    def __init__(self, chart_type=None, chart_name=None, options=None, \
        chart_labels=None, datasets=None):
        """
        Setting all of the settings that will be needed in the charts subclasses
        """
        default_options = {
            'exporting':  {
                'chartOptions': { 
                    'plotOptions': {
                        'series': {
                            'dataLabels': {
                                'enabled': True
                            }
                        }
                    }
                },
                'fallbackToExportServer': False
            }
        }    
        self.chart_type = chart_type
        # datasets will be put into self.data in each charts get_data method
        self.datasets = datasets
        self.chart_name = chart_name
        self.options = default_options
        print("optionszz", options)
        if options:
            self.options.update(options)
        self.chart_labels = chart_labels
        self.data = []
        
        # Figure out how to access the kwargs as a list and make sure none of them
        # are None. Raise exception if they are and test.
        if not all([self.chart_type, self.chart_name, self.datasets]):
            raise Exception(
                "Chart class needs to have all keyword arguments specified")


    def to_string(self):
        """
        This method is meant to be overridden in the child chart type classes
        """
        raise Exception("to_string method has not been overridden")
