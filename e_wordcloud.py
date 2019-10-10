filename = "yes-minister.txt"
with open(filename, encoding = 'utf-8') as f:
    mytext = f.read()

from wordcloud import WordCloud
wordcloud = WordCloud().generate(mytext)

%pylab inline
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
