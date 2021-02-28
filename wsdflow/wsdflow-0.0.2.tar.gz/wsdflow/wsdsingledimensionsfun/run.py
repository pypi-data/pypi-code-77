import numpy as np
from wsdflow.wsdsingledimensionsfun.fun import sum

# 例子
y = 0.8
x = 6
num = 200
k_b_loss_history = sum(y, x, num)


def sigmoid(x):                 # 计算查看验证 y 与 yhat的值是否一致  由于每次的拓扑排序，y k b x 顺序不一样，需要依据上面顺序修改下面代码
    return 1 / ( 1 + np.exp(-x))
for index, loss in enumerate(k_b_loss_history[0]):
    # print('第{}次的k：{}、b：{}、loss：{}'.format(index, k_b_loss_history[0][index],
    #                                       k_b_loss_history[1][index], k_b_loss_history[2][index]))
    yhat = sigmoid(k_b_loss_history[0][index] * x + k_b_loss_history[1][index])  # 手动计算y值
    print(y,yhat,k_b_loss_history[-1][index])