"""
@author: Li Xi
@file: segment.py
@time: 2019/11/5 13:28
@desc: Ltp工具基本
仅包括Ltp文档分句和句子分词的功能
具体使用方法参考：tools.ltp
"""
import os

from pyltp import SentenceSplitter, Segmentor


class LtpSegment(object):
    """LTP文档分句 句子分词工具"""
    __model_dir = os.path.join('source', 'ltp_data_v3.4.0')

    # 分句
    splitter = SentenceSplitter()

    # 分词
    segmentor = Segmentor()
    segmentor.load(os.path.join(__model_dir, "cws.model"))

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
