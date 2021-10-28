import pathlib
import random
import sys

import panel as pn
import param

_COLORS = [
    ("#00A170", "white"),
    ("#DAA520", "white"),
    ("#2F4F4F", "white"),
    ("#F08080", "white"),
    ("#4099da", "white"), # lightblue
]
_LOGOS = {
    "default": "https://panel.holoviz.org/_static/logo_stacked.png",
    "dark": "https://raw.githubusercontent.com/holoviz/panel/98389a8dead125bcb7c60dc2c1564e112d89d3fa/doc/_static/logo_stacked_dark_theme.png",
}


_MENU_FILE = pathlib.Path(__file__).parent / "menu.html"
_MENU_TEXT = _MENU_FILE.read_text()

_ACE_THEMES={
    "default": "chrome",
    "dark": "tomorrow_night_eighties"
}

RAW_CSS = """
.sidenav .menu-item-active a {
    background: var(--accent-fill-active);
    color: white;
}
"""
if not RAW_CSS in pn.config.raw_css:
    pn.config.raw_css.append(RAW_CSS)

def _mock_panel():
    def _reload(module=None):
        if module is not None:
            for module in pn.io.reload._modules:
                if module in sys.modules:
                    del sys.modules[module]
        for cb in pn.io.reload._callbacks.values():
            cb.stop()
        pn.io.reload._callbacks.clear()
        if pn.state.location:
            pn.state.location.reload = True
        for loc in pn.state._locations.values():
            loc.reload = True

    pn.io.reload._reload = _reload

_mock_panel()
#tests

class Configuration(param.Parameterized):
    theme = param.String()
    site = param.String(default="Panel@PyData 2021")
    title = param.String()
    url = param.String()
    logo = param.String()
    accent_base_color = param.Color()
    header_color = param.Color()
    header_accent_base_color = param.Color("white")
    header_background = param.Color()
    main_max_width = param.String("95%")
    sidebar_width = param.Integer(400)
    ace_theme=param.String()

    def __init__(self, random=False, **params):
        """Configuration for your (Fast) Template

        Args:
            random (bool, optional): Whether or not to provide randomized values. Defaults to False.
        """
        super().__init__(**params)

        self.theme = self._get_theme()

        if random:
            color_index = self._get_random_color_index()
        else:
            color_index=0

        self.accent_base_color = _COLORS[color_index][0]
        self.header_color = _COLORS[color_index][1]
        self.header_background = self.accent_base_color

        self.logo=_LOGOS[self.theme]
        self.ace_theme=_ACE_THEMES[self.theme]

    def _get_theme(self):
        if pn.template.FastListTemplate().theme==pn.template.DarkTheme:
            return "dark"
        return "default"

    def _get_random_color_index(self):
        if not "color" in pn.state.cache:
            pn.state.cache["color"]=-1
        color = pn.state.cache["color"]+1
        if color==len(_COLORS):
            color=0
        pn.state.cache["color"]=color
        return color

    @property
    def _collapsed_icon(self) -> str:
        return f"""<svg style="stroke: { self.accent_base_color }" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" slot="collapsed-icon">
<path d="M15.2222 1H2.77778C1.79594 1 1 1.79594 1 2.77778V15.2222C1 16.2041 1.79594 17 2.77778 17H15.2222C16.2041 17 17 16.2041 17 15.2222V2.77778C17 1.79594 16.2041 1 15.2222 1Z" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M9 5.44446V12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M5.44446 9H12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>"""

    @property
    def _expanded_icon(self) -> str:
        return f"""<svg style="stroke: { self.accent_base_color }" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" slot="expanded-icon">
<path d="M15.2222 1H2.77778C1.79594 1 1 1.79594 1 2.77778V15.2222C1 16.2041 1.79594 17 2.77778 17H15.2222C16.2041 17 17 16.2041 17 15.2222V2.77778C17 1.79594 16.2041 1 15.2222 1Z" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M5.44446 9H12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>
"""

    @property
    def menu(self) -> str:
        """Returns a HTML Menu"""
        test=f'<li><a href="{ self.url }">{ self.title }</a></li>'
        return (
            _MENU_TEXT
            .replace("{ COLLAPSED_ICON }", self._collapsed_icon)
            .replace("{ EXPANDED_ICON }", self._expanded_icon)
            .replace(f'<li><a href="{ self.url }">{ self.title }</a></li>', f'<li class="menu-item-active"><a href="{ self.url }">{ self.title }</a></li>')
        )

    def get_logo_pane(self, **params):
        return pn.pane.PNG(
            self.logo,
            link_url="https://panel.holoviz.org",
            embed=False,
            sizing_mode="fixed",
            align="center",
            **params
        )

if __name__.startswith("bokeh"):
    config = Configuration(title="Works in your Notebook and IDE", url="works_in_your_notebook_and_ide", random=True)
    pn.template.FastListTemplate(
        title="Test Configuration",
        site=config.site,
        header_accent_base_color=config.header_accent_base_color,
        header_background=config.header_background,
        header_color=config.header_color,
        sidebar_footer=config.menu,
        accent_base_color=config.accent_base_color,
        main=[pn.pane.PNG(config.logo)],
    ).servable()
