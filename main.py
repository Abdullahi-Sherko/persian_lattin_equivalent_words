from utils import *
persian_equi_words = {}
print('be pacient! it takes a while ...')
lattin_words = ['Softlan', 'khosh govar', 'Golrang']
for word in lattin_words:
    search_keyword = convert_to_persian(word)
    equi_word = equivalent_words(search_keyword)
    if word not in persian_equi_words:
        persian_equi_words[word] = equi_word

print(persian_equi_words)


