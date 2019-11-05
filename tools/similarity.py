"""
@author: Li Xi
@file: similarity.py
@time: 2019/10/30 15:37
@desc:
计算文本相似度：
1. WordMoverDistance 基于词移距离的文本相似度计算 【比较文档的相似度】
2. WordVectorSimilarity word-vector的句子相似度计算  【比较句子的相似度】
注意事项：
* 两种方法都需要输入句子分词之后的结果，类型需要时list
* 为提升效率/效果，可对分词结果进行处理，如去除停用词等
* 具体使用方法见文件的最下
* 可自定义加载词向量文件
"""
import os

import gensim
import numpy as np

from tools.segment import LtpSegment


class WordMoverDistance(object):
    """词移距离 Word Mover's Distance"""

    def __init__(self):
        # 初始化词向量模型
        self.vector_path = os.path.join("source", "sgns.renmin.word.bz2")
        self.word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(self.vector_path)
        self.word2vec_model.init_sims(replace=True)  # normalizes vectors

    def distance(self, tokens1, tokens2):
        """
        计算词移距离
        !!!: 这里需要输入句子的分词后结果
        :param tokens1: [list]
        :param tokens2: [list]
        :return: score 值
        """
        distance = self.word2vec_model.wmdistance(tokens1, tokens2)
        return distance


class WordVectorSimilarity(object):
    """
    基于word-vector的句子相似度计算（余弦相似度）
    !!!: 不仅可以使用词向量也可使用字向量
    """

    def __init__(self, vector_dim=300):
        """

        :param vector_dim: 词向量的维度
        """
        self.vector_path = os.path.join("source", "sgns.renmin.word.bz2")
        self.word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(self.vector_path)
        self.vector_dim = vector_dim

    def get_word_vector(self, word):
        """
        获取词的词向量，如果没有找到，返回全零的embedding
        :param word:
        :return:
        """
        try:
            return self.word2vec_model[word]
        except:
            return np.zeros(self.vector_dim)

    def similarity_cosine(self, tokens1, tokens2):
        """
        计算句子的余弦相似度，其中句子向量等于字符向量求平均
        !!!: 这里需要输入句子的分词后结果
        :param tokens1:
        :param tokens2:
        :return:
        """
        # 求 sentence1 的向量表示
        sentence1 = np.zeros(self.vector_dim)
        for _token in tokens1:
            sentence1 += self.get_word_vector(_token)
        sentence1 = sentence1 / len(tokens1)

        # 求 sentence2 的向量表示
        sentence2 = np.zeros(self.vector_dim)
        for _token in tokens2:
            sentence2 += self.get_word_vector(_token)
        sentence2 = sentence2 / len(tokens2)

        # 余弦相似度计算公式 sim = sum(a*b) / { sum[ sqrt(a^2) ] * sum[ sqrt(b^2) ] }
        cos1 = np.sum(sentence1 * sentence2)
        cos21 = np.sqrt(sum(sentence1 ** 2))
        cos22 = np.sqrt(sum(sentence2 ** 2))
        similarity = cos1 / float(cos21 * cos22)
        return similarity

    def distance(self, tokens1, tokens2):
        """
        计算 WordVectorSimilarity
        !!!: 这里需要输入句子的分词后结果
        :param tokens1:
        :param tokens2:
        :return:
        """
        return self.similarity_cosine(tokens1, tokens2)


if __name__ == "__main__":
    # -------- Begin WordMoverDistance Test --------
    # 初始化 WordMoverDistance
    sim = WordMoverDistance()
    # 初始化 LTP 用于分词
    ltp = LtpSegment()

    str1 = ltp.segment("我是中国人，我深爱着我的祖国")  # 分词结果为list
    str2 = ltp.segment("中国是我的母亲，我热爱她")
    print("相似度：{}".format(sim.distance(str1, str2)))
    # 相似度：0.5040331478972442

    str1 = ltp.segment("小勇硕士毕业于北京语言大学，目前在中科院软件所工作")
    str2 = ltp.segment("大方博士就读于首都师范大学，未来不知道会在哪里上班")
    print("相似度：{}".format(sim.distance(str1, str2)))
    # 相似度：0.8857186341563674
    # -------- End WordMoverDistance Test --------

    # -------- Begin WordVectorSimilarity Test --------
    # 初始化 WordVectorSimilarity
    sim = WordVectorSimilarity()
    # 初始化 LTP 用于分词
    ltp = LtpSegment()

    str1 = ltp.segment("我是中国人，我深爱着我的祖国")  # 分词结果为list
    str2 = ltp.segment("中国是我的母亲，我热爱她")
    print("相似度：{}".format(sim.distance(str1, str2)))
    # 相似度：0.9048935250581785

    str1 = ltp.segment("小勇硕士毕业于北京语言大学，目前在中科院软件所工作")
    str2 = ltp.segment("大方博士就读于首都师范大学，未来不知道会在哪里上班")
    print("相似度：{}".format(sim.distance(str1, str2)))
    # 相似度：0.812708497722071
    # -------- End WordVectorSimilarity Test --------
