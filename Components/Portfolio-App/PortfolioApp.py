# PortfolioApp.py
# Carson Packer
# 5/21/18
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
 
import API
from API import Exchange_API
# from API import Mining_API
import Ethermine
import Siamining

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

    # FUNCTION: updateTime
    # DESCRIPTION:
    #   Updates time in the corner of the screen 
    def 
    pass

# SCREEN: Mining
# DESCRIPTION:
#   Main screen that displays all pertinent mining information.
class MiningScreen(Screen):
    def main(address):
        # STATIC variables 
        # - Address : address of worker, used to grab other files
        # - Worker_count : # of intended workers

        MiningScreen.initializeScreens()
        ticker = 0
        while 1:
        # UPDATED EVERY 5 MINUTES
            ticker += 1
            if ticker == 600:
                # Retrieve values from API
                global_valuesE = MiningScreen.updateGlobals()
                global_valuesS = MiningScreen.updateGlobals()

                worker_one = MiningScreen.updateWorker()
                worker_two = MiningScreen.updateWorker()
                worker_three = MiningScreen.updateWorker()
                worker_four = MiningScreen.updateWorker()
                worker_five = MiningScreen.updateWorker()
                worker_six = MiningScreen.updateWorker()

                front_end_tuple = (0)
                updateFrontEnd(front_end_tuple)

                # Probably need an error checking system

            time.sleep(1)

    # FUNCTION: initializeStaticVariables
    def initializeStaticVariables():
        # Intended Worker Count
        worker_count = 7

        # Mining Addresses
        eth_address = ""
        sc_address = ""
        dcr_address = ""
        zec_address = ""

        worker_one_name = ""
        worker_two_name = ""
        worker_three_name = ""
        worker_four_name = ""
        worker_five_name = ""
        worker_six_name = ""
        worker_seven_name = ""

        worker_one_type = "NVIDIA"
        worker_two_type = "NVIDIA"
        worker_three_type = "AMD"
        worker_four_type = "AMD"
        worker_five_type = "AMD"
        worker_six_type = "AMD"
        worker_seven_type = "AMD"

        worker_one_mining = "ETHSC"
        worker_two_mining = "ZEC"
        worker_three_mining = "ETHSC"
        worker_four_mining = "ETHSC"
        worker_five_mining = "ETHSC"
        worker_six_mining = "ETHSC"
        worker_seven_mining = "ETHSC"

        # Set KV variables to the above

    # FUNCTION: updateWorker
    def updateWorker():
        # Update INDIVIDUAL worker values

        # 1. Grab values from API
        current_hashrate_eth = Ethermine.getCurrentHash()
        current_hashrate_sc = Siamining.getCurrentHash()

        reported_hashrate_eth = Ethermine.getReportedHash()
        reported_hashrate_sc = Siamining.getReportedHash()

        average_hashrate_eth = Ethermine.getAverageHash()
        average_hashrate_sc = Siamining.getAverageHash()

    # FUNCTION: updateGlobals
    def updateGlobals():
        # Update GLOBAL values

        # 1. Grab values from API
        network_eth = Ethermine.getNetworkDifficulty()
        network_sc = Siamining.getNetworkDifficulty()

        worker_count_eth = Ethermine.getWorkerCount()
        worker_count_sc = Siamining.getWorkerCount

# SCREEN: MarketInformation
# DESCRIPTION:
#   More comprehensive display of prices. Will include graphs for
#    ability to analyze prices.
class MarketInfoScreen(Screen):
    
    # FUNCTION: buildCurrenciesList
    # INPUT: 
    # OUTPUT:
    # DESCRIPTION:
    #   
    def buildCurrenciesList():
        pass

    # FUNCTION:
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   
    def updateCurrencies():
        pass
    
    def scroll_down():
        pass

    def scroll_up():
        pass

    def set_alert(pair, price):
        # Check settings for preferences & number
        # Submit above to alert bot, alert bot deals with accordingly
        pass

class CoinListing(GridLayout):
    def __init___(self, **kwargs):
        super(CoinListingself).__init__(**kwargs)
    pass

# SCREEN: FundManagement
# DESCRIPTION:
#   Provides tools to manage the funds on various exchanges
class FundManagementScreen(Screen):
    pass
    
# Settings [Screen] 
#   Accessible from every screen. Contains settings that can be adjusted globally 
#    and per screen.
class SettingsScreen(Screen):
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

