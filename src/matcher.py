'''receives words of the pdf with coordinates and an excel sheet with
search_queries in the first column. The matched words or collocations
will be returned in a dictionary'''

from src.parser import analysis
import pandas as pd
import regex as re


def get_search_terms(excel_path, col=1, sublist_sep=','):
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
    search_term_index_vector = {}
    counter = 0
    for terms in term_query:
        for term in terms:
            search_term_index_vector[str(term)] = counter
        counter += 1
    return search_term_index_vector


def subfinder(mylist, pattern):
    '''returns sublists if in list.
    specifically the x1 and x2 coordinates
    the sublist resides in the superlist'''
    matches = []
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            matches.append([i, i+len(pattern)])
    return matches


def get_subwords_from_articleterms(article_words):
    subwordindex_wordindex = {}
    article_subwords = []
    for i in range(len(article_words)):
        term = article_words[i]
        subwords = re.split("[^a-z]", term)
        for subword in subwords:
            article_subwords.append(subword)
            subwordindex_wordindex[len(article_subwords)-1] = i
    return article_subwords, subwordindex_wordindex


def remove_duplicates_list(lst):
    clean_list = []
    for item in lst:
        if item not in clean_list:
            clean_list.append(item)
    return clean_list


def get_term_matches_pp(search_term_index_vector, article_dict):
    '''matches the search_terms to the pages
    returns a list of term matches per page.
    shallow duplicates are discarded
    (alternative representations of same
    concepts are retained)'''
    search_terms = [term.lower() for term in search_term_index_vector]
    article_words = [word.lower() for word in article_dict["words"]]
    article_subwords, subwordindex_wordindex = get_subwords_from_articleterms(
        article_words)
    term_article_index_matches = []
    for term in search_terms:
        term = term.split()
        group_matches = subfinder(article_subwords, term)
        if group_matches:
            for match in group_matches:
                this_match_indexes = []
                for index in match:
                    original_index = subwordindex_wordindex[index]
                    this_match_indexes.append(original_index)
                this_match_indexes = remove_duplicates_list(this_match_indexes)
                term_article_index_matches.append(this_match_indexes)
    return term_article_index_matches


def get_array_first_occurences(term_article_index_matches):
    '''A feature of StatAssist is to only display
    the fist occurence of a term in the sidebar
    with a explanation, here this is evaluated'''
    mirror_first_ocurrences = []
    for match in term_article_index_matches:
        mirror_first_ocurrences.append([1])
        if len(term_article_index_matches) > 1:
            for i in range(1, len(match)):
                mirror_first_ocurrences[-1].append(0)
    return mirror_first_ocurrences


def get_match_occur_dict(article_dict, search_term_index_vector):
    '''returns package in dictionary format'''
    term_article_index_matches = get_term_matches_pp(search_term_index_vector,
                                                     article_dict)
    array_first_occurences = get_array_first_occurences(
                                                    term_article_index_matches)
    match_occur_dict = {
        'matches': term_article_index_matches,
        'first': array_first_occurences,
        }
    return match_occur_dict


def get_articledict_and_matchesdict(pdf_path, excel_path):
    search_term_index_vector = get_search_terms(excel_path)
    article_dict = analysis(pdf_path)
    match_occur_dict = get_match_occur_dict(article_dict,
                                            search_term_index_vector)
    article_dict["matches"] = match_occur_dict["matches"]
    article_dict["first"] = match_occur_dict["first"]
    return article_dict, match_occur_dict
