#coding=utf-8
#%% 读取数据
import pandas as pd
data=pd.read_csv('test.csv',engine='python')

#%% 构造训练测试数据
# 按照模型的要求，构造X和y
data_set=pd.DataFrame()
for i in range(len(data)-1):
    ill24=data.iloc[i][1:25]
    other=data.iloc[i+1][25:]
    for j in range(24):
        one_data=(ill24.append(other))
        one_data['hour']=j+1
        one_data['y']=data.iloc[i+1][j+1]
        one_data=pd.DataFrame([one_data])
        data_set=data_set.append(one_data)
print(data_set.info()) #生成9*24=216行数据，每行数据29列，前28列为X，最后一列为y
#%% 将数据分为训练数据集和测试数据集
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data_set.iloc[:,:28],data_set.iloc[:,28],test_size=0.2,random_state=1)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

#%% 对比几种不同的回归模型

# 1. 线性回归
from sklearn.linear_model import LinearRegression
model1 = LinearRegression()
model1.fit(X_train, y_train)

# 2.决策树
from sklearn import tree
model2 = tree.DecisionTreeRegressor()  #OK
model2.fit(X_train,y_train)

# 3.支持向量机SVM
from sklearn import svm
model3=svm.SVR()
model3.fit(X_train,y_train)

# 4.随机森林
from sklearn import ensemble
model4=ensemble.RandomForestRegressor()
model4.fit(X_train,y_train)

# 5.KNN回归
from sklearn import neighbors
model5 = neighbors.KNeighborsRegressor()
model5.fit(X_train,y_train)


#%%模型评估
y_pred_1 = model1.predict(X_test)
y_pred_2 = model2.predict(X_test)
y_pred_3 = model3.predict(X_test)
y_pred_4 = model4.predict(X_test)
y_pred_5 = model5.predict(X_test)

from sklearn import metrics
# 用scikit-learn计算MSE,对比均方差
print("MSE1:",metrics.mean_squared_error(y_test, y_pred_1))
print("MSE2:",metrics.mean_squared_error(y_test, y_pred_2))
print("MSE3:",metrics.mean_squared_error(y_test, y_pred_3))
print("MSE4:",metrics.mean_squared_error(y_test, y_pred_4))
print("MSE5:",metrics.mean_squared_error(y_test, y_pred_5))

# model2的均方差最小，model4也还可以
#%%举例,对比预测值和实际值

print(y_test,y_pred_2,y_pred_4)