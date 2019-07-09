'''This is a seperate module which 1. takes input pivot words 2.
takes corpus texts 3. makes bi, tri and tetragrams from corpus
items and builds vector (without counts) 4. based on pivot words
returns all grams with the pivot words included. Thereby presenting
all respective contexts the pivot word occurs in'''

import pandas as pd


# import specific bigram/trigram dataset


# import input selection pivot words
def text_reader():
    pass


def text_to_list():
    pass


# match pivot words to specific dataset
def pivot_to_dataset_matcher(pivot_words, dataset_with_grams):
    pivot_matched = [[] for i in pivot_words]
    for i in range(len(pivot_words)):
        pivot_word = pivot_words[i]
        for gram in dataset_with_grams:
            gram_split = gram.split()
            if pivot_word in gram_split:
                pivot_matched[i].append(gram)
    return pivot_matched


# export matched bigram/trigram into dataframe to excel
def pivot_matched_datasheet_exporter(pivot_words, pivot_matched, export_name="pivot_matches.xlsx"):
    dictionary = {
        "pivot_word": pivot_words,
        "pivot_matched": pivot_matched
        }
    df = pd.DataFrame(dictionary)
    df.to_excel(export_name)
