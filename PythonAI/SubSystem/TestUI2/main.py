import importlib
import os.path

from kivy import Config
from  kivy.uix.screenmanager import ScreenManager
from  PIL import ImageGrab
from kivymd.uix.screen import MDScreen

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need
Config.set("graphics", "height", resolution[1])
Config.set("graphics", "width", "400")

from kivy.core.window import Window

# Place the application widow on the right side of the computer screen
Window.top = 0
Window.left = resolution[0] - Window.width

from kivymd.tools.hotreload.app import MDApp

class MagicMenuConcept(MDApp):
    KV_DIRS = {
        os.path.join(
            os.getcwd(),
            "magicmenu"
        )
    }

    def build_app(self)->ScreenManager:
        import magicmenu.magic_menu

        importlib.reload(magicmenu.magic_menu)

        magic_menu = magicmenu.magic_menu.MagicMenu()
        magic_menu.generate_menu()

        screen = MDScreen()
        screen.add_widget(magic_menu)

        return screen

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers)->None:
        """
        The method handles keyboard events

        By default, a forced restart of an applicattion is tied to 'CTRL+R' key on Windows and 'COMAND+R' on MAC
        """
        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()

MagicMenuConcept().run()
