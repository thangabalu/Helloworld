#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/home/prabhu/Dropbox/Django_projects/python/Helloworld')

from copyspecialfiles.copyspecial import CopySpecialFiles
import unittest
import tempfile
from testfixtures import TempDirectory
import shutil
import os
import zipfile

class copySpecialTestCase(unittest.TestCase):

    def setUp(self):
        self.inputDirectory1 = TempDirectory()
        self.inputDirectory1.write('india__universe__.txt', 'some foo thing')
        self.inputDirectory1.write('god__baby__.txt', 'some foo thing')
        self.inputDirectory1.write('hi.txt', 'some foo thing')

        self.inputDirectory2 = TempDirectory()
        self.inputDirectory2.write('world__universe__.txt', b'some foo thing')
        self.inputDirectory2.write('fyra.txt', b'some foo thing')
        self.inputDirectory2.write('hej.txt', b'some foo thing')

        self.specialFilesNamesAbsolutePath = ['%s/india__universe__.txt' %self.inputDirectory1.path, \
                                  '%s/god__baby__.txt' %self.inputDirectory1.path,\
                                  '%s/world__universe__.txt' %self.inputDirectory2.path]

        self.specialFileNames = ['india__universe__.txt', 'god__baby__.txt', 'world__universe__.txt']

        self.inputDirectoriesPath =[self.inputDirectory1.path, self.inputDirectory2.path]
        self.outputDirectory = TempDirectory()
        self.outputDirectory.path = self.outputDirectory.path

    def test_getSpecialFilesNames(self):
        copySpecialFiles = CopySpecialFiles()
        for path in self.inputDirectoriesPath:
            copySpecialFiles.specialFileNames.extend(copySpecialFiles.getSpecialFilesNames(path))
        self.assertEqual(sorted(self.specialFilesNamesAbsolutePath), sorted(copySpecialFiles.specialFileNames))

    def test_copyToDirectory(self):
        copySpecialFiles = CopySpecialFiles()
        for path in self.inputDirectoriesPath:
            copySpecialFiles.specialFileNames.extend(copySpecialFiles.getSpecialFilesNames(path))
        copySpecialFiles.outputDirectory = self.outputDirectory.path
        copySpecialFiles.copyToDirectory()
        self.assertEqual(sorted(os.listdir(self.outputDirectory.path)), sorted(self.specialFileNames))

    def test_copyToZip(self):
        copySpecialFiles = CopySpecialFiles()
        for path in self.inputDirectoriesPath:
            copySpecialFiles.specialFileNames.extend(copySpecialFiles.getSpecialFilesNames(path))
        copySpecialFiles.zipFile = "dummy.zip"
        copySpecialFiles.copyToZip()
        with zipfile.ZipFile('dummy.zip', 'r') as myzip:
            self.assertEqual(sorted(myzip.namelist()), sorted(self.specialFileNames))
        os.remove("dummy.zip")

    def tearDown(self):
        self.inputDirectory1.cleanup()
        self.inputDirectory2.cleanup()
        self.outputDirectory.cleanup()
