from os.path import join, isdir
from os import listdir
import shutil


class FolderSearch(object):
    @staticmethod
    def list_duplicates(folder):
        FolderSearch._remove_case_dups(folder)


    @staticmethod
    def _remove_case_dups(folder):
        if isdir(folder):
            # Get a list of folder names and lowercase names
            folders = [item for item in listdir(folder)]
            lowers = [item.lower() for item in folders]

            # Remove the folder if it's lower case occurs > 1
            for item in folders:
                if lowers.count(item.lower()) > 1:
                    lowers.remove(item.lower())
                    shutil.rmtree(join(folder, item))

            for item in folders:
                FolderSearch._remove_case_dups(join(folder, item))

if __name__ == "__main__":
    FolderSearch.list_duplicates('/media/Zen320/Zen/Music')
