from collections import Counter
from itertools import chain

def top_words(word_list, CUTOFF = None):
    ## Takes a list of words and returns the top N frequent words
    # https://www.geeksforgeeks.org/find-k-frequent-words-data-set-python/
    # Pass the split_it list to instance of Counter class.
    word_count = Counter(word_list)
    # most_common() produces k frequently encountered
    # input values and their respective counts
    if CUTOFF is None:
        return([var[1] for var in enumerate(word_count)])

    else:
        most_occur = word_count.most_common(CUTOFF)
        return([var[1][0] for var in enumerate(most_occur)])

def compute_frequent_keywords(edge_to_nodes: dict, compare_list: list = None,CUTOFF = None):
    top_n_cutoff = CUTOFF
    if compare_list is None:
        keywords = list(chain.from_iterable(edge_to_nodes.values()))
        return (top_words(keywords, top_n_cutoff))
    else:
        words_in_values = []
        for edge, nodes in edge_to_nodes.items():
            if edge in compare_list:
                words_in_values.extend(nodes)
        return(top_words(words_in_values,top_n_cutoff))