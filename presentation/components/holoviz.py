import holoviews as hv
import hvplot.pandas  # noqa
import hvplot.xarray  # noqa
import numpy as np
import panel as pn
import param
import xarray as xr
from bokeh.sampledata.sprint import sprint
from holoviews import opts, streams
from holoviews.plotting.links import DataLink
from .base import ComponentBase

air = xr.tutorial.open_dataset("air_temperature").load().air

class Datashader(ComponentBase):
    component = param.Parameter(pn.pane.HoloViews)
    reference = param.String("https://panel.holoviz.org/reference/panes/HoloViews.html")
    imports = """\
import hvplot.xarray  # noqa
import panel as pn
import xarray as xr

pn.extension(sizing_mode="stretch_width")

air = xr.tutorial.open_dataset("air_temperature").load().air
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plot = (
                air.hvplot.scatter(
                    "time",
                    groupby=[],
                    rasterize=True,
                    dynspread=True,
                    responsive=True,
                    cmap="YlOrBr",
                    colorbar=True,
                )
                * air.mean(["lat", "lon"]).hvplot.line(
                    "time", color=accent_base_color, responsive=True
                )
            )
            plot.opts(responsive=True, active_tools=["box_zoom"])
            return plot

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.HoloViews(plot, min_height=400, sizing_mode="stretch_both")
        return component


class HoloViews(ComponentBase):
    component = param.Parameter(pn.pane.HoloViews)
    reference = param.String("https://panel.holoviz.org/reference/panes/HoloViews.html")
    imports = """\
import holoviews as hv
import numpy as np
import panel as pn
from holoviews import opts, streams
from holoviews.plotting.links import DataLink

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            curve = hv.Curve(np.random.randn(10).cumsum()).opts(
                responsive=True,
                line_width=6,
                color=accent_base_color,
                # https://github.com/holoviz/holoviews/issues/5058
                # active_tools=["point_draw"]
            )
            if theme == "default":
                point_color = "black"
            else:
                point_color = "#E5E5E5"

            streams.CurveEdit(
                data=curve.columns(), source=curve, style={"color": point_color, "size": 10}
            )

            table = hv.Table(curve).opts(editable=True)
            DataLink(curve, table)

            return (curve + table).opts(
                opts.Table(editable=True),
            )

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.HoloViews(plot, height=500, sizing_mode="stretch_both")
        return component


class HVPlot(ComponentBase):
    component = param.Parameter(pn.pane.HoloViews)
    reference = param.String("https://panel.holoviz.org/reference/panes/HoloViews.html")
    imports = """\
import hvplot.pandas  # noqa
import panel as pn

from bokeh.sampledata.sprint import sprint

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            return sprint.hvplot.violin(
                y="Time",
                by="Medal",
                c="Medal",
                ylabel="Sprint Time",
                cmap=["gold", "silver", "brown"],
                legend=False,
                responsive=True,
                padding=0.4,
            )

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.HoloViews(plot, height=500, sizing_mode="stretch_both")
        return component


ALL = {
    # "COLORCET": HVPlot,
    "DATASHADER": Datashader,
    # "GEOVIEWS": HVPlot,
    "HOLOVIEWS": HoloViews,
    "HVPLOT": HVPlot,
    # "PANEL": HVPlot,
    # "PARAM": HVPlot,
}