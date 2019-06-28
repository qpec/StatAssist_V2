from Config import *
from Utils import cleaner, get_pdf_text_pp
import os
import pandas as pd
import regex as re

def get_clean_txt_pdf_pp(pdf_path):
    text_pp = get_pdf_text_pp(pdf_path)
    clean_text_pp = [cleaner(text) for text in text_pp]
    return clean_text_pp

def get_search_terms(excel_path, col=0, sublist_sep=','):
    '''function that selects column in input excel
    for associated search queries and formats it
    to the appropriate search format.
    output is a vector with the term locked to index
    in dictionary.'''
    df = pd.read_excel(excel_path)
    terms_unformatted = df[df.columns[col]].to_list()

    '''if multiple options, make sublist'''
    term_query = []
    for terms in terms_unformatted:
        terms = terms.split(sublist_sep)
        term_query.append(terms)

    '''make the vector associated with query'''
    term_index_vector = {}
    counter = 0
    for terms in term_query:
        for term in terms:
            term_index_vector[str(term)] = counter
        counter += 1
    return term_index_vector

def get_term_matches_pp(term_index_vector, text_pp):
    '''matches the terms to the pages
    returns a list of term matches per page.
    shallow duplicates are discarded
    (alternative representations of same
    concepts are retained)'''
    terms = [term for term in term_index_vector]
    terms_pp = []
    for page in text_pp:
        this_page_terms = []
        for term in terms
            if term in page:
                if term not in this_page_terms:
                    this_page_terms.append(term)
        terms_pp.append(this_page_terms)
    return terms_pp

def get_term_indexes_pp(terms_pp, term_index_vector):
    term_indexes_pp = []
    for page in terms_pp:
        page_indexes = []
        for term in page:
            page_indexes.append(term_index_vector[term])
        term_indexes_pp.append(page_indexes)
    return term_indexes_pp

def get_array_first_occurences(term_indexes_pp):
    '''A feature of StatAssist is to only display
    the fist occurence of a term in the sidebar
    with a explanation, here this is evaluated'''
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
    term_index_vector = get_search_terms(excel_path)
    text_pp = get_clean_txt_pdf_pp(pdf_path)
    term_pp = get_term_matches_pp(term_index_vector, text_pp)
    term_indexes_pp = get_term_indexes_pp(term_pp, term_index_vector)
    array_first_occurences = get_array_first_occurences(term_indexes_pp)

    terms = [term for term in term_index_vector]
    story_ref = {
    'terms_pp': term_pp,
    'index_pp': term_indexes_pp,
    'first': array_first_occurences,
    'stem_vector': term_index_vector,
    }
    return story_ref

create_story_ref(pdf_path, excel_path)
