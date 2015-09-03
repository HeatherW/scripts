import os
from lxml import etree

def exercise_number(xml):
    '''
    Number the exercises using ??.
    Still deciding where to put the number.
    Exercises currently are <div class="section"><h2 class="title" id="toc-id-11">Exercises</h2>
    This part of the script gets complicated and I am not 100% sure why each bit works
    '''
    global exercise_counter  # danger!
    for div in xml.findall('.//div[@class]'):  # find all divs with classes
        title = div.find('.//h2')  # find the title
        ps = div.find('.//div[@class]')  # find the problemset
        if ps != None and ps.attrib['class'] == 'problemset':  # verify that we do have a problemset
            if title != None and title.text == 'Exercises':  # now find just the exercises
                span_code = etree.Element('span')  # make a span
                span_code.set('class', 'exerciseTitle')  # set the class of the span
                span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)  # add the counter as text along with the file number
                ps.insert(0, span_code)  # append the exercise counter after the initial problemset
                # to change where span is inserted find the index, see here: http://stackoverflow.com/questions/7474972/python-lxml-append-element-after-another-element
                exercise_counter += 1  # if I have this correctly this only affects the local instance of the counter
                span_end = etree.Element('span')  # trying to add the bit about practice
                span_end.set('class', 'practiceInfo')  # set the class of the span
                practice_link = etree.SubElement(span_end, 'a')  # make a link
                span_end.text = 'For more exercises, visit '  # change to science for the science one
                practice_link.set('href', 'http://www.everythingmaths.co.za')  # set the class of the link
                practice_link.text = 'www.everythingmaths.co.za'  # set the text of the link
                practice_link.tail = ' and click on "Practice Maths"'  # add a tail to the link
                ps.append(span_end)  # add it to the end of the problemset
    return xml

# Put it all together
#path = '/home/heather/Desktop/books/physical-sciences-12/english/build/xhtml'
#path = '/home/heather/Desktop/books/mathematics-12/english/build/xhtml/'
path = '/home/heather/Desktop/books/scripts/test-files/new_test'

fileList = os.listdir(path)
fileList.sort()

file_counter = 1  # set a file counter
exercise_counter = 1  # set an exercise counter

for file_name in fileList:
    full_file_name = '{}/{}'.format(path, file_name)

    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
        continue

    xml = etree.parse(full_file_name, etree.HTMLParser())

    title_exercise = xml.findall('.//h2')  # trying to find h2's in the file
    
    file_number = int(file_name[:2])  # set a file number

    random_number = 0  # only way I could think of to do this
    for i in title_exercise:  # find out if there is Exercises in the file
        if i.text == 'Exercises':
            random_number += 1
    if random_number != 0:  # we did find Exercises so now we can play with the counters
        if file_counter != file_number:  # if not then we must increment the file counter and reset the exercise counter
            file_counter += 1
            exercise_counter = 1
    
    fileText = None

    xml = exercise_number(xml)

    fileText = etree.tostring(xml, pretty_print=True)

    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)
