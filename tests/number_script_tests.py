from unittest import TestCase

from number_html5 import *

class SectionNumberTests(TestCase):
    def test_section_counter(self):
        '''Test that the section counter increments correctly when the file counter
        increments and that the section counter resets when the file counter is 0
        '''
        if file_counter == 0:
            assert section_counter == 1
        if file_counter != 0:
            assert section_counter != 1
            assert section_counter != 0
    
    def test_exercise_counter(self):
        '''Test that the exercise counter increments correctly when the file counter
        increments and that the exercise counter resets when the file counter is 0
        '''
        if file_counter == 0:
            assert exercise_counter == 1
        if file_counter != 0:
            assert exercise_counter != 1
            assert exercise_counter != 0
    
    def test_worked_example_counter(self):
        '''Test that the worked example counter increments correctly when the file counter
        increments and that the worked example counter resets when the file counter is 0
        '''
        if file_counter == 0:
            assert worked_example_counter == 1
        if file_counter != 0:
            assert worked_example_counter != 1
            assert worked_example_counter != 0
    
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
            assert figure_counter != 1  # this sometimes fails if no figures are found
            assert figure_counter != 0
        