# WidgetLibrary.py
# Carson Packer
# DESCRIPTION:
#    This will be the main container library for Kivy widgets. It may be subdivided in the future as is necessary. The main caveat to this is that each function acts as either a wrapper to kivy functinos with added functionality or combines main widgets to make a more complex, generic widget. A theme dictactes the background

# External Imports
import kivy

# Internal Imports

# Kivy Imports
from kivy.uix.widget import Widget

# Latest Version: ???
kivy.require('')

# TYPES OF WIDGETS:
# - Display widgets
#    These are simple display widgets, for displaying singular items such as text or media.
# - Button widgets
#    A simple generic button wrapper and various alternate styles.
# - List widgets
#    Suite of widgets which display lists of other widgets.
# - Media widgets
#    Suite of widgets that use media widgets as the base.
# - Menu Widgets
#    Toolkit of generic menus.
# - ToolbarWidgets
#    Toolkit of generic toolbars.

########## Display Widgets

def TextWidget(Widget):
    pass

def MediaWidget(Widget):
    pass

def InputWidget(Widget):
    pass

######### Button Wigets
def GenericButton(Widget):
    pass

def GenButtonStyleOne(Widget):
    pass

######### Menu Widgets
def Menu(Widget):
    pass

def MenuMedia(Widget):
    pass

######### List Widgets

# WIDGET: ListWidget
# INPUTS: columns - int [number of columns]
# DESCRIPTION:
#    Generic widget that displays a list of items. 
def ListWidget(Widget):
    pass

def ListWidgetScr(Widget):
    pass

def MatrixWidget(Widget):
    pass

###################### Media Widgets



# #################################### TOOL BAR WIDGETS ######################################

# WIDGET: GenericTB
# DESCRIPTION:
#    Generic toolbar... intended to be used on the the far side of  another widget or screen. This can be on the top, the bot, or one of the sides.
def GenericTB(Widget):
    pass

# WIDGET: MainTB
# DESCRIPTION:
#    Generic 'main' toolbar to be used on top of main window. This is supposed to be a standard easily accessible toolbar that provides basic functions.
def MainTB(Widget):
    pass

# WIDGET: DropDownTB
# DESCRIPTION:
#    Creates a drop-down toolbar when clicked. Toolbar's items are filled dynamically using input parameters
class DropDownTB(Widget):
    pass
