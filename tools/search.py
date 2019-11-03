"""
@author: Li Xi
@file: search.py
@time: 2019/11/2 17:40
@desc: 查找关键词
应用：在文档中查找相应的关键词，可用于基于词典的敏感词检测和基于词典的情感分析等应用
主要算法：
1. 基于DFA的搜索算法
之后可根据需要添加更多的搜索算法
使用方法：见文件最下方
"""
import os


class DFASearch(object):
    """通过DFA算法查找文本中的关键词"""

    def __init__(self):
        self.keyword_tree = {}  # 词典树
        self.delimit = '\x00'

    def add_word(self, word):
        """
        向词典树中加入新的词语。下面给出一个词典树示例方便理解：
        {
            '第': {
                '一': {'\x00': 0},
                '二': {'\x00': 0}},
            '一': {
                '二': {'\x00': 0}}
        }
        :param word:
        :return:
        """
        word = word.lower().strip()
        if len(word) == 0:
            return
        level = self.keyword_tree  # 初始化当前所在的level，树的层次，子树
        for i, char_i in enumerate(word):  # 枚举关键词中的每个字符
            if char_i in level:  # 当前字符在子树中，向level下移一层
                level = level[char_i]
            else:  # 当前字符不在子树中
                if not isinstance(level, dict):
                    break
                for j, char_j in enumerate(word[i:]):  # 枚举还未加入的字符
                    level[char_j] = {}  # 初始化以新字符（不在之前子树中）为root的子树
                    last_level, last_char = level, char_j  # 标记last level和last char
                    level = level[char_j]  # 将level下移一层
                last_level[last_char] = {self.delimit: 0}  # 树的最下层叶子节点以{'\x00': 0}结束
                break
        if i == len(word) - 1:
            level[self.delimit] = 0
        # print(self.keyword_tree)

    def parse(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            words = f.readlines()
            for _w in words:
                self.add_word(_w.strip())
        print("Success load words in {}".format(str(path)))

    def search(self, content):
        """
        搜索文本中的关键词
        :param content: 待查找的文本
        :return: 查找到的关键词结果
        """
        result = []  # 存储搜索到的关键词
        content = content.lower()
        content_len = len(content)
        start = 0
        while start < content_len:
            level = self.keyword_tree
            tmp_word = ""  # 用于记录当前查找到的词语
            for char in content[start:]:
                if char in level:  # 查找到对应记录
                    tmp_word += char
                    if self.delimit not in level[char]:  # 未结束，level下移一层
                        level = level[char]
                    else:  # 查找结束
                        start += len(tmp_word) - 1  # 修改start位置
                        result.append(tmp_word)  # 将当前词语加入到result中
                        tmp_word = ""  # 清楚tmp word
                        break
                else:  # 未找到对应的记录
                    break
            start += 1
        return list(set(result))


if __name__ == "__main__":
    word_path = os.path.join("..", "resource", "sensitive", "keywords.txt")
    dfa = DFASearch()  # 初始化
    dfa.parse(word_path)  # 添加敏感词文件
    print(dfa.search("hello sexy baby"))  # 查找
    # 结果：['sex']
