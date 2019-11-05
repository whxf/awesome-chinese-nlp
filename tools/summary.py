"""
@author: Li Xi
@file: summary.py
@time: 2019/11/5 13:01
@desc: 获取文本摘要
1. 使用text rank的方式获取摘要
2. 使用方式如文档最下所示
"""
import os
from itertools import combinations

import networkx as nx
import numpy as np

from tools.segment import LtpSegment


class Summary(object):
    """使用text rank的方式获取文本摘要"""

    def __init__(self):
        self.ltp_seg_tool = LtpSegment()  # 使用ltp工具进行文档分句和句子分词

    def calculate_weight(self, words1, words2):
        """
        计算两个句子边的weight
        :param words1: word list
        :param words2: word list
        :return:
        """
        if len(words1) <= 1 or len(words2) <= 1:
            return 0.0
        return len(set(words1) & set(words2)) / (np.log2(len(words1)) + np.log2(len(words2)))

    def get_summary(self, doc, topK=5, with_importance=False):
        """
        获取文档的摘要
        :param doc: 待分析文档 str类型
        :param topK: 获取重要性top k的句子作为最终摘要
        :param with_importance: 是否显示句子重要性
        :return: top k句子 list
        """
        sentences = self.ltp_seg_tool.split(doc)  # 文档分句
        tokenized_sentences = [self.ltp_seg_tool.segment(sentence) for sentence in sentences]  # 句子分词
        G = nx.Graph()  # 构造graph
        for u, v in combinations(range(len(tokenized_sentences)), 2):
            G.add_edge(u, v, weight=self.calculate_weight(tokenized_sentences[u], tokenized_sentences[v]))
        pr = nx.pagerank_scipy(G)  # 计算page rank
        pr_sorted = sorted(pr.items(), key=lambda x: x[1], reverse=True)  # 按照重要性排序
        # 抽取出top k的句子，返回摘要
        if with_importance:
            return [(sentences[i], imp) for i, imp in pr_sorted[:topK]]
        else:
            return [sentences[i] for i, rank in pr_sorted[:topK]]


if __name__ == "__main__":
    doc = """
    科技日报北京11月4日电 (记者张强)谷歌近日发表于《自然》杂志的论文宣布实现了量子霸权。记者4日获悉，在国际上率先开启称霸标准研究的、国防科技大学计算机学院吴俊杰带领的QUANTA团队，联合信息工程大学等国内外科研机构，提出了量子计算模拟的新算法。该算法在“天河二号”超级计算机上的测试性能达到国际领先水平，谷歌的工作也引用了这项结果的预印版论文。当地时间4日，国际权威期刊《物理评论快报》正式在线发表了该成果。

量子霸权，代表量子计算装置在特定测试案例上表现出超越所有经典计算机的计算能力，实现量子霸权是量子计算发展的重要里程碑。评测称霸标准，需要高效的、运行于经典计算机的量子计算模拟器。在后量子霸权时代，这种模拟器还会成为s加速量子计算科学研究的重要工具。

论文作者、博士研究生刘雍介绍，量子计算模拟的实际难度，并不完全依赖于量子比特的数目或量子门的数目，而是取决于运算过程中量子态的复杂程度——量子纠缠度。该项研究提出了一种依赖于量子纠缠度的模拟算法，开发了通用量子线路模拟器，并在“天河二号”超级计算机上完成了量子霸权测试案例——随机量子线路采样问题的模拟，实际测试了49、64、81、100等不同数目量子比特在不同量子线路深度下的问题实例，计算性能达到国际领先水平。

刘雍指出，量子霸权的实现并非量子计算研究的终点，而是量子计算发展的起点。除了继续提升量子计算物理系统的性能外，有噪声系统中的量子算法、量子纠错等都将成为量子计算下一阶段的研究重点。

据悉，该项研究获得了中国长城量子实验室、国家超级计算广州中心、国家自然科学基金委等单位的支持。
    """

    summary_tool = Summary()  # 初始化摘要生成工具
    print("\n".join(summary_tool.get_summary(doc, topK=5)))  # 获取摘要

    # 该项研究提出了一种依赖于量子纠缠度的模拟算法，开发了通用量子线路模拟器，并在“天河二号”超级计算机上完成了量子霸权测试案例——随机量子线路采样问题的模拟，实际测试了49、64、81、100
    # 等不同数目量子比特在不同量子线路深度下的问题实例，计算性能达到国际领先水平。
    # 记者4日获悉，在国际上率先开启称霸标准研究的、国防科技大学计算机学院吴俊杰带领的QUANTA团队，联合信息工程大学等国内外科研机构，提出了量子计算模拟的新算法。
    # 据悉，该项研究获得了中国长城量子实验室、国家超级计算广州中心、国家自然科学基金委等单位的支持。
    # 量子霸权，代表量子计算装置在特定测试案例上表现出超越所有经典计算机的计算能力，实现量子霸权是量子计算发展的重要里程碑。
    # 评测称霸标准，需要高效的、运行于经典计算机的量子计算模拟器。
