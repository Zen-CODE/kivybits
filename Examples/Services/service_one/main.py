from time import sleep
from kivy.logger import Logger
import zipfile
from os.path import exists


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
        while self.counter < 3:
            Logger.info("service_one/main.py: counter = {0}".format(self.counter))
            sleep(.5)
            self.counter += 1 
        
        Logger.info("service_one/main.py: About to open zip")

    def open_zip():
        """ Open a standard zip file. """
        file_name = "service_one/main.zip"
        if exists(file_name):
            Logger.info("service_one/main.py: zip found. About to open.")
            my_zip = zipfile.ZipFile(file_name, "r")
            Logger.info("service_one/main.py: zip open. contains {0}".format(
                my_zip.filelist))
            Logger.info("service_one/main.py: zip examined. Exiting.")

        else:
            Logger.info("service_one/main.py: zip not found. Exiting.")
            


if __name__ == '__main__':
    Waiter().wait()

