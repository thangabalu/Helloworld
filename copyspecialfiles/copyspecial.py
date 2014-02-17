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

"""Copy Special exercise
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
    print 'Usage: [--todir dir] [--tozip zipfile] dir dir dir'
    directorynames = sys.argv[1:]
    i = 0
    todirectory = 'false'
    tozip = 'false'
    todirectorypath = ''
    for arguments in directorynames:
        if arguments == '--todir':
            todirectory = 'true'
            index = i
        elif arguments == '--tozip':
            tozip = 'true'
            index = i
    #Removing '--todir' from arguments if it is present
    if todirectory == 'true':
        todirectorypath = directorynames[index+1]
        del directorynames[index:index+2]
        
    #Removing '--tozip' from arguments if it is present
    if tozip == 'true':
        zipfile_name = directorynames[index+1]
        del directorynames[index:index+2]
    
    #Pass the directory name to a function and get the special file names.
    copiedfilenames =[]
    for directoryname in directorynames:
        copiedfilenames = copyspecialfiles(directoryname)
    #if '--todir' option is given, write the special files to the given directory.
        if todirectory == 'true':
            absolutepath_todirectory = os.path.abspath(todirectorypath)
            if not os.path.exists(absolutepath_todirectory):
                print 'creating directory'
                os.mkdir(absolutepath_todirectory)
                print 'created directory'

            for filename in copiedfilenames:
                print 'copying files to the said directory'
                shutil.copy(filename,absolutepath_todirectory)

    #if '--tozip' option is given, zip the files under the given zip file name  
    #TODO : Check if the zipfile already exists. Don't create if it already exists
        elif tozip == 'true':
            current_working_directory = os.getcwd()
            zipfile_path = os.path.join(current_working_directory,zipfile_name)
            print 'zip file path is %s' %(zipfile_path)
            if not os.path.exists(zipfile_path):
                print 'creating zip file'
                zip_file = zipfile.ZipFile(zipfile_name, 'w')

            for filename in copiedfilenames:
                zip_file.write(filename)
        else:
            print copiedfilenames
    if tozip == 'true':
        zip_file.close()

if __name__ == "__main__":
    main()