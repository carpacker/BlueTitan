import csv
import time
# Only works with something of same asset


# FUNCTION: main
# INPUT: csv_name - string of csv file
# OUTPUT: N/A
# DESCRIPTION:
#   Top level function for converting a list of buys and sells into a FIFO
#    profit loss generator
def main(csv_name):
    inputs = []
    outputs = []
    consumables = []
    with open(csv_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        # 1. Read in CSV, fill input/output lists based on type of transaction
        for row in readCSV:
            # Place INPUT values in the input list, first in
            if row[1] == 'buy':
                inputs.append(row)
            elif row[1] == 'sell':
                outputs.append(row)
            elif row[1] == 'consumable':
                consumables.append(row) 
                
        # 2. While there are outputs still left to be acted over, calculate
        #     profit loss using FIFO methodology.
        running_profit = 0
        running_loss = 0
        total_in = 0
        total_out = 0

        ctr_flag = 2


        while len(outputs) > 0:
            if ctr_flag == 2:
                current_output = outputs.pop()
                current_input = inputs.pop()

            elif ctr_flag == 1:
                current_input = inputs.pop()

            elif ctr_flag == 0:
                current_output = outputs.pop()
                
            print("---- ITERATION " + str(len(outputs)) + "----")
            print("OUT:", outputs)
            print("IN:", inputs)
            print("CURRENT PROFIT:", running_profit)
            
            # CASE: Sell is larger - work through buys
            curr_value = float(current_output[2])
            print(current_input, current_output)
            while curr_value > float(current_input[2]):
                # Calculate the profit FILO
                orig_value = float(current_input[4]) * float(current_input[5])
                sell_value = float(current_input[4]) * float(current_output[5])
                profit_loss = sell_value - orig_value

                # Add to running profit, adjust current output's value for next iteration
                running_profit += profit_loss
                current_output[4] = float(current_output[4]) - float(current_input[4])
                curr_value = float(current_output[2]) - sell_value
                print(orig_value,sell_value,profit_loss,running_profit,curr_value)

                # Set control flag to pop input
                current_input = inputs.pop()
                time.sleep(3)

            # CASE: Buy is larger, continue loop 
            # Calculate the profit FILO
            orig_value = float(current_output[4]) * float(current_input[5])
            sell_value = float(current_output[4]) * float(current_output[5])
            profit_loss = sell_value - orig_value

            # Add to running profit, adjust current output's value for next iteration
            running_profit += profit_loss
            current_input[4] = float(current_input[4]) - float(current_output[4])
            print(orig_value,sell_value,profit_loss,running_profit)

            # Pop new input
            ctr_flag = 0
            time.sleep(3)           

        print(running_profit, "END")
        # 3. Determine what is leftover, if anything, from input list
        for consumable in consumables:
            profit_short = (float(consumable[4]) * float(consumable[6])) - (float(consumable[4]) * float(consumable[5]))
            running_profit += profit_short

        print(running_profit, "add consumables")

        # Insert results as final csv row
        # TODO
if __name__ == "__main__":
    main('taxes2017.csv')

