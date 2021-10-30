import random
import string
import sys
from unicodedata import category
from thefuzz import fuzz
from thefuzz import process
from Levenshtein import *

def file_process_fitzgerald(filename, skip_header):
    """
    Histogram contains all the words in the Great Gatsby.
    filename is a string.
    header: boolean, skips the header of the book
    """
    hist_fitzgerald = {}
    fp = open(filename, encoding = 'utf8')

    if skip_header:
        skip_book_header(fp)

    strippables = ''.join(
        [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
    )

    for line in fp:
        if line.startswith('*** END OF THE PROJECT GUTENBERG EBOOK'):
            break

        line = line.replace('-', ' ')
        line = line.replace(
            chr(8212), ' ' #8212 is for em dash
        )

        for word in line.split():
            #remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()

            #update histogram
            hist_fitzgerald[word] = hist_fitzgerald.get(word,0) + 1

    return hist_fitzgerald

def file_process_dickens(filename, skip_header):
    """
    Histogram contains all the words in the Great Gatsby.
    filename is a string.
    header: boolean, skips the header of the book
    """
    hist_dickens = {}
    fp = open(filename, encoding = 'utf8')

    if skip_header:
        skip_book_header(fp)

    strippables = ''.join(
        [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
    )

    for line in fp:
        if line.startswith('*** END OF THE PROJECT GUTENBERG EBOOK'):
            break

        line = line.replace('-', ' ')
        line = line.replace(
            chr(8212), ' ' #8212 is for em dash
        )

        for word in line.split():
            #remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()

            #update histogram
            hist_dickens[word] = hist_dickens.get(word,0) + 1

    return hist_dickens

def skip_book_header(fp):
    """
    Reads fp (open file object) until finds the line to stop
    """
    for line in fp:
        if line.startswith('*** START OF THE PROJECT GUTENBERG EBOOK'):
            break

def total_words_fitzgerald(hist_fitzgerald):
    """
    Return the total words in book (histogram)
    """
    return sum(hist_fitzgerald.values())

def total_words_dickens(hist_dickens):
    """
    Return the total words in book (histogram)
    """
    return sum(hist_dickens.values())

def different_words(hist_fitzgerald, hist_dickens):
    fuzz.ratio(hist_fitzgerald, hist_dickens) 
    fuzz.partial_ratio(hist_fitzgerald, hist_dickens)
    fuzz.token_sort_ratio(hist_fitzgerald, hist_dickens)
    return (f"{fuzz.ratio}{fuzz.partial_ratio}{fuzz.token_sort_ratio}")

def main():
    hist_fitzgerald = file_process_fitzgerald('Books/The Great Gatsby.txt', skip_header = True)
    hist_dickens = file_process_dickens('Books/A Tale of Two Cities.txt', skip_header = True)

    print(f"There are {total_words_fitzgerald(hist_fitzgerald)} words in 'The Great Gatsby' by F.Scott Fitzgerald.")
    print(f"There are {total_words_dickens(hist_dickens)} words in 'A Tale of Two Cities' by Charles Dickens.")
    print(f"These are the different ratios: {different_words(hist_fitzgerald, hist_dickens)}.")

if __name__ == '__main__':
    main()