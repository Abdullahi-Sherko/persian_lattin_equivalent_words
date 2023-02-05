from utils import *
persian_equi_words = {}
lattin_words = input('Enter lattin words separated by space\n-> ')
lattin_words = lattin_words.split()
print('be pacient! it takes a while ...')
for i in range(len(lattin_words)):
    word = lattin_words[i]
    search_keyword = convert_to_persian(word)
    equi_word = equivalent_words(search_keyword)
    if word not in persian_equi_words:
        persian_equi_words[word] = equi_word
    print('{}/{} is done!'.format((i+1), len(lattin_words)))
print(persian_equi_words)
#

