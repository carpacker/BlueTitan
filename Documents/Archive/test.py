class testClass(object):
    initialize_me = 'one'

    def __init__(self, value):
        initialize_me = value

if __name__ == "__main__":
    the_cla = testClass('two')
    print(testClass.initialize_me)
