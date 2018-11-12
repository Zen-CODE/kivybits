from os import environ
from time import sleep


class Waiter(object):
    """
    This class simply waits for the update to finish and then closes.
    """
    def __init__(self):
        super(Waiter, self).__init__()
        ''' Hold a reference to the display wrapper class'''
        self.counter = 0

    def wait(self):
        """ Start the loop where we wait for messages. """
        while self.counter < 10:
            print("service1/main.py: counter = {0}".format(self.counter))
            sleep(.5)
            self.counter += 1 

if __name__ == '__main__':
    Waiter().wait()

