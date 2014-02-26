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
import argparse

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
def download_images(urls,directorypath):
    i = 0
    indexfile_path = os.path.join(directorypath,'index.html')

    # Open a html file
    index_file = open(indexfile_path,'w')
    index_file.write('<html><body>')
    for url in urls:
        filename = 'image%s' %(i)
        filename_path = os.path.join(directorypath,filename)
        print 'Retrieving %s' %(url)
        urllib.urlretrieve(url,filename_path)
        index_file.write('<img src ="%s">' %(filename))
        i += 1
    index_file.write('</body></html>')    
    index_file.close()
    

def main():

    #usage:  Puzzle [-h] [--todir TODIR] logfile
    #--todir---> optional arguments
    #logfile ---> positional arguments(mandatory argument)

	parser = argparse.ArgumentParser(description = 'Given an apache logfile, find the puzzle urls and download the images.', prog ='Puzzle')
	parser.add_argument('--todir','--todirectory', help = 'Extracted Files will be copied to this directory')
	parser.add_argument('logfile', help = 'The input log file where puzzle url will be searched')
	args = parser.parse_args()    
	print args.todir
	print args.logfile

	if args.todir:
		absolute_directory_path = os.path.abspath(args.todir)

	logfile_name = args.logfile

    #Extract the url's from the given log file and download the images to a directory if --todir option is given
	#Or just print the url's in the screen
	urls = read_urls(logfile_name)
	if args.todir:
		if not os.path.exists(absolute_directory_path):
			os.mkdir(absolute_directory_path)
		download_images(urls,absolute_directory_path)
	else:
		for url in urls:
			print url
  
if __name__ == "__main__":
  main()
