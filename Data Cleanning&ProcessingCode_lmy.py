#!/usr/bin/env python
# coding: utf-8

# In[70]:


import pandas as pd
import numpy as np
#导入


# In[145]:


#导入数据集
df= pd.read_csv('C:\\Users\ellel\PythonProcessing\comments_917_final.csv')
df


# In[146]:


#将初步清洗后内容写入xlsx文件用于用户画像的可视化
outputpath='C:\\Users\ellel\PythonProcessing/Comments.xlsx'
df.to_excel(outputpath,index=False,header=True)


# 分析评论内容并做词云

# In[147]:


#获取评论内容
comment=df.iloc[:,4]
df.iloc[:,4]


# In[149]:


#将评论内容写入txt文件
df1=comment
df1.to_csv('file917.txt', header=None,sep=' ', index= False)


# In[150]:


#引入jieba和wordcloud做词云
from wordcloud import WordCloud
import jieba


# In[151]:


# 分词
def trans_CN(text):
# 接收分词的字符串
    word_list = jieba.cut(text)
    # 分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result


# In[152]:


#去除标点符号
text= open("C:\\Users\\ellel\\file917.txt","r", encoding='utf-8').read()
import string
from string import punctuation 
import re

str=text
add_punc='，。、【】“”：；"\n"（）《》‘’了 {}？！⑦()、%^>℃：.” “^ 无语-——=擅长 真 所以 没有 还被 就 吧 和于的&#@￥呵 是 不 也在 我天 了 一个 吗害草 淦 操 ~ 哎啧哈 ~啊这 …哇哦Emm'
all_punc= punctuation +add_punc
temp = []
for c in str:
    if c not in all_punc :
        temp.append(c)
newText1 = ''.join(temp)
print(newText1)


# In[153]:


#中文内容分词
words = jieba.lcut(newText1)     # 使用精确模式对文本进行分词
counts = {}     # 通过键值对的形式存储词语及其出现的次数
afcutw=" ".join(words)


# In[155]:


#生成词云
from wordcloud import WordCloud
import PIL.Image as image
wordcloud=WordCloud(font_path="C:\Windows\Fonts\AdobeHeitiStd-Regular.otf",height=1200,width=1600,random_state=50).generate(afcutw)
image_produce = wordcloud.to_image()
image_produce.show()
wordcloud.to_file('917comment.png')#保存词云图


# # 原用于作图代码

# In[6]:


#获取用户性别
gender17=df917.iloc[:,0]
df.iloc[:,0]


# In[9]:


#做饼图
import matplotlib.pyplot as plt

labels = ['Male','Female']

x = [35.4,64.6]

#显示百分比
plt.pie(x,labels=labels,autopct='%1.2f%%')

#设置x,y的刻度一样，使其饼图为正圆
plt.axis('equal')

plt.show()


# In[8]:


#替换m和f
gender17.replace(['m','f'],['Male','Female'],inplace=True)
#计算男女频数

genders=gender17
count1={}
for gender in genders:
        count1[gender] = count1.get(gender, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1
        
items1 = list(count1.items())#将键值对转换成列表
items1


# In[13]:


#获取用户年龄
age17=df917.iloc[:,2]
age17
#删除无效行
age17=age17.fillna('无')
ages=age17[~age17.isin(['无'])]
print(ages)


# In[14]:


#绘制直方图
plt.hist(ages,bins=20,color='steelblue')
plt.xlabel('age')
plt.ylabel('frequency')


# In[15]:


#计算元素频率
from collections import Counter
list=ages
counter= Counter(ages)
counterm=counter.most_common()

#dfc=pd.DataFrame(counter,index=['frequency'])
 

#dfc1=dfc.stack()
#print(dfc1)
# 将字典拆分为键和值的列表

keys = counter.keys()

values = counter.values()

#df做表
#dfc=pd.DataFrame(keys,columns=['age'])
#dfc=pd.concat([dfc,pd.DataFrame(values,columns=['frequency'])])


# In[16]:


#绘制散点图
plt.scatter(x=keys,y=values)

