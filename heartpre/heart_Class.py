# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import tensorflow.contrib.eager as tfe

tf.compat.v1.enable_eager_execution()

trainPath = "./data/heart_training.csv"
testPath = "./data/heart_test.csv"


def parse_csv(line):
    # 设置特征和标签的数据接收格式 （自己设置的函数）
    featlab_types = [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0]]
    # 解析csv数据，以featlab_types的格式接收
    parsed_line = tf.io.decode_csv(line, featlab_types)
    # 提取出特征数据，并转化成张量
    features = tf.reshape(parsed_line[:-1], shape=(13,))
    # 提取出标签数据，并转化成张量
    label = tf.reshape(parsed_line[-1], shape=())
    return features, label


def getFeaturesLables(dataPath):
    # 使用TextLineDataset 读取文件内容
    FeatLabs = tf.data.TextLineDataset(trainPath)
    # 跳过第一行，因为第一行是所有数据内容的总结，不能用于训练或测试
    # FeatLabs = FeatLabs.skip(1)
    # 把每一行数据按照parse_csv的格式报错
    FeatLabs = FeatLabs.map(parse_csv)
    # 打乱数据原来的存放位置，
    FeatLabs = FeatLabs.shuffle(buffer_size=100)
    # 以float32的格式保存数据
    FeatLabs = FeatLabs.batch(32)
    return FeatLabs


def readCategory():
    categories = ['无心脏病', '一级心脏病', '二级心脏病', '三级心脏病', '四级心脏病']
    cat_to_id = dict(zip(categories, range(len(categories))))
    return categories, cat_to_id


class NNetConfig():
    num_classes = 5  # 多分类的种类
    num_epochs = 100  # 训练总批次
    print_per_epoch = 10  # 每训练多少批次时打印训练损失函数值和预测准确率值
    layersls = [13, 20, 20, 20, 20, 20, 5]  # 【输入，隐藏各层节点数，输出】
    learning_rate = 0.01  # 网络学习率
    train_filename = 'data/heart_training.csv'  # 训练数据
    test_filename = 'data/heart_test.csv'  # 测试数据
    best_model_savepath = "heartpre/dnn/best_validation"  # 最好模型的存放文件夹


def heart_prediction(cat, config_other, features=[]):
    # 预测函数
    # 加载已经训练好的最优模型（包括网络结构及网络权值矩阵）
    # compile=False 表示对此模型，我只用不再次训练
    model = tf.keras.models.load_model(
        os.path.join(config_other.best_model_savepath, "model_best.h5"),
        compile=False)
    # 当预测特征为空时，使用下面给出的默认值进行预测
    if len(features) == 0:
        print("預測值為空")
        return 0;
    else:
        # 预测特征数据转换成张量
        predFeats = tf.convert_to_tensor(features)
    # 预测结果存放列表
    cat_probs = []
    # 使用已训练模型预测的预测结果，是张量
    y_probs = model(predFeats)
    # 取出每条预测结果进行处理，取出其中最大值，即最可能的结果，
    # 根据最大值所在下标，取到cat可读文本
    for prob in y_probs:
        top1 = tf.argmax(prob).numpy()
        cat_probs.append(cat[top1])
    return cat_probs
