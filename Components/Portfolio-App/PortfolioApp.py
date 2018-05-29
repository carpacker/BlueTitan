# PortfolioApp.py
# Carson Packer
# 5/21/18

# Contains widgets, screens and functions for building a front end
#  portfolio management system.

# TODO:
#   - Consistent sidebar/bottom
#   - Side/bottom bar has a few options
#    - Mining information
#    - Cryptocurrency prices
#    - Current balances and assets
#  
# SCREEN: Main/Menu
# DESCRIPTION:
#   Opening/introduction screen to the application.
class MainScreen(Screen):
    fullscreen = BooleanProperty(False)

        def add_widget(self, *args):
    if 'content' in self.ids:
        return self.ids.content.add_widget(*args)
    return super(ShowcaseScreen, self).add_widget(*args)

# SCREEN: Mining
# DESCRIPTION:
#   Main screen that displays all pertinent mining information.
class MiningScreen(Screen):
    pass

# SCREEN: MarketInformation
# DESCRIPTION:
#   More comprehensive display of prices. Will include graphs for
#    ability to analyze prices.
def MarketInfoScreen(Screen):
    pass

# SCREEN: FundManagement
# DESCRIPTION:
#   Provides tools to manage the funds on various exchanges
def FundManagementScreen(Screen):
    pass

# Main Application
class PortfolioApp(App):

    # Global Variables
    # TODO: Edit these
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'hello world'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Buttons', 'ToggleButton', 'Sliders', 'ProgressBar', 'Switches',
            'CheckBoxes', 'TextInputs', 'Accordions', 'FileChoosers',
            'Carousel', 'Bubbles', 'CodeInput', 'DropDown', 'Spinner',
            'Scatter', 'Splitter', 'TabbedPanel + Layouts', 'RstDocument',
            'Popups', 'ScreenManager'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    # TODO:
    #   Edit this for specific needs
    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    # TODO:
    #   Pull other functions as necessary from samples

if __name__ == '__main__':
    PortfolioApp().run()

