import panel as pn

from shared import Configuration

config = Configuration(title="Works in your Notebook and IDE", url="works_in_your_notebook_and_ide", random=True)
pn.extension(sizing_mode="stretch_width")

# Define the Text

text = """# Works with your Favorite Server

## Panel **supports most deployment scenarios** for data science apps.
"""

# Define the Image Component

image_component = pn.layout.FlexBox(
    pn.pane.PNG(
        "https://panel.holoviz.org/_static/logo_stacked.png",
        link_url="https://panel.holoviz.org/user_guide/Server_Deployment.html",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    pn.pane.JPG(
        "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel-assets/master/images/bokeh-logo.jpg",
        link_url="https://docs.bokeh.org/en/latest/docs/user_guide/server.html",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    pn.pane.PNG(
        "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel-assets/master/images/voila-logo.png",
        link_url="https://panel.holoviz.org/FAQ.html?highlight=voila",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    pn.pane.PNG(
        "https://github.com/MarcSkovMadsen/awesome-panel-assets/blob/5535537e86ce49974794a12e289831204caa2774/images/flask-logo.png?raw=True",
        link_url="https://discourse.holoviz.org/t/panel-server-embedded-in-flask-gunicorn/978",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    pn.pane.PNG(
        "https://github.com/MarcSkovMadsen/awesome-panel-assets/blob/5535537e86ce49974794a12e289831204caa2774/images/django-logo-negative.png?raw=True",
        link_url="https://panel.holoviz.org/user_guide/Django_Apps.html",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    pn.pane.PNG(
        "https://github.com/MarcSkovMadsen/awesome-panel-assets/blob/5535537e86ce49974794a12e289831204caa2774/images/fast-api-logo.png?raw=True",
        link_url="https://hackmd.io/ileoi_9YT6eEm27hbxTzmA?view",
        embed=False,
        height=115,
        margin=25,
        sizing_mode="fixed",
    ),
    justify_content="center", margin=25, sizing_mode="stretch_both"
)

# Layout the App

pn.template.FastListTemplate(
    site=config.site,
    title=config.title,
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=400,
    main_max_width=config.main_max_width,
    main=[
        pn.Row(text, config.get_logo_pane(width=100)),
        image_component,
    ],
).servable()
