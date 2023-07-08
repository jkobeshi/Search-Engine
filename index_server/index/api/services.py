"""Service v1/api routes."""
import shutil
import math
import os
import re
import flask
import index

STOP_WORDS = []
# map docID to a score
PAGERANK = {}
INVERTED_INDEX = {}


# Given two vectors, multiply indices together to get a collective sum
def dot_product(q_vec, d_vec):
    """Dot product."""
    # q and d are lists, cycle through each set and multiply
    total = 0
    # for v_index in range(0, len(q_vec)):
    for ind, val in enumerate(q_vec):
        total += float(val) * float(d_vec[ind])
    return total


def calc_score(product, weight, doc_id, qry_norm_fac, doc_norm_fac):
    """Calculate doc score."""
    # w * pagerank(d) + (1-w) * tfidf(q,d)
    tfidf = float(product / (qry_norm_fac * doc_norm_fac))
    return float(weight * PAGERANK[doc_id] + (1 - weight) * tfidf)


def load_index():
    """Put index in memory."""
    # copy over stopwords from inverted_index
    shutil.copy("inverted_index/stopwords.txt",
                "index_server/index/stopwords.txt")

    # open stopwords and put into list for later indexing
    index_path = "index_server/index"
    with open(f"{index_path}/stopwords.txt", 'r', encoding="utf-8") as file:
        for line in file:
            line = line.split("\n")[0]
            STOP_WORDS.append(line)

    with open(f"{index_path}/pagerank.out", 'r', encoding="utf-8") as file:
        for line in file:
            line = line.split("\n")[0].split(",")
            PAGERANK[str(line[0])] = float(line[1])

    invrted_index_file = os.getenv("INDEX_PATH")
    if invrted_index_file is None:
        invrted_index_file = "inverted_index_1.txt"
    inv_path = f"index_server/index/inverted_index/{invrted_index_file}"
    with open(inv_path, 'r', encoding="utf-8") as file:
        # map term to idf, and doc id to tf
        for line in file:
            line = line.split("\n")[0].split(" ", 2)

            term = line[0]  # grab term
            idf = line[1]  # grab idf(remember to cast)

            INVERTED_INDEX[str(term)] = {
                "idf": float(idf),
                "docs_dicts": {}
            }
            line = line[2].split(" ")
            while len(line) != 0:
                d_dict = {
                    "tfik": float(line[1]),
                    "norm_fac": float(line[2])
                }
                INVERTED_INDEX[str(term)]["docs_dicts"][str(line[0])] = d_dict
                line = line[3:]


@index.app.route('/api/v1/')
def get_services():
    """Return service."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


# Cleans the query and quantifies the number of terms
def clean_and_quant(query):
    """Clean query and quantify terms."""
    query_dict = {}
    cleaned_line = str(re.sub(r"[^a-zA-Z0-9 ]+", "", query)).casefold()
    words = cleaned_line.split()
    for word in words:
        if len(word) != 0 and word not in STOP_WORDS:
            if str(word) in query_dict:
                query_dict[str(word)] += 1
            else:
                query_dict[str(word)] = 1
    return query_dict


def get_doc_hit_list(query_dict):
    """Get full hit list."""
    docid_hit_list = set()
    first_word = True
    for word in query_dict:
        temp_set = set()
        dict_vec = INVERTED_INDEX[word]["docs_dicts"]
        for doc_id in dict_vec:
            temp_set.add(doc_id)
        if first_word:
            first_word = False
            docid_hit_list = temp_set
        else:
            docid_hit_list = docid_hit_list.intersection(temp_set)
    return docid_hit_list


def get_doc_id_to_score(query_dict, query_vector, weight):
    """Doc id to score."""
    # calculate norm factor of query
    query_norm_fac = 0
    for wik in query_vector:
        query_norm_fac += wik * wik
    query_norm_fac = math.sqrt(query_norm_fac)

    docid_hit_list = get_doc_hit_list(query_dict)

    # map of doc_id to document vector
    docid_to_score = {}
    for doc_id in docid_hit_list:
        doc_vector = []
        doc_norm_fac = 0  # Vector of all norm factors squared
        for word in query_dict:
            invert_ind_word = INVERTED_INDEX[word]  # Returns {idf + doc_dicts}
            doc_norm_fac = math.sqrt(
                invert_ind_word["docs_dicts"][doc_id]["norm_fac"])
            doc_vector.append(invert_ind_word["idf"] *
                              invert_ind_word["docs_dicts"][doc_id]["tfik"])

        result = calc_score(dot_product(query_vector, doc_vector),
                            weight, doc_id, query_norm_fac, doc_norm_fac)
        docid_to_score[int(doc_id)] = float(result)
    return docid_to_score


@index.app.route('/api/v1/hits/')
def get_pagerank():
    """Calculate hits for a given query."""
    args = flask.request.args
    query = args["q"]
    weight = 0.5
    if "w" in args:
        weight = float(args["w"])

    # Cleans the query and quantifies each word for term freq
    query_dict = clean_and_quant(query)
    query_vector = []
    for key, value in query_dict.items():
        if key not in INVERTED_INDEX:
            context = {
                "hits": []
            }
            return flask.jsonify(**context)
        term_idf = INVERTED_INDEX[key]["idf"]
        query_vector.append(term_idf * value)

    # helper
    docid_to_score = get_doc_id_to_score(query_dict, query_vector, weight)

    # Sort Score map
    docid_to_score = sorted(docid_to_score.items(), key=lambda x: x[1])
    context = {
        "hits": []
    }
    for dic in docid_to_score[::-1]:
        score_dict = {
            "docid": int(dic[0]),
            "score": float(dic[1])
        }
        context["hits"].append(score_dict)

    return flask.jsonify(**context)
