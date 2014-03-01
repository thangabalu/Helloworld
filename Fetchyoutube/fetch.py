import urllib
import re
import sys
import termcolor
import argparse
import time
import xlsxwriter


def remove_quotes_url(url):
	"""
	Function to remove extra quotes from the given url
	"""
	if url.startswith('"'):
		url = url[1:]
	if url.endswith('"'):
		url = url[:-1]
	return url

def remove_quotes_title(title):
	"""
	Function to remove extra quotes from the given title
	"""
	if title.startswith('"'):
		title = title[1:]
	if title.endswith('"'):
		title = title[:-1]
	return title

def find_maximum_length_dictionary_in_items(dictionary):
	"""
	Function to find the maximum length of dictionary items
	"""	
	maximum_length_title = max([len(title) for title in dictionary.keys()])
	maximum_length_url = max([len(url) for url in dictionary.values()])
	
	return {'title': maximum_length_title, 'url' : maximum_length_url}
	
def print_in_prompt(dictionary):
	"""
	Function to print the output in the user prompt
	"""
	maximum_length = find_maximum_length_dictionary_in_items(dictionary)

	for title,url in dictionary.items():
		url = termcolor.colored(url,'red')
		print title.ljust(maximum_length['title'] + 2) + url.ljust(maximum_length['url'])
	
def print_in_textfile(dictionary):
	"""
	Function to print the output in a text file
	"""
	maximum_length = find_maximum_length_dictionary_in_items(dictionary)
	output_file = open('output.txt','w')
	output_file.write('List size is %s' %len(dictionary) + '\n' )
	for title,url in dictionary.items():
		#url = termcolor.colored(url,'red') Color is not working. Need to check
		output_file.write(title.ljust(maximum_length['title'] + 2) + url.ljust(maximum_length['url']) + '\n')
	output_file.close()

def print_in_html(dictionary):
	"""
	Function to print the output in a html file
	"""
	output_file = open('output.html','w')
	output_file.write('<html><body>')
	output_file.write('List size is %s' %len(dictionary)+ '<br>')
	for title,url in dictionary.items():
		#url = termcolor.colored(url,'red')
		output_file.write('<a href='+'"'+url+'"'+'>'+title+'</a>'+'<br>')
	output_file.write('</body></html>') 
	output_file.close()

def print_in_excel(dictionary):
	"""
	Function to print the output in an excel file.
	As of now, it writes only url since I am not able to write the title. It is throwing unicodedecodeError. 
	Don't know how to fix it
	"""
	maximum_length = find_maximum_length_dictionary_in_items(dictionary)

	# Create a new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook('output.xlsx')
	worksheet = workbook.add_worksheet()

	# Widen the first column to make the text clearer.
	worksheet.set_column('A:A', maximum_length['title'])
	
	# Widen the second column to make the text clearer.
	worksheet.set_column('B:B', maximum_length['url'])

	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})

	# Write some simple text with formatting
	worksheet.write('A1', 'Title',bold) # This is equal to worksheet.write(0, 0, 'Hello')
	worksheet.write('B1', 'Url', bold)  # This is equal to worksheet.write(0, 1, 'Title')
	
	row = 1
	try:
		for title, url in dictionary.items():
			if isinstance(title, str):
				#worksheet.write_string(row,0,title)
				worksheet.write_url(row,1,url)
				row += 1
		workbook.close()
	except UnicodeDecodeError:
		print 'UnicodeDecodeError catched'


def prepare_list(url_list,dictionary_length, url_already_dictionary_size, ignore_already_dictionary, keyword_flag, keyword_list, urldefault_flag):
	
	"""
	Function to prepare the list which have title of the youtube video and their url.
	"""
	dictionary ={}
	url_temporary_list=[]
	url_already_dictionary = 0

	if urldefault_flag:
		#This is to start the search in www.youtube.com with recommended videos.
		htmlfile = urllib.urlopen('http://www.youtube.com').read()
		video_title = re.findall('<a class=\".*\"\s+ dir=\"ltr\"\s+title=\"(.*)\"\s+data-sessionlink=\".*\"\s+href=\"(.*\")\s+',htmlfile)
		for title,url in video_title:
			url = '"'+'http://www.youtube.com'+url
			if url not in dictionary.values():
				dictionary[title] = url
				url_list.append(url)
		print 'Now the size of the list is %d and the search is ongoing' %len(dictionary)


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
			#Todo - Need to do something to fix this \r.
			print 'Now the size of the list is %d and the search is ongoing' %len(dictionary)
			
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
	return dictionary

def main():
    
	#ToDO- Tamil letter is not coming in the extracted output
	#Add one more parameter - Asking how long the user would like to wait for the search. If the timer expires, return the so far fetched list
	
	file_type = ["text", "html", "excel","cmdprompt"]
            
	parser = argparse.ArgumentParser(description = 'Prepare a list which has youtube video title and url according to user input', prog ='Fetch youtube videos')
	parser.add_argument('--listsize', type=int, help = 'The size of the output list. If this is not given, default value is 200')
	parser.add_argument('--keyword',  type=str, nargs='+', help = 'The extracted list will be filtered with these keywords')
	parser.add_argument('--stopsize', type=int, help = 'If the search exceeds this many repetitive urls, it would stop. If this is not given default value is 1000')
	parser.add_argument('--tofile',   choices=file_type, help = 'Specify where the output has to be written. If this is not given, it will be written in the user prompt')
	parser.add_argument('--url',nargs='+', help = 'The search will be started from the related videos of this video/videos. If this is not given, search will be started by default from user youtube home page. Please provide the entire url including http. ')
	args = parser.parse_args()
    
	keyword_flag = False
	urldefault_flag = False
	keyword_list =[]
	if args.url:
		url_list = args.url
	else:
		url_list = ['http://www.youtube.com']
		urldefault_flag = True
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
		url_already_dictionary_size = 1000

	dictionary = {}
	dictionary = prepare_list(url_list, dictionary_length, url_already_dictionary_size, ignore_already_dictionary, keyword_flag, keyword_list,urldefault_flag)
    
	if args.tofile == "text":
		print_in_textfile(dictionary)
	
	elif args.tofile == "html":
		print_in_html(dictionary)

	elif args.tofile == "excel":
		print_in_excel(dictionary)

	elif args.tofile == "cmdprompt" or not args.tofile:
		print_in_prompt(dictionary)

if __name__== "__main__":
    main()
