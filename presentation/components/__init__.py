import param
import panel as pn

import altair as alt
from vega_datasets import data

class ComponentBase(param.Parameterized):
    component =  param.Parameter()
    reference = param.String("https://panel.holoviz.org/")
    extension = param.String("")

    def example(self, theme="default", accent_base_color="blue"):
        raise NotImplemented("")

    def __str__(self):
        return type(self).__name__.upper()

class Altair(ComponentBase):
    component =  param.Parameter("pn.pane.Vega")
    reference = param.String("https://panel.holoviz.org/reference/panes/Vega.html#altair")
    extension = param.String("vega")

    def example(self, theme="default", accent_base_color="blue"):
        if theme=="dark":
            alt.themes.enable("dark")
        else:
            alt.themes.enable("default")

        cars = data.cars()
        plot = alt.Chart(cars).mark_circle(size=60).encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin',
            tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
        ).properties(
            height="container",
            width="container",
        ).interactive()
        return pn.pane.Vega(plot, height=500, sizing_mode="stretch_both")

class Bokeh(ComponentBase):
    component =  param.Parameter(pn.pane.Bokeh)
    reference = param.String("https://panel.holoviz.org/")

    def example(self, theme="default", accent_base_color="blue"):
        import numpy as np
        from scipy.integrate import odeint

        from bokeh.plotting import figure

        sigma = 10
        rho = 28
        beta = 8.0/3
        theta = 3 * np.pi / 4

        def lorenz(xyz, t):
            x, y, z = xyz
            x_dot = sigma * (y - x)
            y_dot = x * rho - x * z - y
            z_dot = x * y - beta* z
            return [x_dot, y_dot, z_dot]

        initial = (-10, -7, 35)
        t = np.arange(0, 100, 0.006)

        solution = odeint(lorenz, initial, t)

        x = solution[:, 0]
        y = solution[:, 1]
        z = solution[:, 2]
        xprime = np.cos(theta) * x - np.sin(theta) * y

        colors = ["#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", "#08519C", "#08306B",]

        p = figure(title="Lorenz attractor example", tools=["pan,wheel_zoom,box_zoom,reset,hover"])

        p.multi_line(np.array_split(xprime, 7), np.array_split(z, 7),
                    line_color=colors, line_alpha=0.8, line_width=1.5)
        return pn.pane.Bokeh(p, height=500, sizing_mode="stretch_both")

class DeckGL(ComponentBase):
    component =  param.Parameter(pn.pane.DeckGL)
    reference = param.String("https://panel.holoviz.org/reference/panes/DeckGL.html")
    extension = param.String("deckgl")

    def example(self, theme="default", accent_base_color="#A01346"):
        MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"

        if theme=="dark":
            deckgl_map_style = "mapbox://styles/mapbox/dark-v9"
        else:
            deckgl_map_style = "mapbox://styles/mapbox/light-v9"

        json_spec = {
            "initialViewState": {
                "bearing": -27.36,
                "latitude": 52.2323,
                "longitude": -1.415,
                "maxZoom": 15,
                "minZoom": 5,
                "pitch": 40.5,
                "zoom": 6
            },
            "layers": [{
                "@@type": "HexagonLayer",
                "autoHighlight": True,
                "coverage": 1,
                "data": "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv",
                "elevationRange": [0, 3000],
                "elevationScale": 50,
                "extruded": True,
                "getPosition": "@@=[lng, lat]",
                "id": "8a553b25-ef3a-489c-bbe2-e102d18a3211",
                "pickable": True
            }],
            "mapStyle": deckgl_map_style,
            "views": [
                {"@@type": "MapView", "controller": True}
            ]
        }

        return pn.pane.DeckGL(json_spec, mapbox_api_key=MAPBOX_KEY, sizing_mode='stretch_both', height=400)

class ECharts(ComponentBase):
    component =  param.Parameter(pn.pane.ECharts)
    reference = param.String("https://panel.holoviz.org/reference/panes/ECharts.html#panes-gallery-echarts")
    extension = param.String("echarts")

    def example(self, theme="default", accent_base_color="#A01346"):
        echart = {
            "xAxis": {
                "data": ['2017-10-24', '2017-10-25', '2017-10-26', '2017-10-27']
            },
            "yAxis": {},
            "series": [{
                "type": 'k',
                "data": [
                    [20, 34, 10,38],
                    [40, 35, 30, 50],
                    [31, 38, 33, 44],
                    [38, 15, 5, 42],
                ]
            }],
            "responsive": True
        }
        return pn.pane.ECharts(echart, sizing_mode="stretch_both")
class HoloViews(ComponentBase):
    component =  param.Parameter(pn.pane.HoloViews)
    reference = param.String("https://panel.holoviz.org/reference/panes/HoloViews.html")

    def example(self, theme="default", accent_base_color="blue"):
        import numpy as np
        import holoviews as hv

        from holoviews import opts, streams
        from holoviews.plotting.links import DataLink

        hv.extension('bokeh')

        curve = hv.Curve(np.random.randn(10).cumsum()).opts(responsive=True, line_width=6, color=accent_base_color)
        if theme=="default":
            point_color="black"
        else:
            point_color="#E5E5E5"

        curve_stream = streams.CurveEdit(data=curve.columns(), source=curve, style={'color': point_color, 'size': 10})

        table = hv.Table(curve).opts(editable=True)
        DataLink(curve, table)

        plot=(curve + table).opts(
            opts.Table(editable=True),
        )

        return pn.pane.HoloViews(plot, height=500, sizing_mode="stretch_both")
class HVPlot(ComponentBase):
    component =  param.Parameter(pn.pane.HoloViews)
    reference = param.String("https://panel.holoviz.org/reference/panes/HoloViews.html")

    def example(self, theme="default", accent_base_color="blue"):
        import hvplot.pandas  # noqa

        from bokeh.sampledata.sprint import sprint as df

        plot = df.hvplot.violin(y='Time', by='Medal', c='Medal', ylabel='Sprint Time',
                        cmap=['gold', 'silver', 'brown'], legend=False,
                        responsive=True, padding=0.4)

        return pn.pane.HoloViews(plot, height=500, sizing_mode="stretch_both")

class IPyWidget(ComponentBase):
    component =  param.Parameter(pn.pane.IPyWidget)
    reference = param.String("https://panel.holoviz.org/")
    extension = param.String("ipywidgets")

    def example(self, theme="default", accent_base_color="blue"):
        # from ipyleaflet import Map, VideoOverlay

        # m = Map(center=(25, -115), zoom=4)

        # video = VideoOverlay(
        #     url="https://www.mapbox.com/bites/00188/patricia_nasa.webm",
        #     bounds=((13, -130), (32, -100))
        # )
        # m.add_layer(video)
        # return pn.pane.IPyWidget(m)
        return pn.pane.Alert("Currently not working. C.f. issue [#2593](https://github.com/holoviz/panel/issues/2593)", alert_type="info")
class Matplotlib(ComponentBase):
    component =  param.Parameter(pn.pane.Matplotlib)
    reference = param.String("https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib")

    def example(self, theme="default", accent_base_color="blue"):
        import numpy as np

        from matplotlib.figure import Figure
        from matplotlib import cm
        from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1
        import matplotlib.pyplot as plt

        plt.style.use("default")
        if theme=="dark":
            plt.style.use("dark_background")
        Y, X = np.mgrid[-3:3:100j, -3:3:100j]
        U = -1 - X**2 + Y
        V = 1 + X - Y**2
        speed = np.sqrt(U*U + V*V)

        fig0 = Figure(figsize=(12, 6))
        ax0 = fig0.subplots()
        FigureCanvas(fig0)  # not needed for mpl >= 3.1

        strm = ax0.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=cm.autumn)
        fig0.colorbar(strm.lines)

        return pn.pane.Matplotlib(fig0, sizing_mode="stretch_both")

class Plotly(ComponentBase):
    component =  param.Parameter(pn.pane.Plotly)
    reference = param.String("https://panel.holoviz.org/reference/panes/Plotly.html#panes-gallery-plotly")
    extension = param.String("plotly")

    def example(self, theme="default", accent_base_color="blue"):
        import pandas as pd
        import plotly.express as px

        data = pd.DataFrame([
            ('Monday', 7), ('Tuesday', 4), ('Wednesday', 9), ('Thursday', 4),
            ('Friday', 4), ('Saturday', 4), ('Sunay', 4)], columns=['Day', 'Orders']
        )

        if theme=="dark":
            plotly_template="plotly_dark"
        else:
            plotly_template="plotly"

        fig = px.line(data, x="Day", y="Orders", template=plotly_template, color_discrete_sequence=(accent_base_color,))
        fig.update_traces(mode="lines+markers", marker=dict(size=10), line=dict(width=4))
        fig.layout.autosize = True

        return pn.pane.Plotly(fig, config={'responsive': True})

class Plotnine(ComponentBase):
    component =  param.Parameter(pn.pane.Matplotlib)
    reference = param.String("https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib")

    def example(self, theme="default", accent_base_color="blue"):
        from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, themes, element_rect
        from plotnine.data import mtcars

        import matplotlib.pyplot as plt
        plt.style.use("default")
        if theme=="dark":
            plotnine_theme=themes.theme_dark() + themes.theme(plot_background=element_rect(fill='black', alpha=0))
        else:
            plotnine_theme=themes.theme_xkcd()

        plot=(
            (ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
            + geom_point()
            + stat_smooth(method='lm')
            + facet_wrap('~gear'))
            + plotnine_theme
            + themes.theme(figure_size=(16, 8))

        )
        return plot.draw()
class PyDeck(ComponentBase):
    component = param.Parameter(pn.pane.DeckGL)
    reference = param.String("https://panel.holoviz.org/reference/panes/DeckGL.html#pydeck")
    extension = param.String("deckgl")

    def example(self, theme="default", accent_base_color="blue"):
        import pydeck


        LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]
        polygon = pydeck.Layer(
            'PolygonLayer',
            LAND_COVER,
            stroked=False,
            # processes the data as a flat longitude-latitude pair
            get_polygon='-',
            get_fill_color=[0, 0, 0, 20]
        )

        DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
        geojson = pydeck.Layer(
            'GeoJsonLayer',
            DATA_URL,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation='properties.valuePerSqm / 20',
            get_fill_color='[255, 255, properties.growth * 255]',
            get_line_color=[255, 255, 255],
            pickable=True
        )

        if theme=="dark":
            deckgl_map_style = "mapbox://styles/mapbox/dark-v9"
        else:
            deckgl_map_style = "mapbox://styles/mapbox/light-v9"
        MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"
        INITIAL_VIEW_STATE = pydeck.ViewState(
            latitude=49.254,
            longitude=-123.13,
            zoom=11,
            max_zoom=16,
            pitch=45,
            bearing=0
        )

        r = pydeck.Deck(
            api_keys={'mapbox': MAPBOX_KEY},
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
            "style": {
                "backgroundColor": accent_base_color,
                "color": "white"
            }
        }
        tooltips = {geojson.id: geojson_tooltip}

        return pn.pane.DeckGL(r, tooltips=tooltips, height=600, sizing_mode="stretch_both")

class PyECharts(ComponentBase):
    component =  param.Parameter(pn.pane.ECharts)
    reference = param.String("https://panel.holoviz.org/reference/panes/ECharts.html#panes-gallery-echarts")
    extension = param.String("echarts")

    def example(self, theme="default", accent_base_color="blue"):
        from pyecharts.charts import Bar

        plot= (Bar()
            .add_xaxis(['Helicoptors', 'Planes', "Air Ballons"])
            .add_yaxis('Total In Flight', [50, 75, 25], color=accent_base_color)
        )

        # Workaround to make plot responsive
        import json
        plot=json.loads(plot.dump_options())
        plot["responsive"]=True

        return pn.pane.ECharts(plot, height=500, sizing_mode="stretch_both", theme=theme)

class Seaborn(ComponentBase):
    component =  param.Parameter(pn.pane.Matplotlib)
    reference = param.String("https://panel.holoviz.org/reference/panes/Matplotlib.html#panes-gallery-matplotlib")

    def example(self, theme="default", accent_base_color="blue"):
        import seaborn as sns
        import matplotlib.pyplot as plt

        penguins = sns.load_dataset("penguins")

        if theme=="dark":
            sns.set_style("darkgrid")
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
            sns.set_style("whitegrid")

        plot = sns.displot(penguins, x="flipper_length_mm", color=accent_base_color)
        fig0 = plot.fig
        fig0.set_size_inches(16,8)

        # FigureCanvas(fig0)  # not needed for mpl >= 3.1
        return pn.pane.Matplotlib(fig0, sizing_mode="stretch_both")


class Vega(ComponentBase):
    component =  param.Parameter("pn.pane.Vega")
    reference = param.String("https://panel.holoviz.org/reference/panes/Vega.html#altair")
    extension = param.String("vega")

    def example(self, theme="default", accent_base_color="blue"):
        vegalite = {
            "$schema": "https://vega.github.io/schema/vega-lite/v3.json",
            "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/barley.json"},
            "mark": {"type": "bar", "tooltip": True},
            "width": "container",
            "height": "container",
            "encoding": {
                "x": {"aggregate": "sum", "field": "yield", "type": "quantitative"},
                "y": {"field": "variety", "type": "nominal"},
                "color": {"field": "site", "type": "nominal"}
            }
        }

        if theme=="dark":
            vegalite["config"] = {
                "background": '#333',
                "title": { "color": "#fff" },
                "style": {
                    'guide-label': {
                        "fill": "#fff"
                    },
                    'guide-title': {
                        "fill": "#fff"
                    }
                },
                "axis": {
                    "domainColor": "#fff",
                    "gridColor": "#888",
                    "tickColor": "#fff"
                }
            }
        return pn.panel(vegalite, height=400, sizing_mode="stretch_both")

