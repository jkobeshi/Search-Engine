"""Serve search server."""
from threading import Thread
import flask
import requests
import search
import search.model


def thread_body(query, weight, url, hits):
    """Handle API requests."""
    # is timeout right here?
    req = requests.get(f"{url}?q={query}&w={weight}", timeout=20)
    hits.append(req.json()['hits'])


def get_top_ten(hits):
    """Get top ten hits."""
    top_10_hits = []
    while len(top_10_hits) < 10:
        largest = -1
        ind = -1
        hit_length = len(hits)
        for j in range(0, hit_length):
            if (len(hits[j]) != 0) and (hits[j][0]["score"] > largest):
                largest = hits[j][0]["score"]
                ind = j
        if largest == -1:
            break
        winner = hits[ind].pop(0)
        top_10_hits.append(winner["docid"])
    return top_10_hits


@search.app.route("/")
def show_index():
    """Service search."""
    connection = search.model.get_db()

    if flask.request.args.get('q') is not None:
        query = flask.request.args.get('q')
    else:
        context = {"hits": [], "query": "", "weight": 0.5, "lenHit": 0}
        return flask.render_template("index.html", **context)

    # double check this
    weight = 0.5
    if flask.request.args.get('w') is not None:
        weight = flask.request.args.get('w')

    hits = []
    urls = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    threads = []
    url_len = len(urls)
    for index in range(0, url_len):
        inv_ind = Thread(target=thread_body, args=(query, weight, urls[index],
                                                   hits))
        inv_ind.start()
        threads.append(inv_ind)

    for thread in threads:
        thread.join()

    top_10_hits = get_top_ten(hits)

    # for all hits in hits, query using the docid for the document info

    context = {}
    context["query"] = str(query)
    context["weight"] = weight
    context["hits"] = []
    context["lenHit"] = int(len(top_10_hits))
    for hit in top_10_hits:
        cur = connection.execute(
            "SELECT * FROM Documents "
            "WHERE docid == ?",
            (hit, )
        )
        doc = cur.fetchone()
        doc["lenUrl"] = len(doc["url"])
        doc["lenSum"] = len(doc["summary"])
        context["hits"].append(doc)
    return flask.render_template("index.html", **context)
