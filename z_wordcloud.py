import jieba
import re
import numpy as np
from scipy.misc import imread
from PIL import Image
import matplotlib.pyplot as plt
import wordcloud
import codecs
import collections

fn = open('yangben.txt', encoding='utf-8')
data = fn.read()
fn.close()

pattern = re.compile('\t|\n|\.|-|：|；|\)|\(|\?|（|）|“|”|。|，|\|"|\u3000') # 定义正则表达式匹配模式
data = re.sub(pattern, '', data) # 将符合模式的字符去除

seg = jieba.cut(data, cut_all = False)# 精确模式分词
word_List = []
# 停用词表
stopkey = [w.strip() for w in codecs.open('stopWord.txt', 'r', encoding='utf-8').readlines()]

for i in seg:# 循环读出每个分词
    if i not in stopkey:# 如果不在去除词库中
        word_List.append(i) # 分词追加到列表

word_counts = collections.Counter(word_List) # 对分词做词频统计
word_counts_top10 = word_counts.most_common(10) # 获取前10最高频的词

mask = np.array(Image.open('lmf.jpg'))
wc = wordcloud.WordCloud(
    font_path = 'C:\Windows\Fonts\msyh.ttf',# 显示中文，从属性里复制字体名称，不能直接看windows显示的字体名
    background_color="white",# 背景颜色
    mask=mask,# 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
    max_words=2000, # 最大词数
    random_state=42,# 为每个词返回一个PIL颜色
    width=1000, height=860, margin=2,#图片的长宽，边界值
    max_font_size=100 # 字体最大值
)

wc.generate_from_frequencies(word_counts) # 从字典生成词云
image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
plt.imshow(wc) # 显示词云
plt.axis('off') # 关闭坐标轴
plt.show() # 显示图像
