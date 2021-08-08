from presentation.components import Altair

def test_altair():
    assert Altair().code()=="""\
import altair as alt
import panel as pn

from vega_datasets import data

pn.extension("vega", sizing_mode="stretch_width")

accent_base_color = "blue"
template = pn.template.FastListTemplate(
    site="Awesome Panel",
    title="Altair",
    accent_base_color=accent_base_color,
    header_background=accent_base_color,
    header_accent_base_color="white",
)
theme = "dark" if template.theme == pn.template.DarkTheme else "default"


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
template.main.append(component)
template.servable()"""