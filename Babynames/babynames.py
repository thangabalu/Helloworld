#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Here's what the html file(input file/files) looks like in the baby.html files:

...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

If the 'summaryfile' is passed in the command line arguments, output should be written to a file.
If not, output should be just printed.
Year, name and Rank should be printed. And the list has to be sorted by name.
Here is the format.

1990
Aaliyah 222
Aaron 37
Abbey 408
...

"""

def extract_names(filename):
  	# Open the file and read the contents and store as a single string
  	file=open(filename,'rU')
	Text_in_file = file.read()
	file.close()
	
	# Extract the year from the given input file and store it in the list 'Year_name_rank_list'
	Year_name_rank_list =[]
	match = re.search('.*Popularity\s\w\w\s(\d\d\d\d).*', Text_in_file)
	if match:
		Year_name_rank_list.append(match.group(1))
	else:
		print 'not found'

	# Tablecolumns is tuple	which have (rank,boy_name,girl_name)
	# Extract the name and rank and store it in the dictionary. Add both boy and girl names in the same dictionary
	# If a name is added in the dictionary, don't add again even if the name appears again in the file for different gender
	Tablecolumns = re.findall(r'.*<tr\s\w\w\w\w\w=".*"><td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', Text_in_file)
	Rank_and_names_dictionary ={}
	for rank,boy_name,girl_name in Tablecolumns:
		if boy_name not in Rank_and_names_dictionary:
			Rank_and_names_dictionary[boy_name] = rank
		if girl_name not in Rank_and_names_dictionary:
			Rank_and_names_dictionary[girl_name] = rank
	
	# Sort the 'Rank_and_names_dictionary' by name and store it in a list
	for name, rank in sorted(Rank_and_names_dictionary.items(), key = lambda x: x[0]):
		Year_name_rank_list.append(name + " " + rank)

	return Year_name_rank_list



    
def main():

    if len(sys.argv) < 2 :
        print 'usage: [--summaryfile] file [file ...]'
        sys.exit(1)
    filenames = sys.argv[1:]


    #Check if the summary flag is given in the input and remove it from the 'filenames' list.
    summary = False	
    if filenames[0] == '--summaryfile':
		summary = True
		del filenames[0]

    # Multiple filenames can be given in the command line arguments
    # Pass the filename to the function 'extract_names' and get the extracted list which have year, name and rank
    # If the summary flag is set, write the list to a file. If not, just print the list.

    for filename in filenames:
        Extracted_year_name_list = extract_names(filename)
        if summary == True:
            outfile = open(filename + '.summary', 'w')
            for name_rank in Extracted_year_name_list:
                outfile.write(name_rank + '\n')
            outfile.close()
        else:
            print '\n'.join(Extracted_year_name_list)

  
if __name__ == '__main__':
  main()
