
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty
import datetime

def greet_by_time(name):
    current_time = datetime.datetime.now().time()

    if current_time < datetime.time(12, 0, 0):
        greeting = "Good morning"
    elif current_time < datetime.time(18, 0, 0):
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return f"{greeting} {name}"

def format_date():
    date = datetime.datetime.now()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    day_name = days[date.weekday()]
    day_number = date.day
    month_name = months[date.month - 1]
    year = date.year

    formatted_date = f"{day_name}, {day_number} {month_name} {year}"
    return formatted_date

class MainWindow(BoxLayout):
    username = "Huy Gia Ly"
    greeting = StringProperty(greet_by_time(username))
    format_date = StringProperty(format_date())
    def __init__(self, **kw):
        super().__init__(**kw)

class NavTab(ToggleButtonBehavior, BoxLayout):
    text = StringProperty("")
    icon = StringProperty("")
    icon_active = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)

