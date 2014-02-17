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
"""

def read_urls(logname):
    urls = []
    http='http://'
    match = re.search(r'_(\S+)',logname)
    if match:
        host = match.group(1)
    full_host = http+host
    file = open(logname, 'rU')
    file_contents=file.read()
    paths = re.findall(r'GET\s(\S+)',file_contents)
    for path in sorted(paths):
        if 'puzzle' in path:
            urls.append(full_host+path)
    return urls

def download_images(urls):
    print 'downloading images'
    i = 0
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
    print 'usage: [--todir dir] logfile '
    arguments = sys.argv[1:]
    i=0
    todirectory='false'
    for argument in arguments:
        if argument == '--todir':
            todirectory = 'true'
            todirectory_index = i
    if todirectory == 'true':
        directory_path = arguments[todirectory_index+1]
        absolute_directory_path = os.path.abspath(directory_path)
        del(arguments[todirectory_index:todirectory_index+2])
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
