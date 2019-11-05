# 信息抽取工具RecognizersText使用

由微软开发的[RecognizersText](https://github.com/Microsoft/Recognizers-Text/tree/master/Python)是一个从文本中抽取特定信息（时间、数字等）的工具。支持中文、英文等多种语言，支持Python、Java、Node.js、C#等多种开发语言。下面举例介绍工具的使用方法。

## Package 引入

```
from recognizers_date_time import recognize_datetime
from recognizers_number import Culture, recognize_number, recognize_ordinal, recognize_percentage
from recognizers_number_with_unit import recognize_age, recognize_currency, recognize_dimension, recognize_temperature
```

## 数字抽取 recognizers_number

1. 抽取文本中的数字

```
>>> s = '首届进博会吸引了全球3617家企业参展，展览面积达27万平方米，现场成交金额 达578.3亿元。而今年，来自150多个国家和地区的3000多家企业签约参展，50万专业采购商和观众注册报名，参加的国别、地区、国际组织和参展商均超过首届。展览面积经过两次扩大，增至30多万平方米。'
>>> ret = recognize_number(s, Culture.Chinese)
>>> print([item.text for item in ret])
['3617', '27万', '578.3亿', '150', '3000', '50万', '两', '30多万']
```

2. 抽取文本中的序号

```
>>> s = "此外，第二届进博会的展区较首届也有了调整，原先的“消费电子及家电展区”今 年变更为“科技生活展区”。"
>>> ret = recognize_ordinal(s, Culture.Chinese)
>>> print([item.text for item in ret])
['第二']
```

3. 抽取文本中的百分比

```
>>> s = "7投7中又现100%命中率，连续抢板+霸气补扣，霍华德太香了"
>>> ret = recognize_percentage(s, Culture.Chinese)
>>> print([item.text for item in ret])
['100%']
```

## 抽取包含单位的数字 recognizers_number_with_unit

1. 抽取年龄

```
>>> s = "娱乐圈奇妙的合影：明明10岁和哥哥合影，20岁再合影，哥哥还没老"
>>> ret = recognize_age(s, Culture.Chinese)
>>> print([item.text for item in ret])
['10岁', '20岁']
```

2. 抽取金额

```
>>> s = "16999元！史上最贵华为手机上市：5G折叠屏Mate X，还有这些新品！"
>>> ret = recognize_currency(s, Culture.Chinese)
>>> print([item.text for item in ret])
['16999元']
```

3. 抽取距离

```
>>> s = "广州流溪河将建43.4公里碧道示范段 构建最美主题径"
>>> ret = recognize_dimension(s, Culture.Chinese)
>>> print([item.text for item in ret])
['43.4公里']
```

4. 抽取温度

```
>>> s = "冷空气到访！北京气温低迷 7日最低气温仅有1摄氏度"
>>> ret = recognize_temperature(s, Culture.Chinese)
>>> print([item.text for item in ret])
['1摄氏度']
```

## 日期抽取 recognizers_date_time

```
>>> s = "科技日报北京11月4日电 (记者张强)谷歌近日发表于《自然》杂志的论文宣布实 现了量子霸权。"
>>> ret = recognize_datetime(s, Culture.Chinese)
>>> print([item.text for item in ret])
['11月4日']
```
