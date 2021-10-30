import urllib.request

dickens_url = 'https://www.gutenberg.org/files/98/98-0.txt'
response = urllib.request.urlopen(dickens_url)
data = response.read()  # a `bytes` object
text = data.decode('utf-8')
print(text) # for testing

fitzgerald_url = 'https://www.gutenberg.org/files/64317/64317-0.txt'
response = urllib.request.urlopen(fitzgerald_url)
data = response.read()  # a `bytes` object
text = data.decode('utf-8')
print(text) # for testing