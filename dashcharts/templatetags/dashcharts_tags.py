import json
import posixpath
from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe
from django.utils import six
from django.conf import settings

from ..views.base import Chart
from ..views.datatable import DataTable

try:
    DASHCHARTS_JS_REL_PATH = settings. DASHCHARTS_JS_REL_PATH
    if  DASHCHARTS_JS_REL_PATH[0] == '/':
         DASHCHARTS_JS_REL_PATH =  DASHCHARTS_JS_REL_PATH[1:]
except AttributeError:
     DASHCHARTS_JS_REL_PATH = 'dashcharts/js/'

CHART_LOADER_URL = posixpath.join(settings.STATIC_URL,
                                   DASHCHARTS_JS_REL_PATH,
                                  'chartloader.js')

TABLE_LOADER_URL = posixpath.join(settings.STATIC_URL,
                                   DASHCHARTS_JS_REL_PATH,
                                  'tableloader.js')


def json_serializer(obj):
    """
        Return JSON representation of some special data types.
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


register = template.Library()


@register.filter
def load_charts(chart_list=None, render_to=''):
    """Loads the ``Chart`` objects in the ``chart_list`` to the
    HTML elements with id's specified in ``render_to``.
    :Arguments:
    - **chart_list** - a list of Chart objects. If there is just a
      single element, the Chart object can be passed directly
      instead of a list with a single element.
    - **render_to** - a comma separated string of HTML element id's where the
      charts needs to be rendered to. If the element id of a specific chart
      is already defined during the chart creation, the ``render_to`` for that
      specific chart can be an empty string or a space.
      For example, ``render_to = 'container1, , container3'`` renders three
      charts to three locations in the HTML page. The first one will be
      rendered in the HTML element with id ``container1``, the second
      one to it's default location that was specified in ``chart_options``
      when the Chart/PivotChart object was created, and the third one in the
      element with id ``container3``.
    :returns:
    - a JSON array of the HighCharts Chart options. Also returns a link
      to the ``chartloader.js`` javascript file to be embedded in the webpage.
      The ``chartloader.js`` has a jQuery script that renders a HighChart for
      each of the options in the JSON array"""

    embed_script = (
        '<script type="text/javascript">\n'
        'var _dashcharts_hco_array = %s;\n</script>\n'
        '<script src="%s" type="text/javascript">\n</script>')
    
    if chart_list is not None:
        if isinstance(chart_list, Chart):
            chart_list = [chart_list]
        chart_list = [{'chart': c.get_hc_options()} for c in chart_list]
        render_to_list = [s.strip() for s in render_to.split(',')]
        for hco, render_to in six.moves.zip_longest(
                chart_list, render_to_list):
            if render_to:
                hco['renderTo'] = render_to
                
        embed_script = (embed_script % (json.dumps(chart_list,
                                                   default=json_serializer),
                                        CHART_LOADER_URL))
    else:
        embed_script = embed_script % ((), CHART_LOADER_URL)
    
    return mark_safe(embed_script)


@register.filter
def load_tables(table_list=None, render_to=''):
    embed_script = (
        '<script type="text/javascript">\n'
        'var _dashcharts_datatable_array = %s;\n</script>\n'
        '<script src="%s" type="text/javascript">\n</script>')
    
    if table_list is not None:
        if isinstance(table_list, DataTable):
            table_list = [table_list]
        table_list = [{'table': t.get_datatable_options()} for t in table_list]
        render_to_list = [s.strip() for s in render_to.split(',')]
        for hco, render_to in six.moves.zip_longest(
                table_list, render_to_list):
            if render_to:
                hco['renderTo'] = render_to
                
        embed_script = (embed_script % (json.dumps(table_list,
                                                   default=json_serializer),
                                        TABLE_LOADER_URL))
    else:
        embed_script = embed_script % ((), TABLE_LOADER_URL)
    
    return mark_safe(embed_script)
