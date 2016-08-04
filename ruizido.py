# encoding: utf-8

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
    _terms = ["私", "内田寛", "mieruca", "FaberCompany", "サービス", "持つ", "東京工業大学", "通って", "インターン",  "応募",  "名前"]
    #文章リスト
    _documents = ["私の名前は、内田寛です。東京工業大学に通っています。", "mierucaはFaberCompanyのサービスです。", "内田寛は、meirucaをサービスに持つ、FaberCompanyのインターンに応募しています。"]
    tf_idfs = tf_idf(_terms, _documents)

    #文章0と文章1の類似度
    print(cosine_similarity(tf_idfs[0], tf_idfs[1]))
    #文章0と文章2の類似度
    print(cosine_similarity(tf_idfs[0], tf_idfs[2]))
    #文章1と文章2の類似度
    print(cosine_similarity(tf_idfs[1], tf_idfs[2]))