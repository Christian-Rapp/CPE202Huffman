import unittest
import filecmp
import subprocess
from huffman import *

class TestList(unittest.TestCase):

    def test_comes_before(self):
        one = HuffmanNode(97, 1)
        two = HuffmanNode(96, 1)
        self.assertTrue(comes_before(two, one))
        self.assertFalse(comes_before(one,two))
        three = HuffmanNode(95, 2)
        self.assertTrue(comes_before(one, three))
        self.assertFalse(comes_before(three, one))
        four = HuffmanNode(98, 10)
        self.assertTrue(comes_before(one, four))
        self.assertTrue(comes_before(two, four))
        self.assertTrue(comes_before(three, four))
        self.assertFalse(comes_before(four, three))
        self.assertFalse(comes_before(four, two))
        self.assertFalse(comes_before(four, one))

    def test_combine(self):
        one = HuffmanNode(1, 5)
        two = HuffmanNode(2, 10)
        self.assertEqual(combine(one,two).freq, 15)
        self.assertEqual(combine(one, two).char, 1)
        three = HuffmanNode(0, 15)
        self.assertEqual(combine(one, three).freq, 20)
        self.assertEqual(combine(one, three).char, 0)
        self.assertEqual(combine(combine(one, two), three).freq, 30)
        self.assertEqual(combine(combine(one, two), three).char, 0)
        self.assertNotEqual(combine(one, two).char, 2)
        self.assertNotEqual(combine(combine(one, two), three).char, 1)

    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)
        freqlist2 = cnt_freq("multiline2.txt")
        anslist2a = 2
        anslist2b = [0, 1, 1, 1, 0]
        self.assertEqual(freqlist2[10], anslist2a)
        self.assertEqual(freqlist2[96:101], anslist2b)
        self.assertTrue(1 in freqlist2)
        self.assertFalse(3 in freqlist2)
        self.assertNotEqual(freqlist2[90:95], anslist2b)
        self.assertEqual(freqlist[0:96], [0]*96)
        self.assertEqual(freqlist[103:], [0]*153)
        self.assertNotEqual(freqlist2, [0]*256)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        self.assertTrue(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)
        freqlist2 = cnt_freq("file1.txt")
        hufftree2 = create_huff_tree(freqlist2)
        self.assertNotEqual(hufftree2.freq, hufftree.freq)
        self.assertNotEqual(hufftree2.left.freq, hufftree.left.freq)

    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        freqList2 = cnt_freq("multiline2.txt")
        self.assertEqual(create_header(freqList2), "10 2 97 1 98 1 99 1")
        self.assertTrue(create_header(freqList2)[0:1], "10")
        self.assertNotEqual(create_header(freqlist), create_header(freqList2))
        self.assertNotEqual(create_header(freqList2), "")

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertTrue(codes[ord('f')], '0001')
        freqlist2 = cnt_freq("file1.txt")
        hufftree2 = create_huff_tree(freqlist2)
        codes2 = create_code(hufftree2)
        self.assertNotEqual(codes, codes2)

    def test_error(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("file.txt", "test.txt")


    """UNIX TESTS"""
    def test_unix1_textfile(self):
        huffman_encode("file1.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file2_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix2_testfile(self):
        huffman_encode("declaration.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt declaration_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt multiline_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix3_testfile(self):
        huffman_encode("a.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt a_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt b_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix4_testfile(self):
        huffman_encode("b.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt b_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt a_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix5_testfile(self):
        huffman_encode("file2.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt file2_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file1_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix6_testfile(self):
        huffman_encode("multiline.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt multiline_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file2_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix7_testfile(self):
        a = open("multiline3.txt", "a")
        a.write("\n")
        a.close()
        huffman_encode("multiline3.txt", "Test.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb Test.txt multiline_soln.txt", shell=True)
        self.assertNotEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file2_soln.txt", shell=True)
        self.assertNotEqual(err1, 0)

    # """WINDOWS TESTS"""
    # def test_01_textfile(self):
    #     huffman_encode("file1.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("file1_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("file2_soln.txt", "Test.txt"))
    #
    # def test_02_textfile(self):
    #     huffman_encode("declaration.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("declaration_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("declaration_soln.txt", "multiline_soln.txt"))
    #
    # def test_03_textfile(self):
    #     huffman_encode("a.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("a_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("a_soln.txt", "file1_soln.txt"))
    #
    # def test_04_textfile(self):
    #     huffman_encode("b.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("b_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("Test.txt", "a_soln.txt"))
    #
    # def test_05_textfile(self):
    #     huffman_encode("file2.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("file2_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("file1_soln.txt", "Test.txt"))
    #
    # def test_06_textfile(self):
    #     huffman_encode("multiline.txt", "Test.txt")
    #     self.assertTrue(filecmp.cmp("multiline_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("b_soln.txt", "Test.txt"))
    #
    # def test_07_textfile(self):
    #     a = open("multiline3.txt", "a")
    #     a.write("\n")
    #     a.close()
    #     huffman_encode("multiline3.txt", "Test.txt")
    #     self.assertFalse(filecmp.cmp("multiline_soln.txt", "Test.txt"))
    #     self.assertFalse(filecmp.cmp("b_soln.txt", "Test.txt"))


    def test_parseheader(self):
        fileIn = open("file1_soln.txt", "r")
        firstLine = fileIn.readline()
        freqOut = cnt_freq("file1.txt")
        self.assertEqual(parse_header(firstLine), freqOut)
        self.assertNotEqual(parse_header(firstLine), cnt_freq("file2.txt"))
        fileIn.close()
        fileIn = open("declaration_soln.txt", "r")
        firstLine = fileIn.readline()
        freqOut = cnt_freq("declaration.txt")
        self.assertEqual(parse_header(firstLine), freqOut)
        self.assertNotEqual(parse_header(firstLine), cnt_freq("multiline.txt"))
        fileIn.close()

    def test_unix_1huffman_decode(self):
        huffman_decode("file1_soln.txt", "Test.txt")
        err = subprocess.call("diff -wb Test.txt file1.txt", shell = True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file2.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix_2huffman_decode(self):
        huffman_decode("file2_soln.txt", "Test.txt")
        err = subprocess.call("diff -wb Test.txt file2.txt", shell = True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file1.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix_3huffman_decode(self):
        huffman_decode("declaration_soln.txt", "Test.txt")
        err = subprocess.call("diff -wb Test.txt declaration.txt", shell = True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt file2.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_unix_4huffman_decode(self):
        huffman_decode("b_soln.txt", "Test.txt")
        err = subprocess.call("diff -wb Test.txt b.txt", shell=True)
        self.assertEqual(err, 0)
        err1 = subprocess.call("diff -wb Test.txt a.txt", shell=True)
        self.assertNotEqual(err1, 0)

    def test_errors(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode("basafdfsadf.txt", "Test.txt")

    def test_empty_file(self):
        huffman_decode("a.txt", "Test.txt")
        err = subprocess.call("diff -wb Test.txt a.txt", shell=True)
        self.assertEqual(err, 0)

if __name__ == '__main__': 
   unittest.main()
