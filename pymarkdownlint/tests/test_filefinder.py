import os
from os.path import join
from glob import glob
from pymarkdownlint.tests import BaseTestCase
from pymarkdownlint.filefinder import MarkdownFileFinder


class FileFinderTests(BaseTestCase):
    def test_find_files(self):
        sample_dir = self.get_sample_path()
        files = MarkdownFileFinder.find_files(sample_dir)
        self.assertCountEqual(files, glob(join(sample_dir, '*.md')))

        files = MarkdownFileFinder.find_files(sample_dir, filter="*.txt")
        txt1 = os.path.join(sample_dir, "ignored-sample1.txt")
        txt2 = os.path.join(sample_dir, "ignored-sample2.txt")
        self.assertCountEqual(files, [txt1, txt2])
