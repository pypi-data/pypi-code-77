from sklearn.metrics import jaccard_score


def jacc(y_true, y_pred):
    return jaccard_score(y_true, y_pred, average='binary')
