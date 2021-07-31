# 👍 Awesome Panel - Introduction to Panel

THIS REPO IS WORK IN PROGRESS. PRE-ALPHA

[Panel](https://panel.holoviz.org) is a very powerful framework for exploratory data analysis and for creating beautiful data science apps in Python.

This repository contains code and other material to support introductory talks, training and videos on Panel.

![Awesome Panel Introduction - Tour](https://github.com/MarcSkovMadsen/awesome-panel-introduction/blob/main/assets/videos/awesome-panel-introduction-tour.gif?raw=true)

Check it out

Resource | Video | Notebooks | App |
|--------|-------|-----------|-----|
| Presentation | [Youtube](https://youtu.be/dUaS7yM2FxA) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/awesome-panel-introduction/main?urlpath=lab/tree/presentation) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/awesome-panel-introduction/main?urlpath=panel/introduction) |

For more inspiration check out my site [awesome-panel.org](https://awesome-panel.org)

## Installation

```bash
pip install -r requirements.txt
jupyter serverextension enable panel.io.jupyter_server_extension
```

## Run the presentation

```bash
panel serve presentation/*.py --autoreload
```
