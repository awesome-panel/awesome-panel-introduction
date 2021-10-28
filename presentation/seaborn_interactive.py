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
).servable()