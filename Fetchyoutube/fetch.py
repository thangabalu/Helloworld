import urllib
import re
import sys
import termcolor


def main():
    htmlfile = urllib.urlopen('http://www.youtube.com').read()
    dictionary ={}
    print 'started searching'
    video_title = re.findall('<a class=\".*\"\s+ dir=\"ltr\"\s+title=\"(.*)\"\s+data-sessionlink=\".*\"\s+href=\"(.*)\"\s+',htmlfile)
    print 'completed searching'
    for title,url in video_title:
        url = "http://www.youtube.com"+url
        dictionary[title] = url
    
    maximum_length_title = max([len(title) for title in dictionary.keys()])
    maximum_length_url = max([len(url) for url in dictionary.values()])
    
    for title,url in dictionary.items():
        url = termcolor.colored(url,'red')
        print title.ljust(maximum_length_title + 2) + url.ljust(maximum_length_url)
        

if __name__== "__main__":
    main()