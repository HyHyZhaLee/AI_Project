from kivy.animation import Animation
from kivy.properties import DictProperty, NumericProperty, ColorProperty, get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.tooltip import MDTooltip

class ElevationCard(RoundedRectangularElevationBehavior, MDCard):
    """Implement a base class for a card with elevation behavior"""

class MenuButton(MDIconButton, MDTooltip):
    """Implements the button for magic menu"""

class MagicMenu(ElevationCard):
    """Implement the base class for magic menu"""
    pos_marker = NumericProperty(0)
    color_marker = ColorProperty([0,0,0,0])
    menu_buttons = DictProperty(
        {
            "home": "Red",
            "account": "Indigo",
            "message": "Teal",
            "help": "Yellow",
            "close": "BlueGray"
        }
    )

    def generate_menu(self):
        """Generate menu buttons"""

        spacing_button= dp(12)
        start_position = dp(6)

        for i , name_icon in enumerate(self.menu_buttons.keys()):
            start_position += spacing_button
            menu_button= MenuButton(icon=name_icon)
            menu_button.y = (
                self.height - (menu_button.height * (i+1) + start_position)
            )
            menu_button.bind(on_enter=self.set_menu_marker)
            self.ids.buttons_container.add_widget(menu_button)
        self.set_menu_marker(self.ids.buttons_container.children[-1])
    def set_menu_marker(self, instance_menu_button: MenuButton):
        """Sets the color and position of the color area for selected menu item"""
        anim = Animation(
            pos_marker=instance_menu_button.y - dp(16),
            color_marker=get_color_from_hex(
                colors[self.menu_buttons[instance_menu_button.icon]]["500"]
            ),
            t="in_out_sine",
            d=0.3,
        )
        anim.bind(on_complete=self.set_screen_color)
        anim.start(self)

    def set_screen_color(self, *args):
        """Sets the background color of the root screen"""

        anim = Animation(
            md_bg_color=self.color_marker,
            t="in_out_sine",
            d=0.3
        )
        anim.start(self.parent)