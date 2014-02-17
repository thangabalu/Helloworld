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
import urllib

"""Puzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

#This function extracts the required path from the log file and create a complete puzzle urls which can be used in other function to retrieve images.
#Input argument - logfile name
#Return - Puzzle URL's list
def read_urls(logname):
    urls = []
    http='http://'
    #Extract the hostname from the log file name
    #Example: Log file name - animal_code.google.com
    #Host - code.google.com
    match = re.search(r'_(\S+)',logname)
    if match:
        host = match.group(1)
    
    #Adding 'http://' to the host
    full_host = http+host
    log_file = open(logname, 'rU')
    file_contents=log_file.read()
    
    #Extract the path from the 'GET' part in the log file
    paths = re.findall(r'GET\s(\S+)',file_contents)
    
    #Extract the path which has the word 'puzzle' and add it to the url list along with the full host name
    for path in sorted(paths):
        if 'puzzle' in path:
            urls.append(full_host+path)
    return urls

# This function retrieves the images from the given puzzle Url's and write them in a html file.
# Input argument - List of puzzle URL's
# Return - nothing
def download_images(urls):
    print 'downloading images'
    i = 0
    
    # Open a html file
    index_file = open('index.html', 'w')
    index_file.write('<html><body>')
    for url in urls:
        filename = 'image%s' %(i)
        print 'Retrieving %s' %(url)
        urllib.urlretrieve(url,filename)
        index_file.write('<img src ="%s">' %(filename))
        i += 1
    index_file.write('</body></html>')    
    index_file.close()
    

def main():
    #TODO - Command line arguments should be evaluated to check whether the needed input is given and any unnecessary input is given.
    print 'usage: [--todir dir] logfile '
    arguments = sys.argv[1:]
    i=0
    todirectory='false'

    # if '--todir' is given in input, process the inputs to fetch the output folder name.
    for argument in arguments:
        if argument == '--todir':
            todirectory = 'true'
            todirectory_index = i
    if todirectory == 'true':
        directory_path = arguments[todirectory_index+1]
        absolute_directory_path = os.path.abspath(directory_path)
        del(arguments[todirectory_index:todirectory_index+2])

    #Take the log file name and call the necessary functions according to '--todir' option is present or not
    logname = arguments[0]
    urls = read_urls(logname)
    if todirectory == 'true':
        if not os.path.exists(absolute_directory_path):
            os.mkdir(absolute_directory_path)
        download_images(urls)
    else:
        for url in urls:
            print url
  
if __name__ == "__main__":
  main()