from unittest import TestCase

import os

path = '/home/heather/Desktop/books/scripts/test-files/ideal_test'
file_list = os.listdir(path)
file_list.sort()

from number_html5 import number_html_class

class GeneralCounterTests(TestCase):
    def test_file_number_correct_range(self):
        assert type(file_number) == int
        assert type(file_counter) == int
        # the book with the most chapters in it has 23 chapters so file_number should not be higher
        assert file_number in range(0,25)
        # parts of chapters do not go above 15 currently
        assert file_counter in range(0,15)
    
    def test_section_wex_ex_counters(self):
        '''Test that the section, exercise, worked_example counters increment correctly 
        when the file counter increments and that the section, exercise and worked_example counters
        resets when the file counter is 0
        '''
        assert section_wex_ex_number(file_name) 
    
    def test_table_counter(self):
        '''Test that the table counter increments correctly when the file counter
        increments and that the table counter resets when the file counter is 0
        '''
        if file_counter == 0:
            assert table_counter == 1
        if file_counter != 0:
            #assert table_counter != 1  # this sometimes fails if no tables are found
            assert table_counter != 0
    
    def test_figure_counter(self):
        '''Test that the figure counter increments correctly when the file counter
        increments and that the figure counter resets when the file counter is 0
        '''
        if file_counter == 0:
            assert figure_counter == 1
        if file_counter != 0:
            #assert figure_counter != 1  # this sometimes fails if no figures are found
            assert figure_counter != 0
        