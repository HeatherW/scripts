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

#path = '/home/heather/Desktop/books/physical-sciences-12/afrikaans/build/epubs/science12/OPS/xhtml/science12'
#path = '/home/heather/Desktop/books/mathematics-10/afrikaans/build/epubs/maths10/OPS/xhtml/maths10'
path = '/home/heather/Desktop/books/scripts/test-files/html5_test'
#path = '/home/heather/Desktop/books/grade-10-mathslit-latex/afrikaans/build/epubs/maths-lit10v2/OPS/xhtml/maths-lit10v2'
file_list = os.listdir(path)
file_list.sort()

section_counter = 1
figure_counter = 1
table_counter = 1
worked_example_counter = 1
exercise_counter = 1
table_dictionary = {}
figure_dictionary = {}

for file_name in file_list:
    full_file_name = '{}/{}'.format(path, file_name)
    # Skip directories
    if os.path.isdir(full_file_name):
        continue
    if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
        continue

    xml = etree.parse(full_file_name, etree.HTMLParser())

    heading1 = xml.findall('.//h1')
    sections = xml.findall('.//section')
    divs = xml.findall('.//div')
    figures = xml.findall('.//figure[@id]')
    anchors = xml.findall('.//a')
    file_number = int(file_name[:2])

    # Create the chapter titles
    for h1 in heading1:
        newText = 'Chapter {}: {}'.format(file_number, h1.text)
        h1.text = newText

    file_counter = int(file_name[-17:-15])  # the end of every file name is .cnxmlplus.html which has length of 15, this extracts the number at the tail end of the file name
    # Handle section, subsection, exercise, worked example, table and figure numbering
    if file_counter == 0:
        section_counter = 1
        figure_counter = 1
        table_counter = 1
        worked_example_counter = 1
        exercise_counter = 1
    else:
        for section in sections:
            if section.find('h3') is not None:  # subsection headings
                h3 = section.find('h3')
                try:
                    shortcode = etree.Element('span')
                    shortcode.text = '({})'.format(section.attrib['id'][2:])
                    shortcode.set('class', 'shortcode')
                    h3.text = '{} '.format(h3.text)
                    h3.append(shortcode)
                except KeyError:
                    continue
            if section.attrib['class'] == 'worked_example':  # worked examples
                title = section.find('h2')
                try:
                    if title is not None:
                        title.text = 'Worked example {}: {}'.format(worked_example_counter, title.text)
                        worked_example_counter += 1
                except UnicodeEncodeError:
                    continue
            if section.attrib['class'] == 'exercises':  # exercises
                try:
                    problem_set = section.find('.//div[@class]')
                    if problem_set.attrib['class'] == 'problemset':
                        span_code = etree.Element('span')
                        span_code.set('class', 'exerciseTitle')
                        span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)
                        problem_set.insert(0, span_code)
                        exercise_counter += 1
                except AttributeError:
                    continue
            if section.find('h2') is not None:  # section headings
                h2 = section.find('h2')
                try:
                    if section.attrib['id'] is not None and section.attrib['id'][:2] == 'sc':
                        shortcode = etree.Element('span')
                        shortcode.text = '({})'.format(section.attrib['id'][2:])
                        shortcode.set('class', 'shortcode')
                        h2.text = '{}.{} {}'.format(file_number, section_counter, h2.text)
                        h2.append(shortcode)
                        section_counter += 1
                except KeyError:
                    continue

    # figure numbering
    for figure in figures:
        caption = figure.find('.//figcaption')
        if caption is not None and figure.attrib['id'] is not None:
            caption.text = 'Figure {}.{}: {}'.format(file_number, figure_counter, caption.text)
            figure_dictionary[figure.attrib['id']] = str(file_number) + '.' + str(figure_counter)
            figure_counter += 1

    # table numbering
    for div in divs:
        try:
            if div.attrib['class'] is not None:
                if div.attrib['id'] is not None and div.attrib['class'] == 'FigureTable':
                    caption = div.find('.//div[@caption]')
                    if caption is not None:
                        caption.text = 'Table {}.{}: {}'.format(file_number, table_counter, caption.text)
                        table_dictionary[div.attrib['id']] = str(file_number) + '.' + str(table_counter)
                        table_counter += 1
        except KeyError:
            continue

    # replace the anchor tags
    for anchor in anchors:
        try:
            if anchor.attrib['class'] == 'InternalLink':
                if anchor.attrib['href'][1:] in table_dictionary.keys():
                    anchor.text = 'Table ' + table_dictionary[anchor.attrib['href'][1:]]
                elif anchor.attrib['href'][1:] in figure_dictionary.keys():
                    anchor.text = 'Figure ' + figure_dictionary[anchor.attrib['href'][1:]]
        except KeyError:
            continue

    fileText = None
    fileText = etree.tostring(xml, pretty_print=True)

    # This overwrites the contents of the file you are working with. Only do this if you are sure you can get the contents of the file back before the script was run.
    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)
