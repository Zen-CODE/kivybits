from time import sleep
from kivy.logger import Logger


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
            Logger.info("service_one/main.py: counter = {0}".format(self.counter))
            sleep(.5)
            self.counter += 1 
        Logger.info("service_one/main.py: Exiting")


if __name__ == '__main__':
    Waiter().wait()

