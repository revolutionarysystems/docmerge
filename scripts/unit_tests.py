import unittest
import os
from merge.config import local_root

from merge.resource_utils import (
    get_working_dir, strip_xml_dec,get_local_dir, get_output_dir, get_local_txt_content,
    push_local_txt, del_local)
#from merge.merge_utils import 

class LocalResourceTestCase(unittest.TestCase):

    def test_working_dir(self):
        cwd = get_working_dir()
        self.assertTrue(cwd[-8:]=="docmerge")

    def test_local_dir(self):
        local = get_local_dir("templates")
        expected = os.path.sep.join(["docmerge",local_root,"templates"])
        self.assertEqual(local[-len(expected):],expected)

    def test_output_dir(self):
        output = get_output_dir()
        expected = os.path.sep.join(["docmerge",local_root,"output"])
        self.assertEqual(output[-len(expected):],expected)

    def test_strip_xml_dec(self):
        xml = "<?xml header stuff><proper><content>here</content></proper>"
        stripped_xml = strip_xml_dec(xml)
        self.assertTrue(stripped_xml == "<proper><content>here</content></proper>")

    def test_get_local_txt_content(self):
        cwd = get_working_dir()
        txt = get_local_txt_content(cwd, "test", "test.txt")
        self.assertEqual(txt, "Sample test text.")

    def test_push_local_txt(self):
        cwd = get_working_dir()
        newtext = "created text"
        push_local_txt(cwd, "test", "push.txt", newtext)
        text = get_local_txt_content(cwd, "test", "push.txt")
        self.assertEqual(text, newtext)
        del_local(cwd, "test", "push.txt")

    def test_del_local_txt(self):
        cwd = get_working_dir()
        newtext = "created text"
        push_local_txt(cwd, "test", "del.txt", newtext)
        del_local(cwd, "test", "del.txt")
        text = get_local_txt_content(cwd, "test", "del.txt")
        self.assertEqual(text, None)



def run():
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(LocalResourceTestCase)
        unittest.TextTestRunner(verbosity=2).run(suite)
    except Exception as ex:
        print(ex)

