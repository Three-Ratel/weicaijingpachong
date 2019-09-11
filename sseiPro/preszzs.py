import os
#用来加载CSV数据的工具包
import pandas as pd
#：支持高级大量的维度数组与矩阵运算，此外也针对数组运算提供大量的数学函数库
import numpy as np
#sklearn下svm：SVM算法
from sklearn import svm
# sklearn下cross_validation：交叉验证
from sklearn import model_selection


import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)

#parse_dates=第0列解析为日期， index_col= 用作行索引的列编号）
#file_path =
data =pd.read_csv('his.csv',encoding='gbk',parse_dates=[0],index_col=0)
#print('数据',data)
#DataFrame.sort_index(axis=0 (按0列排), ascending=True（升序）,
#inplace=False（排序后是否覆盖原数据））data 按照时间升序排列
data.sort_index(0,ascending=True,inplace=True)
#print(data)
#选取5列数据作为特征：收盘价 最高价 最低价 开盘价 成交量
#dayfeature：选取150天的数据

#featurenum：选取的5个特征*天数
#x：记录150天的5个特征值 y：记录涨或者跌
dayfeature=6500
featurenum =5*dayfeature
#data.shape[0]-dayfeature意思是因为我们要用150天数据做训练，
# 对于条目为200条的数据，只有50条数据是有前150天的数据来训练的，
# 所以测试集的大小就是200-150， 对于每一条数据，他的特征是前150天的所有特征数据，
# 即150*5， +1是将当天的开盘价引入作为一条特征数据
#print(featurenum+1)
x=np.zeros((data.shape[0]-dayfeature,featurenum+1))

y=np.zeros((data.shape[0]-dayfeature))

for i in range(0,data.shape[0]-dayfeature):
    #/将数据中的“收盘价”“最高价”“开盘价”“成交量”存入x数组中
    #u:unicode编码 reshape:转换成1行，featurenum列
    x[i,0:featurenum]=np.array(data[i:i+dayfeature]\
                               [[u'开盘价',u'最高价',u'最低价',u'收盘价',u'成交量']]).reshape((1,featurenum))
    x[i,featurenum]=data.iloc[i+dayfeature][u'开盘价']
    #print(data.ix[i+dayfeature][u'收盘价'])
    #最后一列记录当日的开盘价              ix :索引
for i in range(0,data.shape[0]-dayfeature):
    if data.iloc[i+dayfeature][u'收盘价']>=data.iloc[i+dayfeature][u'开盘价']:
        y[i]=1
    else:
        y[i]=0
# print(x)
# print(y)
clf =svm.SVC(kernel='sigmoid')
#调用svm函数,并设置kernel参数，默认是rbf，其它：‘linear’‘poly’‘sigmoid’
result =[]

for i in range(5):
    #x和y的验证集和测试集，切分80 - 20 % 的测试集
    x_train,x_test,y_train,y_test = model_selection.train_test_split(x,y,test_size=0.2,train_size=0.25)
    #训练数据进行训练
    clf.fit(x_train,y_train)
    #将预测数据和测试集的验证数据比对
    result.append(np.mean(y_test ==clf.predict(x_test)))
print("svm classifier accuacy:")
print('result',result)
#result rbf [0.625, 0.5961538461538461, 0.49038461538461536, 0.5865384615384616, 0.4230769230769231]
#result sigmoid [0.5673076923076923, 0.5096153846153846, 0.5480769230769231, 0.6057692307692307, 0.47115384615384615]
