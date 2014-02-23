#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

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

def copyspecialfiles(directoryname):
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

def main():
    #usage: copy special names [-h] [--todir TODIR] [--zip ZIP]
    #                          inputdirectory [inputdirectory ...]
    #--todir and --zip ---> optional arguments
    #inputdirectory ---> positional arguments(mandatory argument)
    
    parser = argparse.ArgumentParser(description = 'Copy the special file names and do the appropriate action according to user input', prog ='copy special names')
    parser.add_argument('--todir','--todirectory', help = 'Files will be copied to this directory')
    parser.add_argument('--zip','--tozip', help = 'Copied files will be zipped into this file')
    parser.add_argument('inputdirectory',nargs='+', help = 'This is the input directory where the special file names will be searched')
    args = parser.parse_args()

    if args.todir:
        print 'to directory argument is given - %s' %(args.todir)
        output_directory = args.todir
        input_directory = args.inputdirectory
        print 'input directory argument is %s' %(input_directory)
    
    if args.zip:
        zipfile_name = args.zip
        input_directory = args.inputdirectory
        print 'Zip argument is given - %s' %(args.zip)
        
    if not args.todir and not args.zip:
        input_directory = args.inputdirectory
    
    #Pass the directory name to a function and get the special file names.
    copiedfilenames =[]
    for directoryname in input_directory:
        copiedfilenames = copyspecialfiles(directoryname)
    
    #if '--todir' option is given, write the special files to the given directory.
        if args.todir:
            absolutepath_todirectory = os.path.abspath(output_directory)
            if not os.path.exists(absolutepath_todirectory):
                print 'creating directory'
                os.mkdir(absolutepath_todirectory)
                print 'created directory'

            for filename in copiedfilenames:
                print 'copying files to the said directory'
                shutil.copy(filename,absolutepath_todirectory)

    #if '--zip' option is given, zip the files under the given zip file name  
        elif args.zip:
            current_working_directory = os.getcwd()
            zipfile_path = os.path.join(current_working_directory,zipfile_name)
            print 'zip file path is %s' %(zipfile_path)
            if not os.path.exists(zipfile_path):
                print 'creating zip file'
                zip_file = zipfile.ZipFile(zipfile_name, 'w')

            for filename in copiedfilenames:
                zip_file.write(filename)
        else:
            #If no option is given, just print it
            print copiedfilenames
    if args.zip:
        zip_file.close()

if __name__ == "__main__":
    main()