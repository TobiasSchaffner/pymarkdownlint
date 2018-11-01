import fnmatch
import os
from os.path import join
from glob import glob


class MarkdownFileFinder(object):
    @staticmethod
    def find_files(path, filter="*.md"):
        """ Finds files with an (optional) given extension in a given path. """
        if os.path.isfile(path):
            return [path]

        if os.path.isdir(path):
            return glob(join(path, filter))
