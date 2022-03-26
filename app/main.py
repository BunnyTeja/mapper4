
# -----
#    From: https://github.com/karan109/Text-Visualization/blob/3c1ab67e7ee282500d44934fe7d8bfe9c4fe1ac7/vis/Helpers/helpers2.py
# -----

import pickle
# Spacy
#import spacy
# Calculate Levenshtein distance
import nltk
nltk.download('punkt')
from nltk import word_tokenize
from nltk.util import ngrams
import re

#import pip
#pip.main(['install','fuzzywuzzy'])
#import fuzzywuzzy
from fuzzywuzzy import fuzz

# Generate a trie from a map from words to codes
def get_trie(m1):
    trie = {}
    for word in list(m1.keys()):
        if word == '':
            continue
        temp = trie
        for letter in word:
            if letter not in temp.keys():
                temp[letter] = {}
            temp = temp[letter]
        temp['__end__'] = m1[word]
    return trie


# Return the closest string to the word in the trie
def find_(trie, word):
    c = ''
    temp = trie
    for letter in word:
        if letter not in temp.keys():
            dist, word = get_nearest(temp)
            return (dist, c + word)
        else:
            c += letter
            temp = temp[letter]
    if '__end__' not in temp.keys():
        dist, word = get_nearest(temp)
        return (dist, c + word)
    else:
        return (0, c)


# Helper function for find_
def get_nearest(trie):
    ans = 1000000
    word = ''
    if '__end__' in trie.keys():
        return (0, '')
    for key in list(trie.keys()):
        temp = get_nearest(trie[key])
        if ans > temp[0]:
            ans = temp[0]
            word = key + temp[1]
    return (ans + 1, word)


# Return Classification Codes, given a piece of text
# - Assumptions made:
#    * Max N-grams: 7 (ngram_depth))
#    * Similarity threshold: 85 (sim_threshold)
#    * No assumption on terms to be skipped
def get_codes_class(text, term_to_code, code_to_term, triee, ngram_depth = 7, sim_threshold = 85, to_print=0):
    
        # A map from a term to its count
        ans = {}

        # Tokenize text into words
        tokens = [str(word).lower() for word in word_tokenize(text) if str(word).isalpha()]

        # A map to check whether a word has already been included in the Classification
        done = {}

        # Generate N-Grams from ngram_depth to 1
        for i in range(ngram_depth, 0, -1):
            text_temp_ = list(ngrams(tokens, i))
            for j, el in enumerate(text_temp_):
                term = ' '.join(el)
                dist, nearest = find_(triee, term)
                similarity = fuzz.ratio(nearest.strip(), term.strip())

                # Consider terms if similarity > sim_threshold in the trie
                if similarity >= int(sim_threshold):
                    temp = term
                    term = nearest
                    if term != '':
                    #if term != 'general' and term != '' and term != 'miscellaneous':
                        check = False
                        for k in range(len(el)):
                            if done.get(j + k, -1) == -1:
                                check = True
                                break
                        if check:
                            for k in range(len(el)):
                                done[j + k] = 1
                            if to_print == 1:
                                 print(temp, ',', nearest, ',', similarity, ',', j, ',', term_to_code[term])
                                 return(term_to_code[term],similarity)
                            ans[term] = ans.get(term, 0) + 1
    

    #     # Rest of the code decides what to do in case a term belongs to 2 codes
    #     final = {}
    #     codes = {}
    #     for key in list(ans.keys()):
    #         if len(term_to_code[key]) == 1:
    #             final[(key, list(term_to_code[key])[0])] = ans[key]
    #             s = list(term_to_code[key])[0]
    #             codes[s] = codes.get(s, 0) + 1
    #             if s.count('.') >= 1:
    #                 t = s[:s.find('.')]
    #                 codes[t] = codes.get(t, 0) + 1
    #             if s.count('.') >= 2:
    #                 x = [m.start() for m in re.finditer('\.', s)]
    #                 t = s[:x[-1]]
    #                 codes[t] = codes.get(t, 0) + 1
    #     for key in list(ans.keys()):
    #         if len(term_to_code[key]) == 1:
    #             continue
    #         lengths = []
    #         for el in term_to_code[key]:
    #             lengths.append(codes.get(el, 0))
    #         lengths.sort()
    #         if lengths[-1] != lengths[-2]:
    #             for el in term_to_code[key]:
    #                 if codes.get(el, 0) == lengths[-1]:
    #                     final[(key, el)] = ans[key]
    #                     break
    #         else:
    #             keys = []
    #             for el in term_to_code[key]:
    #                 if el.count('.') >= 1:
    #                     x = [m.start() for m in re.finditer('\.', el)]
    #                     keys.append(el[:x[-1]])
    #                 else:
    #                     keys.append(el)
    #             lengths = []
    #             for el in keys:
    #                 lengths.append(codes.get(el, 0))
    #             lengths.sort()
    #             if lengths[-1] != lengths[-2]:
    #                 for i, el in enumerate(keys):
    #                     if codes.get(el, 0) == lengths[-1]:
    #                         final[(key, list(term_to_code[key])[i])] = ans[key]
    #                         break
    #             else:
    #                 temp = []
    #                 for el in keys:
    #                     if el.count('.') >= 1:
    #                         x = [m.start() for m in re.finditer('\.', el)]
    #                         temp.append(el[:x[-1]])
    #                     else:
    #                         temp.append(el)
    #                 keys = temp
    #                 lengths = []
    #                 for el in keys:
    #                     lengths.append(codes.get(el, 0))
    #                 lengths.sort()
    #                 if lengths[-1] != lengths[-2]:
    #                     for i, el in enumerate(keys):
    #                         if codes.get(el, 0) == lengths[-1]:
    #                             final[(key, list(term_to_code[key])[i])] = ans[key]
    #                             break
    #                 else:
    #                     final[(key, list(term_to_code[key])[-1])] = ans[key]
    #     codes = {}
    #     title = {}
    #     for key in list(final.keys()):
    #         title[key[1][0]] = title.get(key[1][0], 0) + 1
    #     letter = max(title, key=lambda x: title[x])
    #     title = code_to_term[letter]
    #     final_codes = sorted(list(final.keys()), key=lambda x: final[x], reverse=True)[:10]
    #     areas = {}
    #     codes = {}
    #     for i, code in enumerate(final_codes):
    #         codes[code[1]] = final[code]
    #         areas[code_to_term[code[1]]] = codes[code[1]]

    #     # Letter is the Code for the Letter with most codes (A-K)
    #     # codes is a map from Classification Code to Frequency (Top 10 codes)
    #     return (letter, codes)
    # except:
    #     return ("", {})


# Initialize data structures
def initialize():

    # print(text)
    # A map from ACM Classification Codes to their corresponding meaning
    code_to_term = pickle.load(open('data/code_to_term.pickle', 'rb'))

    # A map from ACM Classification Terms to their corresponding codes
    term_to_code = pickle.load(open('data/term_to_code.pickle', 'rb'))

    # Convert the map term_to_code to a trie
    trie = get_trie(term_to_code)

    return term_to_code, code_to_term, trie


# - main processing

term_to_code, code_to_term, trie = initialize()
#print (term_to_code)

# text_list = ['general architecture', 'quality assurance', 'artificial intelligence', 'miscellaneous', 'systems', 'insurance',
#              'learn', 'mach. learning', 'data mining' ]
# for text in text_list:
#     print ("--", text)
code = get_codes_class("insure", term_to_code, code_to_term, trie, 7, 65, 1)
print (code)


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return(render_template("mapper.html"))

@app.route('/',methods=["POST"])
def getValue():
    it=request.form["inputtext"]
    th=request.form["threshold"]
    print(it)
    print(th)
    code = get_codes_class(it, term_to_code, code_to_term, trie, 7, th, 1)
    print(code)
    return(render_template("pass.html",inputtext=code[0], threshold=code[1]))





#print (code_to_term)