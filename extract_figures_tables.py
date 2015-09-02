'''
This code does the following two things:
1. Extracts the figure references and makes a dictionary of these referenced by the appropriate figure number
2. Extracts the table references and makes a dictionary of these referenced by the appropriate table number
'''
import os
from lxml import etree

path = '/home/heather/Desktop/books/physical-sciences-12/english'

# create all the lists and dictionaries that we need
figure_dictionary = {}
table_dictionary = {}

# loop over the files in the directory
for file_name in os.listdir(path):

    full_file_name = '{}/{}'.format(path, file_name)
    
    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    # now we have another issue: the directory does not only contain xml files, we need to remove those that do not contain xml and those that do not start with a number.
    if file_name[-9:] != 'cnxmlplus':
        continue
    if file_name[0] not in ['0', '1', '2', '3']:
        continue
    
    xml = etree.XML(open(full_file_name, 'r').read())

    chapter_number = int(file_name[:2])  # set the chapter number and make it an integer
    figure_counter = 1  # start a figure counter running
    table_counter = 1  # start a table counter running
    
    for figure in xml.findall('.//figure'):  # find all the figures
        figure_type = figure.find('.//type')  # get the type of the figure
        if figure_type.text == 'figure': 
            try:  # not all figures have id's
                figure_id = figure.attrib('id')  # get the id
                figure_number = '{}.{}'.format(chapter_number, figure_counter)  # make the number
                figure_dictionary[figure_id] = '#{}'.format(figure_number)  # create a dictionary key-value pair
                figure_counter += 1  # increment the figure counter
            except TypeError:  # if there is not an id we get a type error
                continue
        elif figure_type.text == 'table':
            try:
                table_id = figure.attrib('id')
                table_number = '{}.{}'.format(chapter_number, table_counter)
                table_dictionary[table_id] = '#{}'.format(table_number)
                table_counter += 1
            except TypeError:
                continue

# write the contents of each dictionary and list to a file
with open('gr12-science-fig_refs.txt', 'w') as file:
    file.write(str(figure_dictionary))
    file.write('\n')
    file.write(str(table_dictionary))
