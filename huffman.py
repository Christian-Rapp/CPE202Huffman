import time

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return comes_before(self, other)


def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq == b.freq:
        return a.char < b.char
    return a.freq < b.freq


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    if a.char < b.char:
        char = a.char
    else:
        char = b.char
    if comes_before(a, b):
        temp = HuffmanNode(char, a.freq + b.freq)
        temp.set_left(a)
        temp.set_right(b)
    else:
        temp = HuffmanNode(char, a.freq + b.freq)
        temp.set_left(b)
        temp.set_right(a)
    return temp


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""
    freq = [0]*256
    file = open(filename, "r")
    listString = ""
    for line in file:
        listString = listString + line
    listChars = list(listString)
    for ch in listChars:
        num = ord(ch)
        freq[num] += 1
    file.close()
    return freq


def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    huffmanList = []
    for i in range(len(char_freq)):
        if not (char_freq[i] == 0):
            temp = HuffmanNode(i, char_freq[i])
            huffmanList.append(temp)
    huffmanList.sort()
    while len(huffmanList) > 1:
        temp = combine(huffmanList[0], huffmanList[1])
        huffmanList = huffmanList[2:]
        huffmanList.append(temp)
        huffmanList.sort()
    if len(huffmanList) < 1:
        return
    return huffmanList[0]


def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""
    codeArray = [""]*256
    code = ""
    if node is not None:
        return _create_code(node, codeArray, code)
    return


def _create_code(node, codeArray, code):
    if (node.left and node.right) is None:
        codeArray[node.char] = code
    else:
        _create_code(node.right, codeArray, code + str(1))
        _create_code(node.left, codeArray, code + str(0))
    return codeArray


def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header = ""
    for a in range(len(freqs)):
        if not freqs[a] == 0:
            header = header + str(a) + " " + str(freqs[a]) + " "
    return header.rstrip()

def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""
    try:
        file = open(in_file, "r")
        file.close()

    except FileNotFoundError as error:
        raise FileNotFoundError

    else:
        frequency = cnt_freq(in_file)
        header = create_header(frequency)
        code = encoder_helper(frequency, in_file)
        fileOut = open(out_file, "w")
        fileOut.write(header)
        if not (code == ""):
            fileOut.write("\n"+code)
        fileOut.close()


def encoder_helper(frequency, file):

    file = open(file, "r")
    node = create_huff_tree(frequency)
    code = create_code(node)
    encoded = ""
    listString = ""
    for line in file:
        listString = listString + line
    file.close()
    temp = list(listString)
    for a in temp:
        encoded = encoded + code[ord(a)]
    return encoded


def huffman_decode(encoded_file, decode_file):
    """ reads an encoded text file, encoded_file, and writes the decoded text into an output text file, decode_file, using
    the Huffman Tree produced by using the header information. """
    try:  # Makes sure that the input file exists if not raises error
        encoded = open(encoded_file, "r")
    except FileNotFoundError as error:
        raise error

    decString = ""
    decode = open(decode_file, "w")
    header = encoded.readline()  # Gets the first line of the file as a string
    if len(header) > 0:
        freq = parse_header(header)  # Creates a frequency list from the header information
        tree = create_huff_tree(freq)  # Creates a huffman tree from the frequency list
        root = tree
        encodedSeq = list(encoded.readline())  # Gets the encoded text
        encoded.close()
        decString = ""
        currNode = tree  # Sets the current node to the root
        if len(encodedSeq) == 0:
            for char in range(len(freq)):
                if not freq[char] == 0:
                    decString += chr(char)*freq[char]
        else:
            for i in range(len(encodedSeq)):  # Iterate through each 0 or 1 in the encoded text

                if encodedSeq[i] == "0":  # If 0 go left
                        currNode = currNode.left
                        if currNode.left is None and currNode.right is None:
                            decString += chr(currNode.char)
                            currNode = root  # Makes sure after each character iterate through tree from top

                else:  # If 1 go right
                        currNode = currNode.right
                        if currNode.left is None and currNode.right is None:
                            decString += chr(currNode.char)
                            currNode = root  # Makes sure after each character iterate through tree from top

    decode.write(decString)
    decode.close()
    encoded.close()


def parse_header(header_string):
    """ takes a string input parameter (the first line of the input file) and returns a list of frequencies."""
    freq = [0]*256  # Creates empty frequency list
    header = header_string.split(" ")  # Splits string into array so no white space only numbers
    for i in range(0, len(header), +2):  # iterates by two to get the index and the frequency for numbers
        index = header[i]
        count = header[i+1]
        freq[int(index)] = int(count)

    return freq

# starttime1 = time.time()
# huffman_encode("WarAndPeace.txt", "WarAndPeace_soln.txt")
# stoptime1 = time.time()
#
# starttime2 = time.time()
# huffman_decode("WarAndPeace_soln.txt", "Test.txt")
# stoptime2 = time.time()
#
# print("It took ",stoptime1 - starttime1, "to encode War and Peace")
# print("It took ",stoptime2 - starttime2, "to decode War and Peace")