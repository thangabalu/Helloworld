import urllib
import re
import sys
import termcolor


def main():
    
    url_parameter = sys.argv[1]

    #write it to a file or html or in any format which user asks
    # Ask the user whether to start from the youtube.com or particular link in the youtube.com
    
    #Usage should be something like
    #fetch.py -url(link1, link2, link3) -keyword(key1,key2,key3) -length(number) -stop(when the repetition is this number) -to (text file, html file, commandprompt) -wheretostart(homepage, or specific url)
    
    
    #This is to search in www.youtube.com with recommended videos.
    #video_title = re.findall('<a class=\".*\"\s+ dir=\"ltr\"\s+title=\"(.*)\"\s+data-sessionlink=\".*\"\s+href=\"(.*\")\s+',htmlfile)
    #for title,url in video_title:
        #url = '"'+'http://www.youtube.com'+url
        #if url not in dictionary.values():
            #dictionary[title] = url
            #url_list.append(url)
    
    dictionary ={}
    url_list =[url_parameter]
    url_temporary_list=[]
    url_already_dictionary = 0
    url_already_dictionary_size = 10000
    dictionary_length = 3000

    while (len(dictionary) < dictionary_length) and (url_already_dictionary < url_already_dictionary_size):
        for url in url_list:
            if url.startswith('"'):
                url = url[1:]
            if url.endswith('"'):
                url = url[:-1]
            
            htmlfile = urllib.urlopen(url).read()
            video_href= re.findall('<li class=\"video-list-item related-list-item\"><a href=\"(.*)\" class',htmlfile)
            video_title = re.findall('<span dir=\"ltr\" class=\"title\" title=\"(.*\")>',htmlfile)
    
            for title, href in zip(video_title,video_href):
                href = 'http://www.youtube.com'+href
                
                if url_already_dictionary > url_already_dictionary_size or len(dictionary) > dictionary_length:
                    break
                if href.startswith('"'):
                    href = href[1:]
                if href.endswith('"'):
                    href = href[:-1]
                if title.startswith('"'):
                    title = title[1:]
                if title.endswith('"'):
                    title = title[:-1]
                if href in dictionary.values():
                    url_already_dictionary += 1
                    print 'url already in dictionary and the total count is %s' %(url_already_dictionary)
                if href not in dictionary.values():
                    dictionary[title] = href
                    url_temporary_list.append(href)
            if url_already_dictionary > url_already_dictionary_size or len(dictionary) > dictionary_length:
                break
        if url_already_dictionary > url_already_dictionary_size or len(dictionary) > dictionary_length:
            break    
        
        #Emptying the list to accomodate the new list
        del url_list[:]
        url_list = url_temporary_list
    
    maximum_length_title = max([len(title) for title in dictionary.keys()])
    maximum_length_url = max([len(url) for url in dictionary.values()])
    
    for title,url in dictionary.items():
        url = termcolor.colored(url,'red')
        print title.ljust(maximum_length_title + 2) + url.ljust(maximum_length_url)

    print len(dictionary)
    


if __name__== "__main__":
    main()