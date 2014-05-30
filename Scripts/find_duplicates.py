from os.path import join, isdir
from os import listdir


class FolderSearch(object):
    @staticmethod
    def list_duplicates(folder):
        FolderSearch._find_case_dups(folder)


    @staticmethod
    def _find_case_dups(folder):
        if isdir(folder):
            #print "Processing ", folder
            folders = [item for item in listdir(folder)]
            lowers = [item.lower() for item in folders]
            dups = set([x for x in lowers if lowers.count(x) > 1])
            for dupe in dups:
                print "Case duplicate - ", join(folder, dupe)
            for item in folders:
                FolderSearch._find_case_dups(join(folder, item))

if __name__ == "__main__":
    FolderSearch.list_duplicates('/media/Zen320/Zen/Music')
