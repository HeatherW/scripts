'''Automatic numbering script
This script does the following:
1. Updates the anchor tags to have the correct figure or table reference. This is only needed for science at present.
2. Updates the figure and table caption tags to have a prefix of table x: or figure x:. Again only for science.
3. Updates chapter titles, section titles and subsection titles. Chapter titles need chapter x: as  a prefix, section titles need 'no. title shortcode' and subsection titles just need the shortcode at the end.
4. Numbers the worked examples.
5. Numbers the exercises
'''

# Import the necessary items
import os

from lxml import etree

'/home/heather/Desktop/books/mathematics-10/afrikaans/build/epubs/maths10/OPS/xhtml/maths10'
path = '/home/heather/Desktop/books/scripts/tests/sample-files-for-testing/unnumbered_files'
file_list = os.listdir(path)
file_list.sort()


class NumberingClass():
    '''
    The workhorse for numbering all the pieces of the html
    '''
    
    def __init__(self, file_list):
        self.file_list = file_list
        self.numbered_files = {}
        self.section_number = 1
        self.figure_number = 1
        self.table_number = 1
        self.worked_example_number = 1
        self.exercise_number = 1
        self.table_dictionary = {}
        self.figure_dictionary = {}

    def number_files(self, write_back_to_file_boolean=True):
        for file_name in self.file_list:
            # Skip directories
            full_file_name = '{}/{}'.format(path, file_name)
            if os.path.isdir(full_file_name):
                continue
            if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
                continue

            self.numbered_files[file_name] = self.number_file(full_file_name)
            
        if not write_back_to_file_boolean:
            return
        
        for file_name in self.numbered_files.keys():
            if self.numbered_files[file_name]:
                full_file_name = '{}/{}'.format(path, file_name)
                file_text = self.number_file(full_file_name)
                self.write_back_to_file(file_text, full_file_name)
            
    def number_file(self, full_file_name):
        xml = etree.parse(full_file_name, etree.HTMLParser())

        heading1 = xml.find('.//h1')
        sections = xml.findall('.//section')
        divs = xml.findall('.//div')
        figures = xml.findall('.//figure[@id]')
        anchors = xml.findall('.//a')
        find_chapter_number_index = full_file_name.rfind('/')
        file_number = int(full_file_name
                          [find_chapter_number_index+1:find_chapter_number_index+3])
        
        def chapter_number_insert(self):
            # Create the chapter titles
            if heading1 is not None:
                newText = 'Chapter {}: {}'.format(file_number, heading1.text)
                heading1.text = newText
                return heading1


        file_counter = int(full_file_name[-17:-15])  # the end of every file name is .cnxmlplus.html which has length of 15, this extracts the number at the tail end of the file name
        # Handle section, subsection, exercise, worked example, table and figure numbering
        #if file_counter == 0:
            #section_number = 1
            #figure_number = 1
            #table_number = 1
            #worked_example_counter = 1
            #exercise_counter = 1
        #else:
            #for section in sections:
                #if section.find('h3') is not None:  # subsection headings
                    #h3 = section.find('h3')
                    #try:
                        #shortcode = etree.Element('span')
                        #shortcode.text = '({})'.format(section.attrib['id'][2:])
                        #shortcode.set('class', 'shortcode')
                        #h3.text = '{} '.format(h3.text)
                        #h3.append(shortcode)
                    #except KeyError:
                        #continue
                #if section.attrib['class'] == 'worked_example':  # worked examples
                    #title = section.find('h2')
                    #if title is not None:
                        #title.text = 'Worked example ' + str(worked_example_counter) + ':' + title.text  # while .format or other string concatenation methods might work better this handles unicode errors better
                        #worked_example_counter += 1
                #if section.attrib['class'] == 'exercises':  # exercises
                    #try:
                        #problem_set = section.find('.//div[@class]')
                        #if problem_set.attrib['class'] == 'problemset':
                            #span_code = etree.Element('span')
                            #span_code.set('class', 'exerciseTitle')
                            #span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)
                            #problem_set.insert(0, span_code)
                            #exercise_counter += 1
                    #except AttributeError:
                        #continue
                #if section.find('h2') is not None:  # section headings
                    #h2 = section.find('h2')
                    #try:
                        #if section.attrib['id'] is not None and section.attrib['id'][:2] == 'sc':
                            #shortcode = etree.Element('span')
                            #shortcode.text = '({})'.format(section.attrib['id'][2:])
                            #shortcode.set('class', 'shortcode')
                            #h2.text = '{}.{} {}'.format(file_number, self.section_number, h2.text)
                            #h2.append(shortcode)
                            #self.section_number += 1
                    #except KeyError:
                        #continue


        # figure numbering
        def figure_number_insert(self):
            for figure in figures:
                caption = figure.find('.//figcaption')
                if caption is not None and figure.attrib['id'] is not None:
                    if caption.find('.//p') is not None:
                        para = caption.find('.//p')
                        para.text = 'Figure {}.{}: {}'.format(file_number, self.figure_number, para.text)
                    else:
                        caption.text = 'Figure {}.{}: {}'.format(file_number, self.figure_number, caption.text)
                    self.figure_dictionary[figure.attrib['id']] = str(file_number) + '.' + str(self.figure_number)
                    self.figure_number += 1
                    return caption


        # table numbering
        def table_number_insert(self):
            for div in divs:
                try:
                    if div.attrib['class'] is not None:
                        if div.attrib['id'] is not None and div.attrib['class'] == 'FigureTable':
                            caption = div.find('.//div[@caption]')
                            if caption is not None:
                                if caption.find('.//p') is not None:
                                    para = caption.find('.//p')
                                    para.text = 'Table {}.{}: {}'.format(file_number, table_number, para.text)
                                else:
                                    caption.text = 'Table {}.{}: {}'.format(file_number, table_number, caption.text)
                                table_dictionary[div.attrib['id']] = str(file_number) + '.' + str(table_number)
                                table_number += 1
                                return caption
                except KeyError:
                    continue


        # replace the anchor tags
        def hyperlink_text_fix(self):
            for anchor in anchors:
                try:
                    if anchor.attrib['class'] == 'InternalLink':
                        if anchor.attrib['href'][1:] in table_dictionary.keys():
                            anchor.text = 'Table ' + table_dictionary[anchor.attrib['href'][1:]]
                        elif anchor.attrib['href'][1:] in figure_dictionary.keys():
                            anchor.text = 'Figure ' + figure_dictionary[anchor.attrib['href'][1:]]
                        return anchor
                except KeyError:
                    continue
        
        if chapter_number_insert(self) is not None:
            xml = chapter_number_insert(self)
        if figure_number_insert(self) is not None:
            xml = figure_number_insert(self)
        if table_number_insert(self) is not None:
            xml = table_number_insert(self)
        if hyperlink_text_fix(self) is not None:
            xml = hyperlink_text_fix(self)
        
        file_text = None
        
        file_text = etree.tostring(xml, pretty_print=True)
        return file_text

    def write_back_to_file(self, file_text, full_file_name):
        # This overwrites the contents of the file you are working with. 
        # Only do this if you are sure you can get the contents of the file back 
        # before the script was run.
        with open(full_file_name, 'w') as file:
            file.write(file_text)
        
