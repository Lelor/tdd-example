from time import sleep
from selenium import webdriver
import unittest
from os import remove

from selenium.webdriver.common.keys import Keys


class NewVisitor(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.table_id = 'id_list_table'
        self.input_id = 'id_new_item'

    @property
    def list_table(self):
        return self.browser.find_element_by_id(self.table_id)

    @property
    def input_field(self):
        return self.browser.find_element_by_id(self.input_id)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        rows = self.list_table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def insert_new_item(self, task):
        self.input_field.send_keys(task)
        self.input_field.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # the page title must remet something of a To-Do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        self.assertEqual(self.input_field.get_attribute('placeholder'), 'Enter a to-do item')

        self.insert_new_item('Buy peacock feathers')
        sleep(1)        
        self.insert_new_item('Use peacock feathers to make a fly')
        sleep(5)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        sleep(1)
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
