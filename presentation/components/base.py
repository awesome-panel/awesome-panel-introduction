import inspect
import textwrap

import param


class ComponentBase(param.Parameterized):
    component = param.Parameter()
    docs = param.String("")
    reference = param.String("https://panel.holoviz.org/")
    extension = param.String("")
    imports = param.String("")

    def example(self, theme="default", accent_base_color="blue"):
        raise NotImplementedError

    def code(self, accent_base_color="blue"):
        text = self.imports
        title = type(self).__name__
        text += f"""
accent_base_color = "{ accent_base_color }"
template = pn.template.FastListTemplate(
    site="Awesome Panel",
    title="{title}",
    accent_base_color=accent_base_color,
    header_background=accent_base_color,
    header_accent_base_color="white",
)
theme = "dark" if template.theme == pn.template.DarkTheme else "default"

"""
        text += textwrap.dedent(
            inspect.getsource(self.example)
            .replace('def example(self, theme="default", accent_base_color="blue"):', "")
            .replace("self, ", "")
            .replace("\n        return component", "")
            .replace(" margin=(10, 80, 10, 15)", "")  # Hack
        )

        text += """\
template.main.append(component)
template.servable()"""
        return text

    def __str__(self):
        return type(self).__name__.upper()
