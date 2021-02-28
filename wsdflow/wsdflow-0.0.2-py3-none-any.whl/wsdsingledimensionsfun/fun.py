from wsdflow.wsdsingledimensionscore.core import *


from collections import defaultdict  # 为了定义一种defaultdict(list)数据结构
def convert_feed_dict_to_graph(feed_dict):  # 得到节点类型的图结构
    need_expand = [n for n in feed_dict]

    computing_graph = defaultdict(list)  # 定义一种defaultdict(list)数据结构

    while need_expand:
        n = need_expand.pop(0)
        if n in computing_graph:
            continue

        if isinstance(n, Placeholder):
            n.value = feed_dict[n]

        for m in n.outputs:
            computing_graph[n].append(m)
            need_expand.append(m)

    return computing_graph

## Feedforward
def forward(graph_sorted_nodes):  # 所有节点的一次正向传播
    for node in graph_sorted_nodes:
        node.forward()
        if isinstance(node, Loss):
            pass
            # print('loss value: {}'.format(node.value))

# Backward Propogation
def backward(graph_sorted_nodes):  # 所有节点的一次反向传播  求解每个节点对输入的的偏导值
    for node in graph_sorted_nodes[::-1]:
        #         print('\nI am: {}'.format(node.name))
        node.backward()

def run_one_epoch(graph_sorted_nodes):  # 正向，反向一次 合在一起
    forward(graph_sorted_nodes)
    backward(graph_sorted_nodes)

# optimize
def optimize(graph_nodes, learning_rate=1e-3):  # 优化 一次轮回传播之后，优化参数，k b
    for node in graph_nodes:
        if node.is_trainable:
            node.value = node.value + -1 * node.gradients[node] * learning_rate
            cmp = 'large' if node.gradients[node] > 0 else 'small'
#             print("{}'value is too {}, I need update myself to {}".format(node.name, cmp, node.value))


## Our Simple Model Elements
#version-05
node_x = Placeholder(name='x')
node_y = Placeholder(name='y')
node_k = Placeholder(name='k', is_trainable=True)         # is_trainable 可以训练更新
node_b = Placeholder(name='b', is_trainable=True)
node_linear = Linear(node_x, node_k, node_b, name='linear')
node_sigmoid = Sigmoid(x=node_linear, name='sigmoid')
node_loss = Loss(yhat=node_sigmoid, y=node_y, name='loss')

def intergration(sorted_nodes, num):
    loss_history = []  # 记录所有损失值
    k_history = []
    b_history = []
    for _ in range(num):  # 更新计算的次数
        for node in sorted_nodes:
            if node.name == 'k':
                k_history.append(node.value)
            if node.name == 'b':
                b_history.append(node.value)

        run_one_epoch(sorted_nodes)  # 来回传播一次
        __loss_node = sorted_nodes[-1]
        assert isinstance(__loss_node, Loss)
        loss_history.append(__loss_node.value)

        optimize(sorted_nodes, learning_rate=1e-1)  # 更新参数k b
    return [k_history, b_history, loss_history]

def sum(y, x, num):
    feed_dict = {  # 定义初始化需要传值的参数
        node_x: x,
        node_y: y,
        node_k: random.random(),
        node_b: random.random()
    }
    sorted_nodes = topologic(convert_feed_dict_to_graph(feed_dict))  # 得到经过拓扑排序的节点序列
    k_b_loss_history = intergration(sorted_nodes, num)
    return(k_b_loss_history)



# 例子
# y = [1,2,3]
# x = [4,5,8]
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
