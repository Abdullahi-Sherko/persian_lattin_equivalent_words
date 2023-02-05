import re
import string
from difflib import SequenceMatcher
from os.path import exists
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googlesearch import search


def words_similarity_rate(word1, word2):
    return round(SequenceMatcher(None, word1, word2).ratio(), 2)


def convert_to_persian(lattin_word):
    dual_letters = {'sh': 'ش', 'zh': 'ژ', 'gh': 'ق', 'kh': 'خ', 'ch': 'چ'}
    if exists('persian_alphabet.xlsx'):
        persian_alphabet = pd.read_excel('persian_alphabet.xlsx')
    else:
        exit('persian alphabet file is not exist')
    alphabet = dict(zip(persian_alphabet['english'], persian_alphabet['letter']))
    lowcase_lattin_word = lattin_word.lower()
    to_replace = {}
    two_substrings = [''.join(t) for t in zip(lowcase_lattin_word, lowcase_lattin_word[1:])]
    for letter in two_substrings:
        if letter in dual_letters:
            to_replace[lowcase_lattin_word.index(letter)] = dual_letters[letter]
            lowcase_lattin_word = lowcase_lattin_word.replace(letter, dual_letters[letter])
    persian_word = list(alphabet[letter] for letter in lowcase_lattin_word if letter in alphabet.keys())
    for i in to_replace.keys():
        persian_word.insert(i, to_replace[i])
    persian_word = ''.join(char for char in persian_word)
    combined_word = persian_word + ' ' + lattin_word
    return persian_word, lattin_word, combined_word



def cleanse_words(word):
    string.punctuation += '،'
    puncs = r'[' + string.punctuation + ']'
    clean_word = re.sub(puncs, '', word).strip()
    return clean_word


def equivalent_words(search_keywords):
    equi_words = list()
    websites_text = list()
    for word in search_keywords:
        google_search = search(word, num_results=1)
        for url in google_search:
            try:
                resp = requests.get(url)
                context = resp.text
                if resp.status_code == 200:
                    print(url)
                    soup = BeautifulSoup(context, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.extract()
                    text = soup.get_text()
                    websites_text.append(text)
            except Exception as e:
                continue
    if len(search_keywords[0].split()) == 1:
        for i in range(len(websites_text)):
            for word in websites_text[i].split():
                if words_similarity_rate(search_keywords[0], word) > 0.7:
                    word = cleanse_words(word)
                    if word not in equi_words:
                        equi_words.append(cleanse_words(word))


    else:
        for i in range(len(websites_text)):
            website_text = websites_text[i]
            all_words = find_word(website_text, len(search_keywords[0]))
            for word in all_words:
                if words_similarity_rate(search_keywords[0], word) > 0.75:
                    equi_words.append(cleanse_words(word))
    return list(dict.fromkeys(equi_words))[0:3]


def find_word(text, word_length):
    all_words = []
    for i in range(0, len(text) - word_length + 1):
        all_words.append(text[i:i+word_length])
    return all_words


def word_different_forms(word):
    different_forms = []
    s_lett = ['ص', 'ث']
    t_lett = ['ط']
    z_lett = ['ذ', 'ظ', 'ض']
    a_lett = ['ن']
    if 'س' in word:
        for lett in s_lett:
            different_forms.append(word.replace('س', lett))

    if 'ت' in word:
        for lett in t_lett:
            different_forms.append(word.replace('ت', lett))

    if 'ز' in word:
        for lett in z_lett:
            different_forms.append(word.replace('ز', lett))
    different_forms.append(word)
    return different_forms

