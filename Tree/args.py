import numpy as np


def split_data(dataset, feat_idx, value):
    """
    根据给定的特征编号和特征值对数据集进行分割
    :returns list 矩阵
    """
    left, right = [], []
    for line in dataset:
        if line[feat_idx] <= value:
            left.append(line)
        else:
            right.append(line)

    return left, right


def choose_best_feature(dataList, tree_type='regression', num_remove=0, opt=None):
    """
    选取最佳分割特征和特征值
    :param opt: [err_tolerance: 最小误差下降值, n_tolerance: 数据切分最小样本数]
    :param num_remove:
    :param tree_type:
    :param dataList: 待划分的数据集
    :returns best_feat_idx: 最佳样本分割列
             best_feat_val： 最佳样本分割值
    """
    # 赋初始值
    dataList = np.array(dataList)
    m, n = dataList.shape

    if opt is None:
        opt = {'err_tolerance': 1, 'n_tolerance': 4}
    else:
        err_tolerance, n_tolerance = opt['err_tolerance'], opt['n_tolerance']

    if tree_type == 'regression':
        leaf_faction = leaf_lmTree
        err_faction = err_lmTree
    else:
        # TODO 换成其他树的叶子生成算法，和切割点衡量算法
        leaf_faction = leaf_lmTree
        err_faction = err_lmTree

    best_feat_idx, best_feat_val, best_err = 0, 0, float('inf')
    err = err_faction(dataList)

    # 随机森林部分，随机去掉 num_remove 个特征
    remove_idx = []
    if num_remove != 0:
        while len(remove_idx) < num_remove:
            index = np.random.randint(1, n - 1)
            if index not in remove_idx:
                remove_idx.append(index)

    # 遍历所有特征，如果是随机森林，则随机去掉特征
    for feat_idx in range(1, n):  # 生成从1到9的列表
        if feat_idx not in remove_idx:

            values = dataList[:, feat_idx]
            # 遍历所有特征值
            for val in values:
                # 按照当前特征和特征值分割数据
                left, right = split_data(dataList.tolist(), feat_idx, val)

                if len(left) < n_tolerance or len(right) < n_tolerance:
                    # 如果切分的样本量太小，退出当前循环
                    continue

                # 计算误差
                new_err = err_faction(left) + err_faction(right)
                if new_err < best_err:
                    best_feat_idx = feat_idx
                    best_feat_val = val
                    best_err = new_err
        else:
            continue

    # 如果误差变化并不大归为一类
    if abs(err - best_err) < err_tolerance:
        return None, leaf_faction(dataList)

    # 检查分割样本量是不是太小
    ldata, rdata = split_data(dataList.tolist(), best_feat_idx, best_feat_val)
    if len(ldata) < n_tolerance or len(rdata) < n_tolerance:
        return None, leaf_faction(dataList)

    return best_feat_idx, best_feat_val


def linear_regression(dataList):
    """
    获取线性回归系数
    因变量在第0列，其余为自变量
    :param dataList: 数据集
    :return: w: 回归系数，是一维矩阵
             X: 自变量矩阵
             y: 因变量矩阵
    """
    dataset = np.matrix(dataList)
    # 分割数据并添加常数列
    # X_ori, y = dataset[:, :-1], dataset[:, -1]
    X_ori, y = dataset[:, 1:], dataset[:, 0]
    X_ori, y = np.matrix(X_ori), np.matrix(y)
    # X_ori 少一列，y 只有一列
    m, n = X_ori.shape
    X = np.matrix(np.ones((m, n+1)))
    X[:, 1:] = X_ori

    # 转置矩阵*矩阵
    xTx = X.T * X
    # 如果矩阵的不可逆，会造成程序异常
    if np.linalg.det(xTx) == 0.0:
        raise NameError('This matrix is singular, cannot do inverse,\ntry increasing the second value of opt')
    # 最小二乘法求最优解:  w0*1+w1*x1=y
    w = xTx.I * (X.T * y)

    # print('线性回归：')
    # print(w)
    # print(X.shape)
    # print(X)
    # print(y.shape)
    # print(y)
    return w, X, y


def leaf_lmTree(dataList):
    """
    计算给定数据集的线性回归系数
    :param dataList: 数据集
    :return: 见 def linear_regression
    """
    w, _, _ = linear_regression(dataList)
    return w


def err_lmTree(dataList):
    """
    对给定数据集进行回归并计算误差
    :param dataList: 数据集
    :return: 见 def linear_regression
    """
    w, X, y = linear_regression(dataList)
    y_prime = X*w
    return np.var(y_prime - y)

