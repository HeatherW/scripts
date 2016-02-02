from unittest import TestCase

import number_html5

class SectionNumberTests(TestCase):
    def test_section_counter(self):
        '''Test that the section counter increments correctly when the file counter
        remains the same and that the section counter resets when the file counter changes
        '''
