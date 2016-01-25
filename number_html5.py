'''Attempting to make an automatic numbering script
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

# Make the figure reference dictionary (for grade 12 science at present)
#fig_ref_dict = {"#fig:scienceskills:science":"1.1",}

# and the table ref dictionary
#table_ref_dict = {"#table:momentumandimpulse:units":"2.1",}


# number the figure and table references
def fig_ref_fix(xml):
    '''current code is <a href="blah" data-class="InternalLink">blah</a>. We want this to become <a href="blah" data-class="InternalLink">figure x</a> or table x if we are doing the tables'''
    for a in xml.findall('.//a'):
        aTag = etree.Element('a')
        href = a.get('href')  # the href of the tag
        if href in fig_ref_dict:  # we find the hRef in the figure keys
            aTag.clear()  # clear the contents of the tag
            a.text = 'Figure {}'.format(fig_ref_dict[href])  # replace the text of the tag with the value of the key in the fig ref dict and the word Figure
        elif href in table_ref_dict:  # we find the hRef in the table keys
            aTag.clear()  # clear the contents of the tag
            a.text = 'Table {}'.format(table_ref_dict[href])  # replace the text of the tag with the value of the key in the table ref dict and the word Table
    return xml  # returns what we need


# the other piece is to fix the captions
def fig_caption(xml):
    '''current code is <div id="fig-atom-plumpudding" class="figure"><img src="pspicture/90cffe92260bc3815a6825cbb0d87b39.png" alt="90cffe92260bc3815a6825cbb0d87b39.png"/><div class="figcaption"><p>The atom according to the Plum Pudding model.</p></div></div>. We need to identify the figure from the overarching href and then modify the caption div to state: Figure x: blah
    To repeat for tables we need to take the current code: <div id="blah" data-class="FigureTable"><table>code</table><div class="caption"><p>caption</p></div></div>, identify the table and modify the caption to state Table y: blah
    '''
    for div in xml.findall('.//div[@class]'):  # find all divs with attribute class
        if div.attrib['class'] == 'figure':  # only work on the divs we actually want, this may change to be the same as the tables
            caption = div.find('.//div')
            if caption is not None:
                caption = div.find('.//div').find('.//p')  # extract just the caption bit
                try:
                    figId = '#' + div.attrib['id'].replace('-', ':')  # temporary hack to get the id's correct, the # will always be needed but the replace can be removed when the validator updates are completed
                    #div.set('id', figId)  # attempting to put in a hack to fix the id problem
                    if figId in fig_ref_dict:
                        # caption.text = 'Figure ' + fig_ref_dict[figId] + ': ' + caption.text
                        caption.text = 'Figure {}: {}'.format(fig_ref_dict[figId], caption.text)
                except:
                    pass
    for div in xml.findall('.//div[@data-class]'):  # find all the divs with data-class
        if div.attrib['data-class'] == 'FigureTable':  # check that data-class does equal to FigureTable
            caption = div.find('.//div')
            if caption is not None:
                caption = div.find('.//div').find('.//p')  # extract just the caption bit
                try:
                    tableId = '#' + div.attrib['id'].replace('-', ':')  # temporary hack to get the id's correct, the # will always be needed but the replace can be removed when the validator updates are completed
                    div.set('id', tableId)  # attempting to put in a hack to fix the id problem
                    if tableId in table_ref_dict:
                        # caption.text = 'Table ' + table_ref_dict[tableId] + ': ' + caption.text
                        caption.text = 'Table {}: {}'.format(table_ref_dict[tableId], caption.text)
                except:
                    pass
    return xml


# now trying the chapter and section number function
def chapter_section_number(xml):
    '''This updates the appropriate h1 and h2 tags with a number. The number is determined from an appropriate dictionary. This uses the shortcodes to match the section and subsection headers but uses the chapter name to match the chapter numbers. The chapters might need some manual fixing while the sections and subsections should not.'''
    global section_counter
    for h1 in xml.findall('.//h1'):  # loop over the h1's
        newText = 'Chapter {}: {}'.format(file_number, h1.text)
        h1.text = newText
        # use the shortcode to tag the h2's with a number and the shortcode, repeat for h3's but only add the shortcode
    for section in xml.findall('.//section[@id]'):
        h2 = section.find('h2')
        h3 = section.find('h3')
        id_ = section.attrib['id']
        shortcode = etree.Element('span')
        shortcode.text = '({})'.format(id_[2:])
        shortcode.set('class', 'shortcode')
        try:
            if h2 is not None:
                h2.text = '{}.{} {} '.format(file_number, section_counter, h2.text)
                h2.append(shortcode)
                section_counter += 1
            if h3 is not None:
                h3.text = '{} '.format(h3.text)  # If the text matches the dictionary then add the number. Else ignore.
                h3.append(shortcode)
        except UnicodeEncodeError:
            continue
    return xml  # Return the updated xml


# next up: number the worked examples
def wex_number(xml):
    '''
    Number the worked examples using the wex dictionary. This will be fuzzy matching since it uses the titles and the titles sometimes contain strange characters or maths that cannot be matched.
    Wexes are defined as <div class="worked_example"><h1 class="title">Standard notation</h1>
    This modifies the wex code to be <div class="worked_example"><h1 class="title">Worked example 5: Standard notation</h1>
    '''
    #find the worked examples
    global wex_counter
    for section in xml.findall('.//section[@class]'):  # find all divs with attribute class
        if section.attrib['class'] == 'worked_example':  # only work on the section we actually want
            title = section.find('.//h2')
            problem_statement = section.find('.//div[@class]')
            if problem_statement != None and problem_statement.attrib['class'] == 'question':
                if title is not None:
                    try:
                        title.text = 'Worked example {}: {}'.format(wex_counter, title.text)  # add the number using the dictionary
                        wex_counter += 1
                    except UnicodeEncodeError:
                        pass
    return xml  # return the updated xml


# number the exerices
def exercise_number(xml):
    '''
    Number the exercises using ??.
    Still deciding where to put the number.
    Exercises currently are <section class="section"><h2 class="title" id="toc-id-11"> </h2>
    This part of the script gets complicated and I am not 100% sure why each bit works
    '''
    global exercise_counter
    for section in xml.findall('.//section[@class]'):
        #title = section.find('.//h2')
        ps = section.find('.//div[@class]')
        if ps != None and ps.attrib['class'] == 'problemset':
            #if title != None:
            span_code = etree.Element('span')
            span_code.set('class', 'exerciseTitle')
            span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)
            ps.insert(0, span_code)
            # to change where span is inserted find the index, see here: http://stackoverflow.com/questions/7474972/python-lxml-append-element-after-another-element
            exercise_counter += 1  # this should only affect the local instance of the counter
    return xml

# Put it all together
#path = '/home/heather/Desktop/books/physical-sciences-12/afrikaans/build/epubs/science12/OPS/xhtml/science12'
#path = '/home/heather/Desktop/books/mathematics-10/afrikaans/build/epubs/maths10/OPS/xhtml/maths10'
path = '/home/heather/Desktop/books/scripts/test-files/html5_test'
#path = '/home/heather/Desktop/books/grade-10-mathslit-latex/afrikaans/build/epubs/maths-lit10v2/OPS/xhtml/maths-lit10v2'

fileList = os.listdir(path)
fileList.sort()

# The next 3 lines likely can be improved somehow but I cannot find the way. If one file counter is set then the file counters intefere with each other and the numbers do not increment correctly.
file_counter_ex = 1  # set a file counter for exercises
file_counter_wex = 1  # set a file counter for worked examples
file_counter_section = 1  # set a file counter for sections
exercise_counter = 1
wex_counter = 1
section_counter = 1

for file_name in fileList:
    full_file_name = '{}/{}'.format(path, file_name)

    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
        continue

    xml = etree.parse(full_file_name, etree.HTMLParser())

    heading2 = xml.findall('.//h2')

    file_number = int(file_name[:2])

    # In order to modify counters correctly we also need to set some temporary counters going that can be used to modify the real counters. This likely can be improved as well.
    temp_exercise_counter = 0
    temp_wex_counter = 0
    temp_section_counter = 0
    for heading in heading2:
        if heading.text == 'Exercises':
            temp_exercise_counter += 1
        try:
            if heading.attrib['id'][:3] == 'toc' and heading.attrib['class'] == 'title':  # this is how we can uniquely identify sections
                temp_section_counter += 1
            if heading.attrib['class'] == 'title':  # this uniquely identifies worked examples
                temp_wex_counter += 1
        except KeyError:
            pass
    if temp_exercise_counter != 0:
        if file_counter_ex != file_number:
            file_counter_ex += 1
            exercise_counter = 1

    if temp_wex_counter != 0:
        if file_counter_wex != file_number:
            file_counter_wex += 1
            wex_counter = 1

    if temp_section_counter != 0:
        if file_counter_section != file_number:
            file_counter_section += 1
            section_counter = 1

    fileText = None

    #xml = fig_ref_fix(xml)
    #xml = fig_caption(xml)
    xml = chapter_section_number(xml)
    xml = wex_number(xml)
    xml = exercise_number(xml)

    fileText = etree.tostring(xml, pretty_print=True)

    # target_filename = '{}/heather.txt'.format(path)

    # This overwrites the contents of the file you are working with. Only do this if you are sure you can get the contents of the file back before the script was run.
    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)
