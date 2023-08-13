from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib as mpl
import matplotlib.pyplot as plt


Builder.load_file('views/dashboard/dashboard.kv')

class Dashboard(BoxLayout):

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
