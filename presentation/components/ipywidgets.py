import json
from json import load
from urllib.request import urlopen

# import ipywidgets as ipw
import ipysheet
import pandas as pd
import panel as pn
import param
from ipydatagrid import DataGrid

import ipywidgets as ipw

from .base import ComponentBase


class IPyWidgets(ComponentBase):
    component = param.Parameter(pn.pane.IPyWidget)
    reference = param.String("https://panel.holoviz.org/reference/panes/IPyWidget.html")
    docs = param.String("https://github.com/QuantStack/ipysheet")
    imports = """\
import numpy as np
import panel as pn
import ipywidgets as ipw

pn.extension("ipywidgets", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_widget(theme="default", accent_base_color="blue"):
            date   = ipw.DatePicker(description='Date')
            slider = ipw.IntSlider(description='Slider', min=-5, max=5)

            @pn.depends(date)
            def date_text(value):
                if not value:
                    return "Please select a date"
                return str(value) + " was selected"

            @pn.depends(slider)
            def slider_text(value):
                return 'The slider value is ' + (
                    'negative' if value < 0 else 'nonnegative'
                ) + f": {value=}."

            return pn.Column(
                pn.Row(date, date_text),
                pn.Row(slider, slider_text)
            )

        widget = get_widget(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.panel(widget, height=500, sizing_mode="stretch_both")
        return component

class IPySheet(ComponentBase):
    component = param.Parameter(pn.pane.IPyWidget)
    reference = param.String("https://panel.holoviz.org/reference/panes/IPyWidget.html")
    docs = param.String("https://ipysheet.readthedocs.io/en/latest/")
    imports = """\
import panel as pn
import ipywidgets as ipw
import ipysheet

pn.extension("ipywidgets", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_widget(theme="default", accent_base_color="blue"):
            slider = pn.widgets.FloatSlider(value=10, start=0, end=100)
            sheet = ipysheet.sheet()

            ipysheet.cell(1,1, "Input")
            cell3 = ipysheet.cell(1,2, 42.)
            ipysheet.cell(2,1, "Output")
            cell_sum = ipysheet.cell(2,2, 52., read_only=True, background_color=accent_base_color)

            @pn.depends(slider, cell3, watch=True)
            def calculate(a,b):
                cell_sum.value = a+b
                print("update", cell_sum.value)

            return pn.Column(slider, sheet)

        widget = get_widget(theme=theme, accent_base_color=accent_base_color)
        component = pn.panel(widget, height=500, sizing_mode="stretch_both")
        return component

class IPyDataGrid(ComponentBase):
    component = param.Parameter(pn.pane.IPyWidget)
    reference = param.String("https://panel.holoviz.org/reference/panes/IPyWidget.html")
    docs = param.String("https://github.com/bloomberg/ipydatagrid")
    imports = """\
from ipydatagrid import DataGrid
from json import load
import panel as pn
import pandas as pd
from urllib.request import urlopen
import json

pn.extension("ipywidgets", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_widget(theme="default", accent_base_color="blue"):

            url = "https://raw.githubusercontent.com/bloomberg/ipydatagrid/main/examples/cars.json"
            response = urlopen(url)
            json_data = response.read().decode('utf-8', 'replace')
            data = json.loads(json_data)

            df = (
                pd.DataFrame(data["data"])
                .drop("index", axis=1)
            )

            datagrid = DataGrid(df, selection_mode="cell")

            return pn.pane.IPyWidget(datagrid)

        widget = get_widget(theme=theme, accent_base_color=accent_base_color)
        component = pn.panel(widget, height=500, width=500, sizing_mode="fixed")
        return component


ALL = {
    # "IPYDATAGRID": IPyDataGrid, # Not working: https://github.com/holoviz/panel/issues/2641
    "IPYSHEET": IPySheet,
    "IPyWidgets": IPyWidgets,
}
