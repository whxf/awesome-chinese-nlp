"""
@author: Li Xi
@file: ltp.py
@time: 2019/10/29 16:29
@desc:  LTP工具
包括功能有：
    1. 长文档分句
    2. 句子分词
    3. 词性标注
    4. 命名实体识别
    5. 依存句法分析
    6. 语义角色标注
使用方法：
    见文件最下方
各项返回值具体含义：
    请参考LTP官方文档：https://ltp.readthedocs.io/zh_CN/latest/appendix.html#
"""
import os

from pyltp import Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller

from tools.segment import LtpSegment


class Ltp(LtpSegment):
    __model_dir = os.path.join('source', 'ltp_data_v3.4.0')

    # 词性标注
    postagger = Postagger()
    postagger.load(os.path.join(__model_dir, "pos.model"))

    # 命名实体识别
    recognizer = NamedEntityRecognizer()
    recognizer.load(os.path.join(__model_dir, "ner.model"))

    # 依存句法分析
    parser = Parser()
    parser.load(os.path.join(__model_dir, "parser.model"))

    # 语义角色标注
    labeller = SementicRoleLabeller()
    labeller.load(os.path.join(__model_dir, "pisrl.model"))

    def __init__(self):
        super().__init__()

    def postag(self, words):
        """
        词性标注
        :param input: 分词结果 list
        :return: 词性 list
        """
        postags = self.postagger.postag(words)
        return list(postags)

    def recognize(self, words, postags):
        """
        命名实体识别：
        1. LTP 采用 BIESO 标注体系：B表示实体开始词；I表示实体中间词；E表示实体结束词；
           S表示单独成实体；O表示不构成命名实体
        2. LTP 提供的命名实体类型为：人名（Nh）；地名（Ns）；机构名（Ni）
        3. B、I、E、S位置标签和实体类型标签之间用一个横线 - 相连；O标签后没有类型标签
        例如：
            S-Nh 表示单独一个词构成了人名。
        :param words: 分词结果 list
        :param postags: 词性标注结果 list
        :return: 命名实体标注结果 list
        """
        netags = self.recognizer.recognize(words, postags)
        return list(netags)

    def parse(self, words, postags):
        """
        依存句法分析
        :param words: 分词结果 list
        :param postags: 词性标注结果 list
        :return: ltp原生结果
            (arc.head, arc.relation) for arc in arcs
            ROOT节点的索引是0，第一个词开始的索引依次为1、2、3
            arc.relation 表示依存弧的关系。
            arc.head 表示依存弧的父节点词的索引，arc.relation 表示依存弧的关系。
        例：
        inputs：
            words = ['元芳', '你', '怎么', '看']
            postags = ['nh', 'r', 'r', 'v']
        output：
            4:SBV 4:SBV 4:ADV 0:HED
            输出格式为 head：relation
        """
        arcs = self.parser.parse(words, postags)
        return arcs

    def label(self, words, postags, arcs):
        """
        语义角色标注
        :param words: 分词结果 list
        :param postags: 词性标注结果 list
        :param arcs: 依存句法分析结果 ltp
        :return: ltp原生结果
            (arg.name, arg.range.start, arg.range.end) for arg in role.arguments
            第一个词开始的索引依次为0、1、2
            返回结果 roles 是关于多个谓词的语义角色分析的结果。由于一句话中可能不含有语义角色，所以
            结果可能为空。role.index 代表谓词的索引， role.arguments 代表关于该谓词的若干语义角
            色。arg.name 表示语义角色类型，arg.range.start 表示该语义角色起始词位置的索引，
            arg.range.end 表示该语义角色结束词位置的索引。
        例：
        inputs：
            words = ['元芳', '你', '怎么', '看']
            postags = ['nh', 'r', 'r', 'v']
            arcs 使用依存句法分析的结果
        output：
            3 A0:(0,0)A0:(1,1)ADV:(2,2)

            由于结果输出一行，所以“元芳你怎么看”有一组语义角色。
            其谓词索引为3，即“看”。
            这个谓词有三个语义角色范围分别是：
                (0,0)即“元芳”，(1,1)即“你”，(2,2)即“怎么”，类型分别是A0、A0、ADV。
        """
        roles = self.labeller.label(words, postags, arcs)
        return roles

    def get_name_entity(self, sentence, entity_type):
        """
        获取句子中特定的命名实体集
        :param sentence: 待分析句子
        :param entity_type: 待分析命名实体类型，可选值
        :return:
        """
        words = self.segment(sentence)
        postags = self.postag(words)
        ne_tags = self.recognize(words, postags)
        sentence_len = len(words)

        ret_entity = set()
        entity_pattern = ""
        for i in range(sentence_len):
            if (ne_tags[i] == 'B-' + entity_type) or (ne_tags[i] == 'B-' + entity_type):
                entity_pattern += words[i]
            elif (ne_tags[i] == 'E-' + entity_type) or (ne_tags[i] == 'S-' + entity_type):
                entity_pattern += words[i]
                ret_entity.add(entity_pattern)
                entity_pattern = ""

        return list(ret_entity)


if __name__ == "__main__":
    doc = "“元芳体”的创意来源于古装侦探系列电视剧《神探狄仁杰》。" \
          "剧中的狄公经常征求助手李元芳的意见，从而借对话引出对案情的分析。" \
          "李元芳的标准回答有两个，一个是“大人，我觉得此事有蹊跷”，另一个是“此事背后一定有一个天大的秘密。”"
    sentence = "元芳你怎么看？"

    # 初始化
    ltp_tool = Ltp()  # ltp模型存储位置
    print("-----{}-----".format(" 初始化 "))

    # 长文档分句
    split_out = ltp_tool.split(doc)
    print("-----{}-----".format(" 长文档分句 "))
    print('\n'.join(split_out))

    # 句子分词
    segment_out = ltp_tool.segment(sentence)
    print("-----{}-----".format(" 句子分词 "))
    print(' '.join(segment_out))

    # 词性标注
    postag_out = ltp_tool.postag(segment_out)
    print("-----{}-----".format(" 词性标注 "))
    print(' '.join(postag_out))

    # 命名实体识别
    recognize_out = ltp_tool.recognize(segment_out, postag_out)
    print("-----{}-----".format(" 命名实体识别 "))
    print(' '.join(recognize_out))

    # 依存句法分析
    parse_out = ltp_tool.parse(segment_out, postag_out)
    print("-----{}-----".format(" 依存句法分析 "))
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in parse_out))

    # 语义角色标注
    label_out = ltp_tool.label(segment_out, postag_out, parse_out)
    print("-----{}-----".format(" 语义角色标注 "))
    for role in label_out:
        print(role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

    # 获取句子中特定的命名实体集
    ne = ltp_tool.get_name_entity(sentence, "Nh")  # 获取人名
    print("-----{}-----".format(" 获取句子中特定的命名实体集 "))
    print(' '.join(ne))
