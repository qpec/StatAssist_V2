"""receives words of the pdf with coordinates and an excel sheet with
search_queries in the first column. The matched words or collocations
will be returned in a dictionary"""

from src.parser import analysis
from nltk import SnowballStemmer
import pandas as pd
import regex as re


def get_search_terms(excel_path, col=1, sublist_sep=","):
    """function that selects column in input excel
    for associated search queries and formats it
    to the appropriate search format.
    output is a vector with the term locked to index
    in dictionary."""
    df = pd.read_excel(excel_path)
    terms_unformatted = df[df.columns[col]].to_list()

    """if multiple options, make sublist"""
    term_query = []
    for terms in terms_unformatted:
        terms = terms.split(sublist_sep)
        term_query.append(terms)

    """make the vector associated with query"""
    search_term_index_vector = {}
    counter = 0
    for terms in term_query:
        for term in terms:
            search_term_index_vector[str(term)] = counter
        counter += 1
    return search_term_index_vector


def subfinder(mylist, pattern):
    """returns sublists if in list.
    specifically the x1 and x2 coordinates
    the sublist resides in the superlist"""
    matches = []
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i : i + len(pattern)] == pattern:
            matches.append([i, i + len(pattern) - 1])
    return matches


def remove_duplicates_list(lst):
    clean_list = []
    for item in lst:
        if item not in clean_list:
            clean_list.append(item)
    return clean_list


def get_term_matches_pp(search_term_index_vector, article_dict):
    """matches the search_terms to the input text
    returns a list of term index matches."""
    stemmer = SnowballStemmer("english")
    search_terms = [stemmer.stem(term.lower()) for term in search_term_index_vector]
    article_words = [stemmer.stem(word.lower()) for word in article_dict["words"]]
    wordindex_to_page = article_dict["pages"]
    page_matches = []
    term_article_index_matches = []
    term_searchindex_article_matches = []
    for i in range(len(search_terms)):
        term = search_terms[i].split()
        group_matches = subfinder(article_words, term)
        if group_matches:
            for match in group_matches:
                this_match_indexes = []
                this_match_pages = []
                for index in match:
                    this_match_indexes.append(index)
                    this_match_pages.append(wordindex_to_page[index])
                this_match_indexes = remove_duplicates_list(this_match_indexes)
                term_article_index_matches.append(this_match_indexes)
                page_matches.append(this_match_pages)
                term_searchindex_article_matches.append(i)

    tuple_lists = list(zip(term_article_index_matches, term_searchindex_article_matches, page_matches))
    tuple_lists2 = sorted(tuple_lists, key=lambda x: x[0])
    list_lists = [list(t) for t in zip(*tuple_lists2)]

    term_article_index_matches = list_lists[0]
    term_searchindex_article_matches = list_lists[1]
    page_matches = list_lists[2]
    return term_article_index_matches, term_searchindex_article_matches, page_matches


def get_array_first_occurences(term_searchindex_article_matches, term_article_index_matches, page_matches):
    """A feature of StatAssist is to only display
    the fist occurence of a term in the sidebar
    with a explanation, here this is evaluated"""
    occurred = []
    match_page_fo = {}
    page_of_occurence = [lst[0] for lst in page_matches]
    occurence_tuples = []
    for match_i in range(len(term_searchindex_article_matches)):
        search_match = term_searchindex_article_matches[match_i]
        article_match = term_article_index_matches[match_i]
        this_page = page_of_occurence[match_i]

        if search_match not in occurred:
            match_page_fo[search_match] = this_page
            first_occurence_page = this_page
            #returning tuple (search_match, article_match, first?, first_occurence_page)
            occurence_tuple = (search_match, article_match, True, first_occurence_page, this_page)
            occurred.append(search_match)
        else:
            first_occurence_page = match_page_fo[search_match]
            #returning tuple (search_match, article_match, first?, first_occurence_page)
            occurence_tuple = (search_match, article_match, False, first_occurence_page, this_page)

        occurence_tuples.append(occurence_tuple)

    return occurence_tuples


def get_articledict_and_occurencetuple(pdf_path, excel_path):
    search_term_index_vector = get_search_terms(excel_path)
    article_dict = analysis(pdf_path)
    term_article_index_matches, term_searchindex_article_matches, page_matches = get_term_matches_pp(
        search_term_index_vector, article_dict
    )
    occurence_tuples = get_array_first_occurences(
        term_searchindex_article_matches, term_article_index_matches, page_matches
    )
    return article_dict, occurence_tuples
