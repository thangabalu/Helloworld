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

"""Fetch university
Make a list of the name of the university and the URL from different web pages
in a website and write them to a file. I am writing this program to learn how
to fetch particular data from a webpage
"""

def read_urls(inputurls):
    collegedictionary ={}
    for url in inputurls:
        print 'Retrieving %s' %(url)
        urllib.urlretrieve(url,"universitysourcecode.html")
        sourcecode = open("universitysourcecode.html", 'rU')
        sourcecode_contents = sourcecode.read()
    #Different way to avoid creating a html file
    #htmlfile = urllib.urlopen("www.google.com").read()

        #Extract the college name and the url
        Url_Title_tuple = re.findall('<h2 class=\"college_name\"><a href=(\"\S+) title=\"(.*)\" onClick',sourcecode_contents)

        #Put it in a dictionary
        for Url, title in Url_Title_tuple:
            collegedictionary[title] = Url

    maximum_length_title = max([len(row) for row in collegedictionary.keys()])
    maximum_length_url = max([len(row) for row in collegedictionary.values()])   
    create_file = open('Extracted_colleges', 'w')
    create_file.write('Collegename'.ljust(maximum_length_title+2) + 'URL'.ljust(maximum_length_url) + '\n')
    for title, Url in collegedictionary.items():
        create_file.write(title.ljust(maximum_length_title+2) + Url.ljust(maximum_length_url) + '\n')
    create_file.close()

def main():
    url_list=[]
    for i in range(1, 36):
        url_list.append('http://www.indiacollegesearch.com/engineering/colleges-tamil-nadu?page=%i'%(i))
    read_urls(url_list)
    #http://www.indiacollegesearch.com/engineering/colleges-tamil-nadu?page=1
    
if __name__ == "__main__":
  main()