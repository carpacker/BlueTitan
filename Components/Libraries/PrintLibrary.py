# External Imports
import time

# TODO -
#   Could add dynamically increasing print statement... adding or removing '-' to fulfill requirement
#   Print orderbook

# CLASS: PrintLibrary
# DESCRPTION:
#   Used to help with debugging. More comprehensive description to come.
class PrintLibrary():

    # FUNCTION: delimiter
    def delimiter():
        print("- - - - - - - - - - - - - - - - - - - - -")
    
    def miniDelimiter():
        print ("  *---------------------------*  ")

            
    # FUNCTON: displayDictionary
    # INPUT: var_tuple -  tuple of (key,value)
    #        header    -  string (OPTIONAL)
    def displayDictionary(var_dict, header=""):
        if header != "":
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
            print(" * " + header)
            print("  ___________")
        else :
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
        for key,value in var_dict.items():
            print("  " + str(key) + " - " + str(value))  

    # FUNCTION: displayOrderbook
    def displayOrderbook():
        pass
        
    # FUNCTION: displayVariable
    # INPUT:
    def displayVariable(value, func_name=None):
        print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
        # Different cases for tuple, list, float (?)
        if func_name != None:
            print("** FUNCTION : " + func_name) # Func name display
        else:
            pass
        print(" * - " + str(value)) # Add to this

    # FUNCTON: displayVariables
    # INPUT: var_tuple -  list or tuple
    #        header    -  string (OPTIONAL)
    def displayVariables(var_tuple, header=""):
        if header != "":
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
            print(" * " + header)
            print("  ___________")
        else :
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
        ticker = 0
        for value in var_tuple:
            ticker += 1
            print("  " + str(ticker) + " - " + str(value))  

    def displayKeyVariables(var_tuple, header=""):
        if header != "":
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
            print(" * " + str(header))
            print("  ___________")
        else :
            print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
        for key,value in var_tuple:
            print("  " + str(key) + " - " + str(value))  

    # FUNCTION: header
    # DESCRIPTION:
    #   Displays a header for testing
    def header(message):
        print("|- - - - - - - - - - - - - - - - - - - - - - " + message + " - - - - - - - - - - - - - - - - - - - - - -|")

    def header2(message):
        print("|# # # # # # # # # # # # # # # # # # " + message + " # # # # # # # # # # # # # # # # # #|")

    # FUNCTION: sleep
    # INPUT: time       - int
    #        message    - string
    #        func_name  - string (OPTIONAL)
    # DESCRIPTION:
    #   TODO
    def sleep(time, message, func_name=None):
        pass 

    # probably rework this...
    def stageHeader(message, stage):
        print(str(stage) + " :: " + message)
        stage += 1
        return stage

# Filler script to test out dynamic print-sizing, kept separate from main print library 
class DynamicPrinter():
    size = 40
    # Figure out a way to append '-' based on input string size

    def buildString(size, message=None):
        if message == None:
            # Output default
            string = ""
        else:
            # Detect length of string
            # Build first half of string with remaining characters
            # Append message
            # Build second half
            # Check length
            string = ""

        return string

    def header(size, message=None):
        if message == None:
            DynamicPrinter.buildString(size)
            print(string)
        else:
            DynamicPrinter.buildString(size, message)
            print(string)
    
