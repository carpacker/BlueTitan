# API Library


# FUNCTION: determinePrecision
# INPUT: value - float
# OUTPUT: integer
# DESCRIPTION:
#   Assesses the precision of the input value.
def determinePrecision(value):
    if value == 1.0:
        return 0
    if value == 0.1:
        return 1
    if value == 0.01:
        return 2
    if value == 0.001:
        return 3
    if value == 0.0001:
        return 4
    if value == 0.00001:
        return 5
    if value == 0.000001:
        return 6
    if value == 0.0000001:
        return 7
    if value == 0.00000001:
        return 8
    else:
        return 0

# FUNCTION: verifySupported
# INPUT: exchange           - string
#        supportedexchanges - [string, ...]
# OUTPUT: boolean
# DESCRIPTION:
#   Used to verify whether an exchange is in the list of supported exchanges. Runtime is O(n) where n
#    is the length of supportedexchanges. Since supportedexchanges should be pretty small, this is neglible
#    for now. In the future, a more runtime friendly check may be required.
def verifySupported(exchange, supportedexchanges):
    for s_exchange in supportedexchanges:
        if s_exchange == exchange:
            return True

    print("ERROR :: exchange not supported")
    return False