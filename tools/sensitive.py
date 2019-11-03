"""
@author: Li Xi
@file: sensitive.py
@time: 2019/11/3 14:19
@desc: 敏感检测
用字典的方法检测文本中的敏感词。
使用方法见文件最下方，目前的做法是将敏感词用特定字符mask掉。
"""
import os

from tools.search import DFASearch


class Sensitive(DFASearch):
    def mask(self, content, mask_with="*"):
        result = self.search(content)
        for x in result:
            content = content.replace(x, mask_with * len(x))
        return content


if __name__ == "__main__":
    sen = Sensitive()
    sen.parse(os.path.join("..", "resource", "sensitive", "keywords.txt"))
    content = "hello sexy baby"
    content_with_mask = sen.mask(content)  # mask掉敏感词
    print(content_with_mask)
    # hello ***y baby
