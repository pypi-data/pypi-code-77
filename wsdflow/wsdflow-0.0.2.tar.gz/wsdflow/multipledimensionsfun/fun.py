import random
from wsdflow.multipledimensionscore.core import *
from sklearn.utils import resample

def forward_and_backward(graph):
    # execute all the forward method of sorted_nodes.

    ## In practice, it's common to feed in mutiple data example in each forward pass rather than just 1. Because the examples can be processed in parallel. The number of examples is called batch size.
    for n in graph:
        n.forward()
        ## each node execute forward, get self.value based on the topological sort result.

    for n in  graph[::-1]:
        n.backward()

def forward(graph):
    for n in graph:
        if n.name != 'mse':
            n.forward()


###   v -->  a -->  C
##    b --> C
##    b --> v -- a --> C
##    v --> v ---> a -- > C


def toplogic(graph):
    sorted_node = []

    while len(graph) > 0:

        all_inputs = []
        all_outputs = []

        for n in graph:
            all_inputs += graph[n]
            all_outputs.append(n)

        all_inputs = set(all_inputs)
        all_outputs = set(all_outputs)

        need_remove = all_outputs - all_inputs  # which in all_inputs but not in all_outputs

        if len(need_remove) > 0:
            node = random.choice(list(need_remove))

            need_to_visited = [node]

            if len(graph) == 1: need_to_visited += graph[node]

            graph.pop(node)
            sorted_node += need_to_visited

            for _, links in graph.items():
                if node in links: links.remove(node)
        else:  # have cycle
            break

    return sorted_node

from collections import defaultdict


def convert_feed_dict_to_graph(feed_dict):
    computing_graph = defaultdict(list)

    nodes = [n for n in feed_dict]

    while nodes:
        n = nodes.pop(0)

        if isinstance(n, Placeholder):
            n.value = feed_dict[n]

        if n in computing_graph: continue

        for m in n.outputs:
            computing_graph[n].append(m)
            nodes.append(m)

    return computing_graph


def topological_sort_feed_dict(feed_dict):
    graph = convert_feed_dict_to_graph(feed_dict)

    return toplogic(graph)


def optimize(trainables, learning_rate=1e-2):
    # there are so many other update / optimization methods
    # such as Adam, Mom,
    for t in trainables:
        t.value += -1 * learning_rate * t.gradients[t]
    return trainables


def run(X_, y_, epochs, batch_size = 1):
    # Normalize data
    X_ = (X_ - np.mean(X_, axis=0)) / np.std(X_, axis=0)

    n_features = X_.shape[1]
    n_hidden = 10
    W1_ = np.random.randn(n_features, n_hidden)
    b1_ = np.zeros(n_hidden)
    W2_ = np.random.randn(n_hidden, 1)
    b2_ = np.zeros(1)

    # Neural network
    X, y = Placeholder(name='x'), Placeholder(name='y')
    W1, b1 = Placeholder(name='w1'), Placeholder(name='b1')
    W2, b2 = Placeholder(name='w2'), Placeholder(name='b2')

    l1 = Linear(X, W1, b1, name='l1')
    s1 = Sigmoid(l1, name='s1')
    l2 = Linear(s1, W2, b2, name='l2')
    cost = MSE(y, l2, name='mse')

    feed_dict = {
        X: X_,
        y: y_,
        W1: W1_,
        b1: b1_,
        W2: W2_,
        b2: b2_
    }

    # Total number of examples
    m = X_.shape[0]
    steps_per_epoch = m // batch_size
    graph = topological_sort_feed_dict(feed_dict)
    trainables = [W1, b1, W2, b2]

    losses = []

    for i in range(epochs):
        loss = 0
        for j in range(steps_per_epoch):
            # Step 1
            # Randomly sample a batch of examples
            X_batch, y_batch = resample(X_, y_, n_samples=batch_size)

            # Reset value of X and y Inputs
            X.value = X_batch
            y.value = y_batch

            # Step 2
            _ = None
            forward_and_backward(graph)  # set output node not important.

            # Step 3
            rate = 1e-2
            optimize(trainables, rate)

            loss += graph[-1].value

        # print("Epoch: {}, Loss: {:.3f}".format(i + 1, loss / steps_per_epoch))
        losses.append(loss / steps_per_epoch)

    return losses, graph