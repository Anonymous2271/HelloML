import numpy as np
from Tree.create import load_list_data, create_recursion_tree
from Tree.args import leaf_lmTree, err_lmTree
from Tree.predict import predict_test_data, predict_lmTree
from Tree.r_forest import random_forest, random_forest_predict
from Tree.gc_forest import *
from Tree.evaluation import *

from sklearn.model_selection import train_test_split


# # 预处理：---------------------------------------------------------
def usePCA(dataX):
    # 使用 PCA 将数据变为线性无关，影响预测准确性，弃用
    # # 分割出自变量，因为PCA只处理自变量
    # train_data = np.matrix(train_data)
    # temp_X = train_data[:, 1:]
    #
    # pca_X = outPut(temp_X, 15)
    #
    # # 复原数据
    # train_data[:, 1:] = pca_X
    # train_data = train_data.tolist()
    pass


def standardization(dataX):
    """
    0均值标准化(Z-score standardization)
    因为数据本身的量纲不统一，导致数据的数量级差别很大，导致测试数据的过拟合问题很严重，
    所以需要使用标准化处理。
    :param dataX 输入数据，列表
    :return dataTad.tolist()
    """
    dataX = np.array(dataX)
    # 我们的数据变量按列进行排列(即一行为一个样本),按列求均值，即求各个特征的均值
    meanVal = dataX.mean(axis=0)
    # meanVal = np.mean(dataX, axis=0) 此同为np的方法,得到Series
    # 求标准差
    stdVal = dataX.std(axis=0)
    dataTad = (dataX-meanVal)/stdVal
    return dataTad.tolist()


if __name__ == '__main__':
    # 载入数据---------------------------------------------------------
    # 训练数据 16维
    print("训练数据：")
    train_data = load_list_data('train_data.txt')
    train_data = standardization(train_data)
    # 检验缺省值
    print(np.isnan(train_data).any())
    # 测试数据 15维
    print("测试数据：")
    test_data = load_list_data('test_data.txt')
    test_data = standardization(test_data)
    # 检验缺失值
    print(np.isnan(test_data).any())

    #  ---------------单独使用 logistic model tree 进行训练预测----------
    # tree = create_recursion_tree(train_data,
    #                              leaf_faction=leaf_lmTree,
    #                              err_faction=err_lmTree,
    #                              opt={'err_tolerance': 1, 'n_tolerance': 901})
    # print('树结构为：')
    # print(tree)
    #
    # # 使用树预测
    # print('预测结果为：')
    # yHat = predict_test_data(tree,
    #                          test_data,
    #                          predictFacion=predict_lmTree)
    # print(yHat)

    # --------------------使用随机森林进行训练预测------------------------
    forest = random_forest(train_data, ratio=0.7, n_tree=100)
    print('森林结构为：')
    print(forest)

    print('预测结果为：')
    yHats = random_forest_predict(forest, test_data)
    print(yHats)

    # 与传统的随机森林进行对比
    from sklearn.ensemble import RandomForestClassifier

    # 评估
    test_data = np.matrix(test_data)
    y_true = test_data[:, 0]
    mre(y_true, yHats)
    r2(y_true, yHats)

    # --------------------使用深度森林进行训练预测------------------------
    # iris = load_list_data('iris.txt')
    # iris = np.matrix(iris)
    # y_iris = iris[:, -1]
    # X_iris = np.delete(iris, -1, axis=1)
    # X_iris = np.array(X_iris)
    # y_iris = np.ravel(np.array(y_iris))
    #
    # X_tr, X_te, y_tr, y_te = train_test_split(X_iris, y_iris, test_size=0.33)
    #
    # print('train_data: ', np.shape(X_tr))
    # print('test_data: ', np.shape(X_te))

    # from sklearn.datasets import load_iris, load_digits
    # iris = load_iris()
    # X = iris.data
    # y = iris.target
    # X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.33)
    # # print(np.shape(X_tr))
    # # print(np.shape(y_tr))
    # # print(y_tr)
    #
    # gcf = gcForest(shape_1X=[1, 4], window=2, tolerance=0.0)
    # gcf.fit(X_tr, y_tr)
    # y_pre = gcf.predict(X_te)
    # print('预测值为：', y_pre)
    # print('真实值为：', y_te)
    # print('acc: ', accuracy_score(y_te, y_pre, normalize=True, sample_weight=None))
    pass

