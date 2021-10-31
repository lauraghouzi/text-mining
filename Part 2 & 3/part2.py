import random
import sys
from unicodedata import category
from thefuzz import fuzz
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
    Histogram contains all the words in A Tale of Two Cities.
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
    Return the total words in Fitzgerald book (histogram)
    """
    return sum(hist_fitzgerald.values())

def total_words_dickens(hist_dickens):
    """
    Return the total words in Dickens book (histogram)
    """
    return sum(hist_dickens.values())


def most_common_d(hist_dickens, excluding_stopwords=True):
    """
    Makes a list of word-freq pairs(tuples) in descending order of frequency.
    hist: map from word to frequency
    excluding_stopwords: a boolean value. If it is True, do not include any stopwords in the list.
    returns: list of (frequency, word) pairs
    """
    d = []

    stopwords = file_process_dickens('Data/stopwords.txt', False)

    stopwords = list(stopwords.keys())
    # print(stopwords)

    for word, freq in hist_dickens.items():
        if excluding_stopwords:
            if word in stopwords:
                continue

        d.append((freq, word))

    d.sort(reverse=True)
    return d


def print_most_common_d(hist_dickens, num=10):
    """
    Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    d = most_common_d(hist_dickens)
    print('\nThe most common words in A Tale of Two Cities are:')
    for freq, word in d[:num]:
        print(word, '\t', freq)


def most_common_f(hist_fitzgerald, excluding_stopwords=True):
    """
    Makes a list of word-freq pairs(tuples) in descending order of frequency.
    hist: map from word to frequency
    excluding_stopwords: a boolean value. If it is True, do not include any stopwords in the list.
    returns: list of (frequency, word) pairs
    """
    f = []

    stopwords = file_process_fitzgerald('Data/stopwords.txt', False)

    stopwords = list(stopwords.keys())
    # print(stopwords)

    for word, freq in hist_fitzgerald.items():
        if excluding_stopwords:
            if word in stopwords:
                continue

        f.append((freq, word))

    f.sort(reverse=True)
    return f


def print_most_common_f(hist_fitzgerald, num=10):
    """
    Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    f = most_common_f(hist_fitzgerald)
    print('\nThe most common words in The Great Gatsby are:')
    for freq, word in f[:num]:
        print(word, '\t', freq)


def random_word_dickens(hist_dickens):
    """
    Chooses a random word from a histogram Dickens.
    The probability of each word is proportional to its frequency.
    """
    t = []
    for word, freq in hist_dickens.items():
        t.extend([word] * freq)

    return random.choice(t)


def random_word_fitzgerald(hist_fitzgerald):
    """
    Chooses a random word from a histogram Fitzgerald.
    The probability of each word is proportional to its frequency.
    """
    t = []
    for word, freq in hist_fitzgerald.items():
        t.extend([word] * freq)

    return random.choice(t)

def sentiment_dickens(hist_dickens):
    """
    Convert the dictionary into a string in order to check the emotion analysis.
    Calculate the Sentiment Intensity Analyzer
    """
    string_d = str(hist_dickens)
    score = SentimentIntensityAnalyzer().polarity_scores(string_d)
    return score
    

def sentiment_fitzgerald(hist_fitzgerald):
    """
    Convert the dictionary into a string in order to check the emotion analysis.
    Calculate the Sentiment Intensity Analyzer
    """
    string_f = str(hist_fitzgerald)
    score = SentimentIntensityAnalyzer().polarity_scores(string_f)
    return score


def ratio_difference(hist_fitzgerald, hist_dickens):
    """
    Difference between the texts in ratios, I used partial ratio to note consider the punctuations.
    """
    fuzz.partial_ratio(hist_fitzgerald, hist_dickens) 
    return ratio_difference(hist_fitzgerald, hist_dickens)


def ratio_precise(hist_fitzgerald, hist_dickens):
    """
    Difference between the texts in ratios, the most precised ratio to get the most accurate data.
    """
    fuzz.token_sort_ratio(hist_fitzgerald, hist_dickens)
    return ratio_precise(hist_fitzgerald, hist_dickens)
    

def main():
    hist_fitzgerald = file_process_fitzgerald('Books/The Great Gatsby.txt', skip_header = True)
    hist_dickens = file_process_dickens('Books/A Tale of Two Cities.txt', skip_header = True)

    print(f"There are {total_words_fitzgerald(hist_fitzgerald)} words in 'The Great Gatsby' by F.Scott Fitzgerald.")
    print(f"There are {total_words_dickens(hist_dickens)} words in 'A Tale of Two Cities' by Charles Dickens.")

    d = most_common_d(hist_dickens, False)
    print_most_common_d(hist_dickens, 20)

    f = most_common_f(hist_fitzgerald, False)
    print_most_common_f(hist_fitzgerald, 20)

    print("\n\nHere are some random words from 'The Great Gatsby':")
    for i in range(100):
        print(random_word_dickens(hist_fitzgerald), end=' ')
    
    print("\n\nHere are some random words from the 'A Tale of Two Cities':")
    for i in range(100):
        print(random_word_dickens(hist_dickens), end=' ')
    
    print(f"\n\nHere are the results for the sentiment intensity analysis for 'The Great Gatsby': \n{sentiment_dickens(hist_dickens)}")
    print(f"\nHere are the results for the sentiment intensity analysis for 'A Tale of Two Cities': \n{sentiment_fitzgerald(hist_fitzgerald)}")

    print(f"\nThere is a {ratio_difference(hist_fitzgerald, hist_dickens)} ratio difference in between the two books.")
    print(f"There is a {ratio_precise(hist_fitzgerald, hist_dickens)} ratio difference in between the two books, this is a more precise number.")




if __name__ == '__main__':
    main()