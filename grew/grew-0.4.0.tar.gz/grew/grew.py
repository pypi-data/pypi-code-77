"""
Grew module : anything you want to talk about graphs
Graphs are represented either by a dict (called dict-graph),
or by an str (str-graph).
"""
import os.path
import re
import copy
import tempfile
import json

from grew import network
from grew import utils

''' Library tools '''

def init(dev=False):
    """
    Initialize connection to GREW library
    :return: the ouput of the subprocess.Popen command.
    """
    return network.init(dev)

def grs(data):
    """Load a grs stored in a file
    :param data: either a file name or a Grew string representation of a grs
    :return: an integer index for latter reference to the grs
    :raise an error if the file was not correctly loaded
    """
    try:
        if os.path.isfile(data):
            req = { "command": "load_grs", "filename": data }
            reply = network.send_and_receive(req)
        else:
            with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".grs") as f:
                f.write(data)
                f.seek(0)  # to be read by others
                req = { "command": "load_grs", "filename": f.name }
                reply = network.send_and_receive(req)
        return reply["index"]
    except:
        raise utils.GrewError("[grew.grs] Could not build a GRS with: %s" % data)

def run(grs_data, graph_data, strat="main"):
    """
    Apply rs or the last loaded one to [gr]
    :param grs_data: a graph rewriting system or a Grew string representation of a grs
    :param graph_data: the graph, either a str (in grew format) or a dict
    :param strat: the strategy (by default "main")
    :return: the list of rewritten graphs
    """
    if isinstance(grs_data, int):
        grs_index = grs_data
    else:
        grs_index = grs(grs_data)

    req = {
        "command": "run",
        "graph": json.dumps(graph_data),
        "grs_index": grs_index,
        "strat": strat
    }
    reply = network.send_and_receive(req)
    return utils.rm_dups(reply)

def corpus(data):
    """Load a corpus from a file of a string
    :param data: a file, a list of files or a CoNLL string representation of a corpus
    :return: an integer index for latter reference to the corpus
    :raise an error if the files was not correctly loaded
    """
    try:
        if isinstance(data, list):
            req = { "command": "load_corpus", "files": data }
            reply = network.send_and_receive(req)
        elif os.path.isfile(data):
            req = { "command": "load_corpus", "files": [data] }
            reply = network.send_and_receive(req)
        else:
            with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".conll") as f:
                f.write(data)
                f.seek(0)  # to be read by others
                req = { "command": "load_corpus", "files": [f.name] }
                reply = network.send_and_receive(req)
        return reply["index"]
    except:
        raise utils.GrewError("Could not build a corpus with: %s" % data)

def search(pattern, gr):
    """
    Search for [pattern] into [gr]
    :param patten: a string pattern
    :param gr: the graph
    :return: the list of matching of [pattern] into [gr]
    """
    req = {
        "command": "search",
        "graph": json.dumps(gr),
        "pattern": pattern
    }
    reply = network.send_and_receive(req)
    return reply

def corpus_search(pattern, corpus_index):
    """
    Search for [pattern] into [corpus_index]
    :param patten: a string pattern
    :param corpus_index: an integer given by the [corpus] function
    :return: the list of matching of [pattern] into the corpus
    """
    req = {
        "command": "corpus_search",
        "corpus_index": corpus_index,
        "pattern": pattern,
    }
    return network.send_and_receive(req)

def corpus_count(pattern, corpus_index):
    """
    Count for [pattern] into [corpus_index]
    :param patten: a string pattern
    :param corpus_index: an integer given by the [corpus] function
    :return: the number of matching of [pattern] into the corpus
    """
    req = {
        "command": "corpus_count",
        "corpus_index": corpus_index,
        "pattern": pattern,
    }
    return network.send_and_receive(req)

def corpus_get(data, corpus_index):
    """
    Search for [data] in previously loaded corpus
    :param data: a sent_id (type string) or a position (type int)
    :param corpus_index: an integer given by the [corpus] function
    :return: a graph
    """
    if isinstance(data, int):
        req = {
            "command": "corpus_get",
            "corpus_index": corpus_index,
            "position": data,
        }
    elif isinstance (data, str):
        req = {
            "command": "corpus_get",
            "corpus_index": corpus_index,
            "sent_id": data,
        }
    else:
        raise utils.GrewError("Data error in 'corpus_get': %s" % data)
    return network.send_and_receive(req)

def corpus_size(corpus_index):
    """
    Return the number of sentences in the corpus
    :param corpus_index: an integer given by the [corpus] function
    :return: a integer
    """
    req = { "command": "corpus_size", "corpus_index": corpus_index}
    return network.send_and_receive(req)

def corpus_sent_ids(corpus_index):
    """
    Return the list of sent_id of sentences in the corpus
    :param corpus_index: an integer given by the [corpus] function
    :return: a list of strings
    """
    req = {
        "command": "corpus_sent_ids",
        "corpus_index": corpus_index,
    }
    return network.send_and_receive(req)

def graph_svg(graph):
    req = {
        "command": "dep_to_svg",
        "graph": json.dumps(graph),
    }
    return network.send_and_receive(req)

def json_grs(rs):
    req = {
        "command": "json_grs",
        "grs_index": rs,
    }
    return network.send_and_receive(req)


