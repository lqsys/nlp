import sys
import pandas as pd
import jieba.analyse

#处理标题和摘要，提取关键字
def getKeywords_textrank(data, topK):
    idList, titleList, abstractList = data['id'], data['title'], data['abstract']
    ids, titles, keys = [], [], []
    for index in range(len(idList)):
        text = '%s: %s' %(titleList[index], abstractList[index])#拼接标题和摘要
        jieba.analyse.set_stop_words("stopWord.txt")
        print("\"",titleList[index],"\"" , " 10 Keywords - TextRank :")
        keywords = jieba.analyse.textrank(text, topK=topK, allowPOS = ('n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'))
        word_split = " ".join(keywords)
        print(word_split)
        keys.append(word_split)
#         keys.append(word_split.encode("utf-8"))
        ids.append(idList[index])
        titles.append(titleList[index])
    
    result = pd.DataFrame({"id":ids, "title":titles, "key":keys}, columns=['id', 'title', 'key'])
    return result

def main():
    dataFile = 'sample_data.csv'
    data = pd.read_csv(dataFile)
    result = getKeywords_textrank(data, 10)
    print(result)
    result.to_csv("keys_TextRank.csv", index=False)

if __name__ == '__main__':
    main()
