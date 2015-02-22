#!/usr/bin/python

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands
import zipfile
import argparse

"""Copy Special exercise
The copyspecial.py program takes one or more directories as its arguments. A "special" file is one where the name contains the pattern __w__ somewhere, 
where the w is one or more word chars.

Special files will be treated depending on the input given by the user.

usage: copy special names [-h] [--todir TODIR] [--zip ZIP]
                          inputdirectory [inputdirectory ...]

"""
class CopySpecialFiles():

    def __init__(self):
        self.outputDirectory = None
        self.zipFile = None
        self.specialFileNames = []

    def getSpecialFilesNames(self, directoryname):
        filenames = os.listdir(directoryname)
        absolutepath_list =[]
        for filename in filenames:
            path = os.path.join(directoryname,filename)
            absolutepath = os.path.abspath(path)
            if os.path.isfile(absolutepath):
                match = re.match('.*__\w+__.*', filename)
                if match:
                    absolutepath_list.append(absolutepath)
        return absolutepath_list

    def copyToDirectory(self):
        absolutepath_todirectory = os.path.abspath(self.outputDirectory)
        if not os.path.exists(absolutepath_todirectory):
            os.mkdir(absolutepath_todirectory)
            print 'created directory'

        print 'copying files to the said directory'
        for filename in self.specialFileNames:
            shutil.copy(filename,absolutepath_todirectory)

    def copyToZip(self):
        current_working_directory = os.getcwd()
        zipfile_path = os.path.join(current_working_directory,self.zipFile)
        print 'zip file path is %s' %(zipfile_path)
        if not os.path.exists(zipfile_path):
            zip_file = zipfile.ZipFile(self.zipFile, 'w')
            print 'created zip file'

        for filename in self.specialFileNames:
            baseName = os.path.basename(filename)
            zip_file.write(filename, baseName)
        zip_file.close()


def main():
    #usage: copy special names [-h] [-todir TODIR] [-zip ZIP]
    #                          inputdirectory [inputdirectory ...]
    #-todir and -zip ---> optional arguments
    #inputdirectory ---> positional arguments(mandatory argument)
    
    parser = argparse.ArgumentParser(description = 'Copy the special file names and do the appropriate action according to user input', prog ='Copy special names')
    parser.add_argument('-todir', help = 'Files will be copied to this directory')
    parser.add_argument('-zip', help = 'Copied files will be zipped into this file')
    parser.add_argument('inputdirectory',nargs='+', help = 'This is the input directory where the special file names will be searched')
    args = parser.parse_args()

    copySpecialFiles = CopySpecialFiles()

    input_directory = args.inputdirectory
    print 'input directory argument is %s' %(input_directory)

    #Pass the input directory name to a function and get the special file names.
    for directoryname in input_directory:
        copySpecialFiles.specialFileNames.extend(copySpecialFiles.getSpecialFilesNames(directoryname))

    if args.todir:
        print 'to directory argument is given - %s' %(args.todir)
        copySpecialFiles.outputDirectory = args.todir
        copySpecialFiles.copyToDirectory()

    elif args.zip:
        copySpecialFiles.zipFile = args.zip
        print 'Zip argument is given - %s' %(args.zip)
        copySpecialFiles.copyToZip()

    else:
        #If no option is given, just print it
        for fileName in copySpecialFiles.specialFileNames:
            print fileName


if __name__ == "__main__":
    main()
