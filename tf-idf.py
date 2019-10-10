import sys, codecs
import numpy as np
import pandas as pd
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'] # 定义选取的词性
    seg = jieba.posseg.lcut(text)# 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos: # 去停用词 + 词性筛选
            l.append(i.word)
    return l

# tf-idf获取文本top10关键词
def getKeywords_tfidf(data, stopkey, topK):
    idList, titleList, abstractList = data['id'], data['title'], data['abstract']
    corpus = []# 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(idList)):
        text = '%s，%s' %(titleList[index], abstractList[index])# 拼接标题和摘要
        text = dataPrepos(text, stopkey)# 文本预处理
        text = " ".join(text)# 连接成字符串，空格分隔
        corpus.append(text)
        
    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)# 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    # 4、获取tf-idf矩阵，a[j][i]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    # 5、打印词语权重
    ids, titles, keys = [], [], []
    for i in range(len(weight)):
#         print("-------------这里输出", i+1, "篇文本的词语tf-idf------------")
        ids.append(idList[i])
        titles.append(titleList[i])
        df_word, df_weight = [], []# 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
#             print(word[j], weight[i][j])
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word, columns=['word'])
        df_weight = pd.DataFrame(df_weight, columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1)# 拼接词汇列表和权重列表，1为行对齐，0为列对齐
        word_weight = word_weight.sort_values(by="weight", ascending=False)# 按照权重值降序排列
        keyword = np.array(word_weight['word'])# 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0, topK)]# 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)
    
    result = pd.DataFrame({"id":ids, "title":titles, "key":keys}, columns = ['id', 'title', 'key'])
    return result

def main():
    # 读取数据集
    dataFile = 'sample_data.csv'
    data = pd.read_csv(dataFile)
    # 停用词表
    stopkey = [w.strip() for w in codecs.open('stopWord.txt', 'r', encoding='utf-8').readlines()]
    # tf-idf关键词抽取
    result = getKeywords_tfidf(data, stopkey, 10)
    result.to_csv("keys_TFIDF.csv",index=False)

if __name__ == '__main__':#防止调用时误运行函数外部分程序
    main()
