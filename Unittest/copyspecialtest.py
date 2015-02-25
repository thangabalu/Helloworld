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
        self.inputDirectory = []
        self.specialFilesNamesAbsolutePath = []
        self.specialFileNames =[]
        self.inputDirectoriesPath = []
        for i in range(0,2):
            self.inputDirectory.append(TempDirectory())
            self.inputDirectory[i].write('india__{0}{0}{0}__.txt'.format(i), 'some foo thing')
            self.inputDirectory[i].write('god__{0}{0}{0}__.txt'.format(i), 'some foo thing')
            self.inputDirectory[i].write('hi.txt', 'some foo thing')

            self.specialFilesNamesAbsolutePath.append('{0}/india__{1}{1}{1}__.txt'.format(self.inputDirectory[i].path, i))
            self.specialFilesNamesAbsolutePath.append('{0}/god__{1}{1}{1}__.txt'.format(self.inputDirectory[i].path, i))
            self.specialFileNames.append('india__{0}{0}{0}__.txt'.format(i))
            self.specialFileNames.append('god__{0}{0}{0}__.txt'.format(i))
            self.inputDirectoriesPath.append(self.inputDirectory[i].path)

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
        for inputDirectory in self.inputDirectory:
            inputDirectory.cleanup()
        self.outputDirectory.cleanup()
