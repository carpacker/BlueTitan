# External Imports
import time

# CLASS: PrintLibrary
# DESCRPTION:
#   Used to help with debugging. More comprehensive description to come.
class PrintLibrary():

    # FUNCTON: displayDictionary
    # INPUT: var_dict -  tuple of (key,value)
    #        header   -  string (OPTIONAL)
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Takes a dictionary and prints each key/value pairing of the dictionary.
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
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   Takes input tuples representing an order book (bids and asks) of an exchange and constructs a series of print
    #    statements to display them in a visually cohesive manner.
    def displayOrderbook():
        pass
        
    # FUNCTION: displayVariable
    # INPUT: value
    #        func_name
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Prints a single variable (string, int, ...). Cannot display tuples, lists or dictionaries.
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
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Takes a list or tuple, itereates through and prints each element.
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


    # FUNCTION: header
    # DESCRIPTION:
    #   Displays a header for testing.
    def header(message):
        print("|- - - - - - - - - - - - - - - - - - - - - - " + message + " - - - - - - - - - - - - - - - - - - - - - -|")

    def header2(message):
        print("|# # # # # # # # # # # # # # # # # # " + message + " # # # # # # # # # # # # # # # # # #|")

    # FUNCTION: sleep
    # INPUT: time       - int
    #        message    - string
    #        func_name  - string (OPTIONAL)
    # DESCRIPTION:
    #   Custom sleep statement that prints out a message.
    def sleep(time, message="", func_name=None):
        pass 

    # probably rework this...
    def stageHeader(message, stage):
        print(str(stage) + " :: " + message)
        stage += 1
        return stage

    def delimiter():
        print("- - - - - - - - - - - - - - - - - - - - -")
    
    def miniDelimiter():
        print ("  *---------------------------*  ")


# CLASS: DynamicPrinter
# DESCRIPTION:
#   Used by the PrintLibrary to create dynamically sized prints for the sake of readability. 
#    There is a required input of a maximum length that a print statement is allowed. The 
#    program then adapts inputs such that the print statements produce a cohesive output 
#    irrespective of the unpredictable sizing of given inputs.
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
    
