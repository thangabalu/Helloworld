import urllib
import re
import sys
import termcolor
import argparse

def remove_quotes_url(url):
	if url.startswith('"'):
		url = url[1:]
	if url.endswith('"'):
		url = url[:-1]	
	return url

def remove_quotes_title(title):
	if title.startswith('"'):
		title = title[1:]
	if title.endswith('"'):
		title = title[:-1]	
	return title

def prepare_list(url_list,dictionary_length, url_already_dictionary_size, ignore_already_dictionary, keyword_flag, keyword_list):
	dictionary ={}
	url_temporary_list=[]
	url_already_dictionary = 0

	while (len(dictionary) < dictionary_length) and (url_already_dictionary < url_already_dictionary_size):
		for url in url_list:
			url  = remove_quotes_url(url)
			htmlfile = urllib.urlopen(url).read()
			video_href= re.findall('<li class=\"video-list-item related-list-item\"><a href=\"(.*)\" class',htmlfile)
			video_title = re.findall('<span dir=\"ltr\" class=\"title\" title=\"(.*\")>',htmlfile)
    
			for title, href in zip(video_title,video_href):
				href = 'http://www.youtube.com'+href
				title = remove_quotes_title(title)
				href  = remove_quotes_url(href)
                
				if not ignore_already_dictionary:
					if url_already_dictionary > url_already_dictionary_size:
						print 'The number of repetitive urls reached the limit. Stopping the search.'
						break
					
				if len(dictionary) > dictionary_length:
					print 'The required size is reached. Stopping the search.'
					break
					
				if href in dictionary.values():
					url_already_dictionary += 1

				elif href not in dictionary.values() and 'span' not in title:
					if keyword_flag:
						url_temporary_list.append(href)
						for keyword in keyword_list:
							if keyword.lower() in title.lower():
								dictionary[title] = href
								break
					else:
						dictionary[title] = href
						url_temporary_list.append(href)
			
			if len(dictionary) > dictionary_length:
				break
			
			if not ignore_already_dictionary:
				if url_already_dictionary > url_already_dictionary_size:
					break

		if len(dictionary) > dictionary_length:
			break
		
		if not ignore_already_dictionary:
			if url_already_dictionary > url_already_dictionary_size:
				break
        
		#Emptying the list to accomodate the new list
		del url_list[:]
		url_list = url_temporary_list	
		
		print 'Now the size of the list is %d and the search is ongoing' %len(dictionary)
	return dictionary

def main():
    
    #If the user is not giving any url, default 
	#ToDO- Tamil letter is not coming in the extracted output
    # Ask the user whether to start from the youtube.com or particular link in the youtube.com
    
    #Usage should be something like
    #fetch.py -url(link1, link2, link3) -keyword(key1,key2,key3) -length(number) -stop(when the repetition is this number) -to (text file, html file, commandprompt) -wheretostart(homepage, or specific url)
	#add option for recommended videos
    
	file_type = ["text", "html", "excel"]
            
	parser = argparse.ArgumentParser(description = 'Prepare a list which has youtube video title and url according to user input', prog ='Fetch youtube videos')
	parser.add_argument('--listsize', type=int, help = 'The size of the output list. If this is not given, deafult value is 200')
	parser.add_argument('--keyword',  type=str, nargs='+', help = 'The extracted list will be filtered with this keywords')
	parser.add_argument('--stopsize', type=int, help = 'If the search exceeds this many repetitive urls, it would stop. If this is not given default value is 1000')
	parser.add_argument('--tofile',   choices=file_type, help = 'Specify where the output has to be written')
	parser.add_argument('--url',nargs='+', help = 'The search will be started from the related videos of this video. If this is not given, search will be started by default from user youtube home page. Please provide the entire url including http. ')
	args = parser.parse_args()
    
	keyword_flag = False
	keyword_list =[]
	if args.url:
		url_list = args.url
	if args.keyword:
		for key in args.keyword:
			print key
		keyword_list = args.keyword
		keyword_flag = True

	#Default value for dictionary_length is 200
	#Default value for url_already_dictionary_size is 1000
	ignore_already_dictionary = False
	if args.listsize:
		dictionary_length = args.listsize
		ignore_already_dictionary = True
	else:
		dictionary_length = 200
		
	if args.stopsize:
		url_already_dictionary_size = args.stopsize
	else:
		url_already_dictionary_size = 100 #Change this back to 1000


    #This is to search in www.youtube.com with recommended videos.
    #video_title = re.findall('<a class=\".*\"\s+ dir=\"ltr\"\s+title=\"(.*)\"\s+data-sessionlink=\".*\"\s+href=\"(.*\")\s+',htmlfile)
    #for title,url in video_title:
        #url = '"'+'http://www.youtube.com'+url
        #if url not in dictionary.values():
            #dictionary[title] = url
            #url_list.append(url)

	#Todo - Above for default option
	#Todo - excel
	#Add one more parameter - Asking how long the user would like to wait for the search. If the timer expires, return the so far fetched list
	#When searching add something like '..... .... .... ....' to show that it is in progress

	
	dictionary = {}
	dictionary = prepare_list(url_list, dictionary_length, url_already_dictionary_size, ignore_already_dictionary, keyword_flag, keyword_list)
    
    #Properly align the title and url
	maximum_length_title = max([len(title) for title in dictionary.keys()])
	maximum_length_url = max([len(url) for url in dictionary.values()])
    
	if not args.tofile:
		for title,url in dictionary.items():
			url = termcolor.colored(url,'red')
			print title.ljust(maximum_length_title + 2) + url.ljust(maximum_length_url)
	elif args.tofile == "text":
		output_file = open('output.txt','w')
		output_file.write('List size is %s' %len(dictionary) + '\n' )
		for title,url in dictionary.items():
			#url = termcolor.colored(url,'red')
			output_file.write(title.ljust(maximum_length_title + 2) + url.ljust(maximum_length_url) + '\n')
		output_file.close()
	elif args.tofile == "html":
		output_file = open('output.html','w')
		output_file.write('<html><body>')
		output_file.write('List size is %s' %len(dictionary)+ '<br>')
		i = 1
		for title,url in dictionary.items():
			#url = termcolor.colored(url,'red')
			output_file.write('<a href='+'"'+url+'"'+'>'+title+'</a>'+'<br>')
		output_file.write('</body></html>') 
		output_file.close()
	elif args.tofile == "excel":
		print 'Todo - Add code'

	print len(dictionary)

if __name__== "__main__":
    main()
