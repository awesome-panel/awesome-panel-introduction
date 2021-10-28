import panel as pn
import param

ACCENT_BASE_COLOR = "#6082A2"

pn.extension(sizing_mode="stretch_width")

SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="54" height="14" viewBox="0 0 54 14"><g fill="none" fill-rule="evenodd" transform="translate(1 1)"><circle cx="6" cy="6" r="6" fill="#FF5F56" stroke="#E0443E" stroke-width=".5"></circle><circle cx="26" cy="6" r="6" fill="#FFBD2E" stroke="#DEA123" stroke-width=".5"></circle><circle cx="46" cy="6" r="6" fill="#27C93F" stroke="#1AAB29" stroke-width=".5"></circle></g></svg>
"""

CSS = f"""
body {{
    background: {ACCENT_BASE_COLOR};
    margin: 0px;
    min-height: 100vh;
}}
"""

class CodeTyper(pn.viewable.Viewer):
    value = param.String()
    command = param.String()
    language = param.String(default="python")
    theme=param.String(default="tomorrow_night")
    period= param.Integer(default=20)
    height=param.Integer(650)

    def __init__(self, **params):
        super().__init__(**params)

        self._ace = pn.widgets.Ace(language=self.language, theme=self.theme, height=self.height, margin=0)
        self._terminal = pn.pane.Markdown("$ ", margin=(0,25), background="#25282c", style={"color": "white"}, height=75)
        self._layout = pn.Column(
            pn.Column(
                pn.pane.Markdown("# Make Seaborn Interactive with PANEL", style={"color": "white"}),
                pn.Row(pn.pane.SVG(SVG, margin=7), pn.Spacer(), background="#25282c", height=30, margin=0),
                pn.pane.Markdown("&nbsp; &nbsp; `script.py`", background="#25282c", margin=0, style={"color": "white"}),
                self._ace,
                pn.Row(pn.Spacer()),
                pn.Column(self._terminal,background="#25282c", margin=0),
                margin=(50, 150),
            ),
            pn.pane.HTML("<style>" + CSS + "</style>", width=0, height=0, margin=0),
            background=ACCENT_BASE_COLOR,
        )

        chars = list(self.value)
        command = list(self.command)
        value = {"value": ""}
        def typer():
            if chars:
                for _ in range(0,5):
                    char = chars.pop(0)
                    value["value"] += char
                self._ace.value = value["value"]
            elif command:
                char = command.pop(0)
                self._terminal.object += char

        pn.state.onload(lambda: pn.state.add_periodic_callback(typer, period=self.period))

    def __panel__(self):
        return self._layout

SCRIPT = """\
import seaborn as sns

sns.set_style("whitegrid")
penguins = sns.load_dataset("penguins")

def func(input="green"):
    plot = sns.displot(penguins, x="flipper_length_mm", color=input, legend=False)
    fig0 = plot.fig
    fig0.set_size_inches(11, 8)
    return fig0

import panel as pn

pn.extension()

select = pn.widgets.Select(value="#6082A2", options=["#a2a160", "#6082A2", "#a26061"])

interactive_func=pn.bind(func, input=select)

pn.template.FastListTemplate(
    site="Panel", title="Works With The Tools You Know And Love",
    sidebar=[select], main=[interactive_func],
    header_background="#6082A2", accent_base_color="#6082A2"
).servable()"""

COMMAND="""
panel serve script.py --autoreload --show

Panel app running at: http://localhost:5006/panel
"""

CodeTyper(value=SCRIPT, command=COMMAND).servable()