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
        title = div.find('.//h2')
        ps = div.find('.//div[@class]')
        if title != None and title.text == 'Exercises':  # now find just the exercises
            span_code = etree.Element('span')  # make a span
            span_code.set('class', 'exerciseTitle')  # set the class of the span
            span_code.text = 'Exercise {}.{}'.format(file_number, exercise_counter)  # add the counter as text along with the file number
            ps.insert(0, span_code)  # append the exercise counter after the initial problemset
            exercise_counter += 1  # if I have this correctly this only affects the local instance of the counter
    return xml

# Put it all together
path = '/home/heather/Desktop/books/physical-sciences-12/english/build/xhtml'
#path = '/home/heather/Desktop/books/mathematics-12/english/build/xhtml/'
#path = '/home/heather/Desktop/books/scripts/test-files/new_test'

fileList = os.listdir(path)
fileList.sort()

file_counter = 1  # set a file counter
exercise_counter = 0  # set an exercise counter

for file_name in fileList:
    full_file_name = '{}/{}'.format(path, file_name)

    # Skip directories
    if os.path.isdir(full_file_name):
        continue

    if file_name[0] not in ['0', '1', '2']:  # we need to ignore anything that does not start with a number
        continue

    file_number = int(file_name[:2])  # set a file number

    if file_counter == file_number:  # compare the file counter and the file number
        exercise_counter += 1  # if true then just increment the exercise counter
    else:  # if not then we must increment the file counter and reset the exercise counter
        file_counter += 1
        exercise_counter = 0
    
    fileText = None

    xml = etree.parse(full_file_name, etree.HTMLParser())
    xml = exercise_number(xml)

    fileText = etree.tostring(xml, pretty_print=True)

    # target_filename = '{}/heather.txt'.format(path)

    if fileText:
        with open(full_file_name, 'w') as file:
            file.write(fileText)