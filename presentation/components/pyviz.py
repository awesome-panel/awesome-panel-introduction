import json
from html import escape  # noqa

import altair as alt
import folium
import holoviews as hv
import hvplot.pandas  # noqa
import hvplot.xarray  # noqa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import panel as pn
import param
import plotly.express as px
import pydeck
import pyvista as pv
import seaborn as sns
import vtk
import xarray as xr
from bokeh.plotting import figure
from bokeh.sampledata.sprint import sprint
from holoviews import opts, streams
from holoviews.plotting.links import DataLink
from matplotlib import cm
from matplotlib.backends.backend_agg import \
    FigureCanvas  # not needed for mpl >= 3.1
from matplotlib.figure import Figure
from plotnine import (aes, element_rect, facet_wrap, geom_point, ggplot,
                      stat_smooth, themes)
from plotnine.data import mtcars
from pyecharts.charts import Bar
from scipy.integrate import odeint
from vega_datasets import data
from vtk.util.colors import tomato
from .base import ComponentBase

penguins = sns.load_dataset("penguins")
air = xr.tutorial.open_dataset("air_temperature").load().air

class Altair(ComponentBase):
    component = param.Parameter("pn.pane.Vega")
    reference = param.String("https://panel.holoviz.org/reference/panes/Vega.html#altair")
    extension = param.String("vega")
    imports = param.String(
        """\
import altair as alt
import panel as pn

from vega_datasets import data

pn.extension("vega", sizing_mode="stretch_width")
"""
    )

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            if theme == "dark":
                alt.themes.enable("dark")
            else:
                alt.themes.enable("default")

            return (
                alt.Chart(data.cars())
                .mark_circle(size=60)
                .encode(
                    x="Horsepower",
                    y="Miles_per_Gallon",
                    color="Origin",
                    tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
                )
                .properties(
                    height="container",
                    width="container",
                )
                .interactive()
            )

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Vega(plot, height=500, sizing_mode="stretch_both")
        return component


class Bokeh(ComponentBase):
    component = param.Parameter(pn.pane.Bokeh)
    reference = param.String("https://panel.holoviz.org/")
    imports = """\
import numpy as np
import panel as pn

from bokeh.plotting import figure
from scipy.integrate import odeint

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            sigma = 10
            rho = 28
            beta = 8.0 / 3
            theta = 3 * np.pi / 4

            def lorenz(xyz, t):
                x, y, z = xyz
                x_dot = sigma * (y - x)
                y_dot = x * rho - x * z - y
                z_dot = x * y - beta * z
                return [x_dot, y_dot, z_dot]

            initial = (-10, -7, 35)
            t = np.arange(0, 100, 0.006)

            solution = odeint(lorenz, initial, t)

            x = solution[:, 0]
            y = solution[:, 1]
            z = solution[:, 2]
            xprime = np.cos(theta) * x - np.sin(theta) * y

            colors = [
                "#C6DBEF",
                "#9ECAE1",
                "#6BAED6",
                "#4292C6",
                "#2171B5",
                "#08519C",
                "#08306B",
            ]

            plot = figure(
                title="Lorenz attractor example", tools=["pan,wheel_zoom,box_zoom,reset,hover"]
            )

            plot.multi_line(
                np.array_split(xprime, 7),
                np.array_split(z, 7),
                line_color=colors,
                line_alpha=0.8,
                line_width=1.5,
            )
            return plot

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Bokeh(plot, height=500, sizing_mode="stretch_both")
        return component


class DeckGL(ComponentBase):
    component = param.Parameter(pn.pane.DeckGL)
    reference = param.String("https://panel.holoviz.org/reference/panes/DeckGL.html")
    extension = param.String("deckgl")
    imports = """\
import panel as pn

pn.extension("deckgl", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        # Please create your own access token one your own Access tokens page
        # https://account.mapbox.com/access-tokens/
        MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"

        def get_plot(theme="default", accent_base_color="blue"):
            if theme == "dark":
                deckgl_map_style = "mapbox://styles/mapbox/dark-v9"
            else:
                deckgl_map_style = "mapbox://styles/mapbox/light-v9"

            return {
                "initialViewState": {
                    "bearing": -27.36,
                    "latitude": 52.2323,
                    "longitude": -1.415,
                    "maxZoom": 15,
                    "minZoom": 5,
                    "pitch": 40.5,
                    "zoom": 6,
                },
                "layers": [
                    {
                        "@@type": "HexagonLayer",
                        "autoHighlight": True,
                        "coverage": 1,
                        "data": "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv",
                        "elevationRange": [0, 3000],
                        "elevationScale": 50,
                        "extruded": True,
                        "getPosition": "@@=[lng, lat]",
                        "id": "8a553b25-ef3a-489c-bbe2-e102d18a3211",
                        "pickable": True,
                    }
                ],
                "mapStyle": deckgl_map_style,
                "views": [{"@@type": "MapView", "controller": True}],
            }

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.DeckGL(
            plot, mapbox_api_key=MAPBOX_KEY, sizing_mode="stretch_both", height=500
        )
        return component


class ECharts(ComponentBase):
    component = param.Parameter(pn.pane.ECharts)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/ECharts.html#panes-gallery-echarts"
    )
    extension = param.String("echarts")
    imports = """\
import panel as pn

pn.extension("echarts", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            return {
                "xAxis": {"data": ["2017-10-24", "2017-10-25", "2017-10-26", "2017-10-27"]},
                "yAxis": {},
                "series": [
                    {
                        "type": "k",
                        "data": [
                            [20, 34, 10, 38],
                            [40, 35, 30, 50],
                            [31, 38, 33, 44],
                            [38, 15, 5, 42],
                        ],
                    }
                ],
                "responsive": True,
            }

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.ECharts(plot, min_height=500, sizing_mode="stretch_both")
        return component

class Folium(ComponentBase):
    component = param.Parameter("panel.pane.plot.Folium")
    reference = param.String(
        "https://panel.holoviz.org/gallery/external/Folium.html"
    )
    extension = param.String()
    imports = """\
import folium as fm
import panel as pn

from html import escape # noqa

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plot = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain") #,  width='100%', height="50%")

            folium.Marker(
                location=[45.3288, -121.6625],
                popup="Mt. Hood Meadows",
                icon=folium.Icon(icon="cloud"),
            ).add_to(plot)

            folium.Marker(
                location=[45.3311, -121.7113],
                popup="Timberline Lodge",
                icon=folium.Icon(color="green"),
            ).add_to(plot)

            folium.Marker(
                location=[45.3300, -121.6823],
                popup="Some Other Location",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(plot)
            return plot

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)

        def _get_properties(self):
            properties = pn.pane.HTML._get_properties(self)
            text = '' if self.object is None else self.object
            if hasattr(text, '_repr_html_'):
                text = text._repr_html_()
                before = '<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;">'
                after = '<div style="width:100%;height:100%"><div style="position:relative;width:100%;height:100%;padding-bottom:0%;">'
                text=text.replace(before, after)
            return dict(properties, text=escape(text))

        pn.pane.plot.Folium._get_properties=_get_properties
        component = pn.pane.plot.Folium(plot, min_height=500, sizing_mode="stretch_both")
        return component

class Matplotlib(ComponentBase):
    component = param.Parameter(pn.pane.Matplotlib)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib"
    )
    imports = """\
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_agg import \
    FigureCanvas  # not needed for mpl >= 3.1
from matplotlib.figure import Figure
import panel as pn

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plt.style.use("default")
            if theme == "dark":
                plt.style.use("dark_background")
            Y, X = np.mgrid[-3:3:100j, -3:3:100j]
            U = -1 - X ** 2 + Y
            V = 1 + X - Y ** 2
            speed = np.sqrt(U * U + V * V)

            fig0 = Figure(figsize=(12, 6))
            ax0 = fig0.subplots()
            FigureCanvas(fig0)  # not needed for mpl >= 3.1

            strm = ax0.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
            fig0.colorbar(strm.lines)
            return fig0

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Matplotlib(plot, height=500, sizing_mode="stretch_both")
        return component


class Plotly(ComponentBase):
    component = param.Parameter(pn.pane.Plotly)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/Plotly.html#panes-gallery-plotly"
    )
    extension = param.String("plotly")
    imports = """\
import pandas as pd
import panel as pn

import plotly.express as px

pn.extension("plotly", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            data = pd.DataFrame(
                [
                    ("Monday", 7),
                    ("Tuesday", 4),
                    ("Wednesday", 9),
                    ("Thursday", 4),
                    ("Friday", 4),
                    ("Saturday", 4),
                    ("Sunay", 4),
                ],
                columns=["Day", "Orders"],
            )

            if theme == "dark":
                plotly_template = "plotly_dark"
            else:
                plotly_template = "plotly"

            fig = px.line(
                data,
                x="Day",
                y="Orders",
                template=plotly_template,
                color_discrete_sequence=(accent_base_color,),
            )
            fig.update_traces(mode="lines+markers", marker=dict(size=10), line=dict(width=4))
            fig.layout.autosize = True
            return fig

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Plotly(plot, config={"responsive": True})
        return component


class Plotnine(ComponentBase):
    component = param.Parameter(pn.pane.Matplotlib)
    docs = param.String("https://plotnine.readthedocs.io/en/stable/")
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib"
    )
    imports = """\
import matplotlib.pyplot as plt
import panel as pn

from plotnine import (aes, element_rect, facet_wrap, geom_point, ggplot, stat_smooth, themes)
from plotnine.data import mtcars

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plt.style.use("default")
            if theme == "dark":
                plotnine_theme = themes.theme_dark() + themes.theme(
                    plot_background=element_rect(fill="black", alpha=0)
                )
            else:
                plotnine_theme = themes.theme_xkcd()

            plot = (
                (
                    ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
                    + geom_point()
                    + stat_smooth(method="lm")
                    + facet_wrap("~gear")
                )
                + plotnine_theme
                + themes.theme(figure_size=(16, 8))
            )
            return plot.draw()

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Matplotlib(plot, height=500, sizing_mode="stretch_both")
        return component


class PyDeck(ComponentBase):
    component = param.Parameter(pn.pane.DeckGL)
    reference = param.String("https://panel.holoviz.org/reference/panes/DeckGL.html#pydeck")
    extension = param.String("deckgl")

    imports = """\
import pydeck
import panel as pn

pn.extension("deckgl", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            LAND_COVER = [
                [[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]
            ]
            polygon = pydeck.Layer(
                "PolygonLayer",
                LAND_COVER,
                stroked=False,
                # processes the data as a flat longitude-latitude pair
                get_polygon="-",
                get_fill_color=[0, 0, 0, 20],
            )

            DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
            geojson = pydeck.Layer(
                "GeoJsonLayer",
                DATA_URL,
                opacity=0.8,
                stroked=False,
                filled=True,
                extruded=True,
                wireframe=True,
                get_elevation="properties.valuePerSqm / 20",
                get_fill_color="[255, 255, properties.growth * 255]",
                get_line_color=[255, 255, 255],
                pickable=True,
            )

            if theme == "dark":
                deckgl_map_style = "mapbox://styles/mapbox/dark-v9"
            else:
                deckgl_map_style = "mapbox://styles/mapbox/light-v9"
            MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"
            INITIAL_VIEW_STATE = pydeck.ViewState(
                latitude=49.254, longitude=-123.13, zoom=11, max_zoom=16, pitch=45, bearing=0
            )

            r = pydeck.Deck(
                api_keys={"mapbox": MAPBOX_KEY},
                layers=[polygon, geojson],
                initial_view_state=INITIAL_VIEW_STATE,
                map_style=deckgl_map_style,
            )

            # Tooltip (you can get the id directly from the layer object)
            geojson_tooltip = {
                "html": """
                <b>Value per Square meter:</b> {properties.valuePerSqm}<br>
                <b>Growth:</b> {properties.growth}
                """,
                "style": {"backgroundColor": accent_base_color, "color": "white"},
            }
            tooltips = {geojson.id: geojson_tooltip}
            return r, tooltips

        plot, tooltips = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.DeckGL(plot, tooltips=tooltips, height=500, sizing_mode="stretch_both")
        return component


class PyECharts(ComponentBase):
    component = param.Parameter(pn.pane.ECharts)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/ECharts.html#panes-gallery-echarts"
    )
    extension = param.String("echarts")
    imports = """\
import json
import panel as pn

from pyecharts.charts import Bar

pn.extension("echarts", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plot = (
                Bar()
                .add_xaxis(["Helicoptors", "Planes", "Air Ballons"])
                .add_yaxis("Total In Flight", [50, 75, 25], color=accent_base_color)
            )

            # Workaround to make plot responsive
            plot = json.loads(plot.dump_options())
            plot["responsive"] = True
            return plot

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.ECharts(plot, min_height=500, sizing_mode="stretch_both", theme=theme)
        return component


class PyVista(ComponentBase):
    component = param.Parameter(pn.pane.VTK)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/VTK.html#working-with-pyvista"
    )
    extension = param.String("vtk")
    imports = """\
import json
import panel as pn

from pyecharts.charts import Bar

pn.extension("vtk", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            plotter = pv.Plotter()  # we define a pyvista plotter
            if theme == "dark":
                plotter.background_color = (0.13, 0.13, 0.13)
            else:
                plotter.background_color = (0.97, 0.97, 0.97)

            # we create a `VTK` panel around the render window
            pvcylinder = pv.Cylinder(resolution=8, direction=(0, 1, 0))
            cylinder_actor = plotter.add_mesh(
                pvcylinder, color=accent_base_color, smooth_shading=True
            )
            cylinder_actor.RotateX(30.0)
            cylinder_actor.RotateY(-45.0)
            plotter.add_mesh(
                pv.Sphere(theta_resolution=8, phi_resolution=8, center=(0.5, 0.5, 0.5)),
                color=accent_base_color,
                smooth_shading=True,
            )
            return plotter.ren_win

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.panel(plot, height=500, sizing_mode="stretch_both")
        return component


class Seaborn(ComponentBase):
    component = param.Parameter(pn.pane.Matplotlib)
    reference = param.String(
        "https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib"
    )
    imports = """\
import matplotlib.pyplot as plt

import panel as pn
import seaborn as sns

pn.extension(sizing_mode="stretch_width")

penguins = sns.load_dataset("penguins")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            if theme == "dark":
                sns.set_style("darkgrid")
                plt.style.use("dark_background")
            else:
                plt.style.use("default")
                sns.set_style("whitegrid")

            plot = sns.displot(penguins, x="flipper_length_mm", color=accent_base_color)
            fig0 = plot.fig
            fig0.set_size_inches(16, 8)
            return fig0

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Matplotlib(plot, sizing_mode="stretch_both")
        return component


class Vega(ComponentBase):
    component = param.Parameter("pn.pane.Vega")
    reference = param.String("https://panel.holoviz.org/reference/panes/Vega.html#altair")
    extension = param.String("vega")
    imports = """\
import panel as pn

pn.extension("vega", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            vegalite = {
                "$schema": "https://vega.github.io/schema/vega-lite/v3.json",
                "data": {
                    "url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/barley.json"
                },
                "mark": {"type": "bar", "tooltip": True},
                "width": "container",
                "height": "container",
                "encoding": {
                    "x": {"aggregate": "sum", "field": "yield", "type": "quantitative"},
                    "y": {"field": "variety", "type": "nominal"},
                    "color": {"field": "site", "type": "nominal"},
                },
            }

            if theme == "dark":
                vegalite["config"] = {
                    "background": "#333",
                    "title": {"color": "#fff"},
                    "style": {"guide-label": {"fill": "#fff"}, "guide-title": {"fill": "#fff"}},
                    "axis": {"domainColor": "#fff", "gridColor": "#888", "tickColor": "#fff"},
                }
            return vegalite

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.Vega(plot, height=500, sizing_mode="stretch_both")
        return component


class VTK(ComponentBase):
    component = param.Parameter("pn.pane.VTK")
    reference = param.String("https://panel.holoviz.org/reference/panes/VTK.html")
    extension = param.String("vtk")
    imports = """\
import panel as pn
import vtk

from vtk.util.colors import tomato

pn.extension("vtk", sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_plot(theme="default", accent_base_color="blue"):
            # This creates a polygonal cylinder model with eight circumferential
            # facets.
            cylinder = vtk.vtkCylinderSource()
            cylinder.SetResolution(8)

            # The mapper is responsible for pushing the geometry into the graphics
            # library. It may also do color mapping, if scalars or other
            # attributes are defined.
            cylinderMapper = vtk.vtkPolyDataMapper()
            cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

            # The actor is a grouping mechanism: besides the geometry (mapper), it
            # also has a property, transformation matrix, and/or texture map.
            # Here we set its color and rotate it -22.5 degrees.
            cylinderActor = vtk.vtkActor()
            cylinderActor.SetMapper(cylinderMapper)
            cylinderActor.GetProperty().SetColor(tomato)
            # We must set ScalarVisibilty to 0 to use tomato Color
            cylinderMapper.SetScalarVisibility(0)
            cylinderActor.RotateX(30.0)
            cylinderActor.RotateY(-45.0)

            # Create the graphics structure. The renderer renders into the render
            # window.
            ren = vtk.vtkRenderer()
            renWin = vtk.vtkRenderWindow()
            renWin.AddRenderer(ren)

            # Add the actors to the renderer, set the background and size
            ren.AddActor(cylinderActor)
            if theme == "dark":
                ren.SetBackground(0.13, 0.13, 0.13)
            else:
                ren.SetBackground(0.97, 0.97, 0.97)
            return renWin

        plot = get_plot(theme=theme, accent_base_color=accent_base_color)
        component = pn.pane.VTK(plot, height=500, sizing_mode="stretch_both")
        return component

ALL = {
    "ALTAIR": Altair,
    "BOKEH": Bokeh,
    "DECKGL": DeckGL,
    "ECHARTS": ECharts,
    "FOLIUM": Folium,
    "MATPLOTLIB": Matplotlib,
    "PLOTLY": Plotly,
    "PLOTNINE": Plotnine,
    "PYDECK": PyDeck,
    "PYECHARTS": PyECharts,
    "PYVISTA": PyVista,
    "SEABORN": Seaborn,
    "VEGA": Vega,
    "VTK": VTK,
}