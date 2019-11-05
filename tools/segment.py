"""
@author: Li Xi
@file: segment.py
@time: 2019/11/5 13:28
@desc:
"""
import os

from pyltp import SentenceSplitter, Segmentor


class LtpSegment(object):
    """LTP文档分句 句子分词工具"""

    def __init__(self, model_dir):
        self.model_dir = model_dir

        # 分句
        self.splitter = SentenceSplitter()

        # 分词
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(self.model_dir, "cws.model"))

    def split(self, document):
        """
        长文档分句
        :param document: str
        :return: 句子 list
        """
        sentences = self.splitter.split(document)
        return [sentence for sentence in sentences if len(sentence) > 0]

    def segment(self, sentence):
        """
        句子分词
        :param sentence: str
        :return:  词语 list
        """
        words = self.segmentor.segment(sentence)
        return list(words)

    def release(self):
        """
        释放模型
        :return:
        """
        self.segmentor.release()
