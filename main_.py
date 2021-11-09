import numpy as np
import matplotlib.pyplot as plt
import math
import struct

from sklearn.utils.extmath import softmax


class Neural_Network(object):
    # initialize neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        """
        :param inputnodes: 输入层结点数
        :param hiddennodes: 隐藏层结点数
        :param outputnodes: 输出层结点数
        :param learningrate: 学习率
        """
        self.inputnodes = inputnodes
        self.hiddennodes = hiddennodes
        self.outputnodes = outputnodes
        self.learningrate = learningrate
        # 输入层与隐藏层权重矩阵初始化
        self.w1 = np.random.randn(self.hiddennodes, self.inputnodes) * 0.01
        # 隐藏层与输出层权重矩阵初始化
        self.w2 = np.random.randn(self.outputnodes, self.hiddennodes) * 0.01
        # 构建第一层常量矩阵100 by 1 matrix
        self.b1 = np.zeros((200, 1))
        # 构建第二层常量矩阵 10 by 1 matrix
        self.b2 = np.zeros((10, 1))
        # 定义迭代次数
        self.epoch = 5

    # 激活函数
    def sigmoid(self, x):
        """
        :param x: 输入数据
        :return:返回softmax激活函数值
        """
        from scipy import special
        #logistic sigmoid
        return special.expit(x)
    # def softmax(self,x):
    #     """Compute softmax values for each sets of scores in x."""
    #     e_x = np.exp(x - np.max(x))
    #     return e_x / e_x.sum(axis=0) # only difference

    def tanh(self, x):
        """
        :param x: 输入数据
        :return: 返回tanh激活函数值
        """
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    # 定义损失函数
    # def loss_function(self, origin_label, fp_result):
    #     return -origin_label * (math.log2(fp_result)) - (1 - origin_label) * (
    #         math.log2(1 - fp_result))

    # 前向传播
    def forward_propagation(self, input_data, weight_matrix, b):
        """

        :param input_data: 输入数据
        :param weight_matrix: 权重矩阵
        :return: 激活函数后输出的活性值
        """
        z = np.add(np.dot(weight_matrix, input_data), b)
        return z, self.sigmoid(z)

    # 反向传播
    def back_propagation(self, a, z, da, weight_matrix, b):
        dz = da * (z * (1 - z))
        weight_matrix -= self.learningrate * np.dot(dz, a.T) / 60000
        b -= self.learningrate * np.sum(dz, axis=1, keepdims=True) / 60000
        da_n = np.dot(weight_matrix.T, da)
        return da_n

    # 训练模型
    def train(self, input_data, label_data):
        for item in range(self.epoch):
            print('Executing %dth epoch' % item)
            for i in range(60000):
                # forward propagation
                z1, a1 = self.forward_propagation(
                    input_data[:, i].reshape(-1, 1), self.w1, self.b1)
                z2, a2 = self.forward_propagation(a1, self.w2, self.b2)
                # calculate da[2]
                dz2 = a2 - label_data[:, i].reshape(-1, 1)
                dz1 = np.dot(self.w2.T, dz2) * a1 * (1.0 - a1)
                # back propagation
                self.w2 -= self.learningrate * np.dot(dz2, a1.T)
                self.b2 -= self.learningrate * dz2

                self.w1 -= self.learningrate * np.dot(
                    dz1, (input_data[:, i].reshape(-1, 1)).T)
                self.b1 -= self.learningrate * dz1
    #alternative solution
    def train_vector(self, train_data, train_label):
        for item in range(self.epoch):
            print('executing the %dth epoch' % item)
            # forward prop
            z1, a1 = self.forward_propagation(train_data, self.w1, self.b1)
            z2, a2 = self.forward_propagation(a1, self.w2, self.b2)
            dz2 = a2 - train_label
            dz1 = np.dot(self.w2.T, dz2) * a1 * (1 - a1)
            # back prop
            self.w2 -= self.learningrate * np.dot(dz2, a1.T) / 60000
            self.b2 -= self.learningrate * np.sum(dz2, axis=1,
                                                  keepdims=True) / 60000
            self.w1 -= self.learningrate * np.dot(dz1, train_data.T) / 60000
            self.b1 -= self.learningrate * np.sum(dz1, axis=1,
                                                  keepdims=True) / 60000

    # predict
    def predict(self, input_data, label):
        precision = 0
        for i in range(10000):
            z1, a1 = self.forward_propagation(input_data[:, i].reshape(-1, 1),
                                              self.w1, self.b1)
            z2, a2 = self.forward_propagation(a1, self.w2, self.b2)
            print(a2)
            print('This model\'s predicted value:{0},\nactual value:{1}'.format(np.argmax(a2), label[i]))
            if np.argmax(a2) == label[i]:
                precision += 1
        print('Overall accuracy rate：{0}%'.format(precision * 100 / 10000))

    # 向量训练的预测结果
    def predict_vector(self, input_data, label):
        z1, a1 = self.forward_propagation(input_data, self.w1, self.b1)
        z2, a2 = self.forward_propagation(a1, self.w2, self.b2)
        precision = 0
        for item in range(10000):
            if np.argmax(a2[:, item]) == label[item]:
                precision += 1



# read original data and preprocess it
def data_fetch_preprocessing():
    train_image = open('train-images.idx3-ubyte', 'rb')
    test_image = open('t10k-images.idx3-ubyte', 'rb')
    train_label = open('train-labels.idx1-ubyte', 'rb')
    test_label = open('t10k-labels.idx1-ubyte', 'rb')

    magic, n = struct.unpack('>II', train_label.read(8))
    # original data's lable
    y_train_label = np.array(np.fromfile(train_label, dtype=np.uint8), ndmin=1)
    y_train = np.ones((10, 60000)) * 0.01
    for i in range(60000):
        y_train[y_train_label[i]][i] = 0.99

    # test data's label
    magic_t, n_t = struct.unpack('>II', test_label.read(8))
    y_test = np.fromfile(test_label, dtype=np.uint8).reshape(10000, 1)
    # print(y_train[0])
    # train data quantity: 60,000
    # print(len(labels))
    magic, num, rows, cols = struct.unpack('>IIII', train_image.read(16))
    x_train = np.fromfile(train_image,
                          dtype=np.uint8).reshape(len(y_train_label), 784).T

    magic_2, num_2, rows_2, cols_2 = struct.unpack('>IIII',
                                                   test_image.read(16))
    x_test = np.fromfile(test_image, dtype=np.uint8).reshape(len(y_test),
                                                             784).T

    #

    x_train = x_train / 255 * 0.99 + 0.01
    x_test = x_test / 255 * 0.99 + 0.01

    # 关闭打开的文件
    train_image.close()
    train_label.close()
    test_image.close()
    test_label.close()

    return x_train, y_train, x_test, y_test


if __name__ == '__main__':

    # input layer: 784, hidden layer: 200, output:10, learning rate:0.1
    dl = Neural_Network(784, 200, 10, 0.1)
    x_train, y_train, x_test, y_test = data_fetch_preprocessing()

    ##
    # print(x_train.shape)
    # # 可以通过这个函数观察图像
    # data = x_train[:, 0].reshape(28, 28)
    # plt.imshow(data, cmap='Greys', interpolation=None)
    # plt.show()
    # 循环训练方法
    dl.train(x_train, y_train)
    # 向量化训练方法

    # 预测模型
    dl.predict(x_test, y_test)
    # dl.train_vector(x_train,y_train)
    # dl.predict_vector(x_test,y_test)
