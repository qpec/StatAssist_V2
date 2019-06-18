from Config import *
from Utils import term_query_cleanerstemmer, txt_pages_cleanerstemmer, return_pdf_text_pp
import os
import pandas as pd

def get_term_query(excel_path, col=1, sublist_sep=','):
    '''function that selects column in input excel
    for associated search queries and formats it
    to the appropriate search format.
    output is a vector with the term locked to index
    in dataframe.'''
    df = pd.read_excel(excel_path)
    terms_unformatted = df[df.columns[col]].to_list()

    '''if multiple options, make sublist'''
    term_query = []
    for term in terms_unformatted:
        term = term.split(',')
        term_query.append(term)
    stemkey_query = term_query_cleanerstemmer(term_query)

    '''make the vector associated with query'''
    stemkey_index_vector = {}
    counter = 0
    for item in stemkey_query:
        for subitem in item:
            stemkey_index_vector[subitem] = counter
        counter += 1

    '''make the stem to original term vector'''
    stemkey_term_vector = {}
    for i in range(len(stemkey_query)):
        for i2 in range(len(stemkey_query[i])):
            stemkey_term_vector[stemkey_query[i][i2]] = term_query[i][i2]
        counter += 1
    return stemkey_index_vector, stemkey_term_vector

def get_clean_pages(pdf_path, stem=True):
    '''returns a list of string pages,
    cleaned and stemmed (if true)'''
    text_pp = return_pdf_text_pp(pdf_path)
    text_pp = txt_pages_cleanerstemmer(text_pp, stem)
    return text_pp

def get_term_matches_pp(stemkey_index_vector, text_pp):
    '''matches the terms to the pages
    returns a list of term matches per page.
    shallow duplicates are discarded
    (alternative representations of same
    concepts are retained)'''
    terms = [term for term in stemkey_index_vector]
    terms_pp = []
    for page in text_pp:
        this_page_terms = []
        for term in terms:
            if term in page:
                if term not in this_page_terms:
                    this_page_terms.append(term)
        terms_pp.append(this_page_terms)
    return terms_pp

def get_term_indexes_pp(terms_pp, stemkey_index_vector):
    term_indexes_pp = []
    for page in terms_pp:
        page_indexes = []
        for term in page:
            page_indexes.append(stemkey_index_vector[term])
        term_indexes_pp.append(page_indexes)
    return term_indexes_pp

def get_array_first_occurences(term_indexes_pp):
    occured_indexes = []
    array_fo = []
    for page in term_indexes_pp:
        page_occurences = []
        for index in page:
            if index in occured_indexes:
                page_occurences.append(0)
            else:
                occured_indexes.append(index)
                page_occurences.append(1)
        array_fo.append(page_occurences)
    return array_fo

def create_story_ref(pdf_path, excel_path):
    '''returns package in dictionary format'''
    stemkey_index_vector = get_term_query(excel_path)
    text_pp = get_clean_pages(pdf_path, stem=False)
    text_stemmed_pp = get_clean_pages(pdf_path)
    term_matches_pp = get_term_matches_pp(stemkey_index_vector, text_pp)
    term_indexes_pp = get_term_indexes_pp(term_matches_pp, stemkey_index_vector)
    array_first_occurences = get_array_first_occurences(term_indexes_pp)
    terms = [term for term in stemkey_index_vector]
    story_ref = {
    'terms_pp': term_matches_pp,
    'index_pp': term_indexes_pp,
    'first': array_first_occurences,
    'term_vector': stemkey_index_vector,
    'pages_stemmed': text_stemmed_pp,
    'pages': text_pp
    }
    return story_ref

create_story_ref(pdf_path, excel_path)
