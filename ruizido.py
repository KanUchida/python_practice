__author__ = 'emoson'


def cosine_similarity(v1, v2):
    """
    ベクトルv1, v2のcos類似度の算出
    """
    return sum([a*b for a, b in zip(v1, v2)])/(sum(map(lambda x: x*x, v1))**0.5 * sum(map(lambda x: x*x, v2))**0.5)


def tf(terms, document):
    """
    TF値の計算。単語リストと文章を渡す
    :param terms:
    :param document:
    :return:
    """
    tf_values = [document.count(term) for term in terms]
    return list(map(lambda x: x/sum(tf_values), tf_values))


def idf(terms, documents):
    """
    IDF値の計算。単語リストと全文章を渡す
    :param terms:
    :param documents:
    :return:
    """
    import math
    return [math.log10(len(documents)/sum([bool(term in document) for document in documents])) for term in terms]


def tf_idf(terms, documents):
    """
    TF-IDF値を計算。文章毎にTF-IDF値を計算
    :param terms:
    :param documents:
    :return:
    """
    return [[_tf*_idf for _tf, _idf in zip(tf(terms, document), idf(terms, documents))] for document in documents]


if __name__ == "__main__":
    #単語リスト
    _terms = ["ミエルカ", "自然言語処理", "人工知能"]
    #文章リスト
    _documents = ["ミエルカ、ミエルカ", "ミエルカと自然言語処理", "自然言語処理と人工知能"]
    tf_idfs = tf_idf(_terms, _documents)

    #文章0と文章1の類似度
    print(cosine_similarity(tf_idfs[0], tf_idfs[1]))
    #文章0と文章2の類似度
    print(cosine_similarity(tf_idfs[0], tf_idfs[2]))
    #文章1と文章2の類似度
    print(cosine_similarity(tf_idfs[1], tf_idfs[2]))