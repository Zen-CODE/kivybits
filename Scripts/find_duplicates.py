from os.path import join, isdir
from os import listdir, rename
import shutil


class FolderSearch(object):
    @staticmethod
    def list_duplicates(folder):
        FolderSearch._remove_case_dups(folder)
        FolderSearch._ensure_titlecase(folder)

    @staticmethod
    def _remove_case_dups(folder):
        if isdir(folder):
            # Get a list of folder names and lowercase names
            folders = [item for item in listdir(folder)
                       if isdir(join(folder, item))]
            lowers = [item.lower() for item in folders]

            # Remove the folder if it's lower case occurs > 1
            for item in folders:
                if lowers.count(item.lower()) > 1:
                    lowers.remove(item.lower())
                    shutil.rmtree(join(folder, item))

            for item in folders:
                FolderSearch._remove_case_dups(join(folder, item))

    @staticmethod
    def _ensure_titlecase(folder):
        if isdir(folder):
            folders = [item for item in listdir(folder)
                       if isdir(join(folder, item))]
            for item in folders:
                if item.title() != item:
                    #rename(join(folder, item), join(folder, item.title()))
                    print "renaming ", join(folder, item)
                    print "     to ", join(folder, item.title())
                    rename(join(folder, item), join(folder, item.title()))
                FolderSearch._ensure_titlecase(join(folder, item.title()))

if __name__ == "__main__":
    FolderSearch.list_duplicates('/media/Zen320/Zen/Music/Recorded')
