import numpy as np
import random
from functools import reduce    # 图的输出节点的加和

def topologic(graph):  # 得到任意图的拓扑排序序列
    """graph: dict
    {
        x: [linear],
        k: [linear],
        b: [linear],
        linear: [sigmoid],
        sigmoid: [loss],
        y: [loss],
    }
    """

    sorted_node = []  # 定义拓扑排序序列

    while graph:
        all_nodes_have_inputs = reduce(lambda a, b: a + b, list(graph.values()))  # 有输入的节点
        all_nodes_have_outputs = list(graph.keys())  # 有输出的节点
        all_nodes_only_have_outputs_no_inputs = set(all_nodes_have_outputs) - set(
            all_nodes_have_inputs)  # 只有输出无输入的节点

        if all_nodes_only_have_outputs_no_inputs:
            node = random.choice(list(all_nodes_only_have_outputs_no_inputs))  # 随机选取其中的一个

            sorted_node.append(node)
            if len(graph) == 1: sorted_node += graph[node]  # 为了最后一格节点不丢失

            graph.pop(node)
            for _, links in graph.items():
                if node in links: links.remove(node)
        else:
            raise TypeError('this graph has circle, which cannot get topplogical order')

    return sorted_node


class Node:  # 定义节点类结构
    def __init__(self, inputs=[], name=None, is_trainable=False):
        self.inputs = inputs  # 节点的输入的节点
        self.outputs = []  # 节点的输出的节点
        self.name = name  # 为节点命名
        self.value = None  # 节点的值
        self.gradients = dict()  # 存储节点对某个值的偏导
        self.is_trainable = is_trainable  # 参数值是否可训练，x y 不可训练，k b需要训练

        for node in inputs:  # 如果此节点有输入的节点，把此输入的节点的输出节点链接到此节点
            node.outputs.append(self)

    def __repr__(self):  # 重写repr 打印的时候乎打印这个名字  为了能够显示名字，而不是内存
        return 'Node: {}'.format(self.name)

    def forward(self):  # 向前传播
        #         print('I am {}, I have no humam baba, I calculate myself value :  by MYSEL !!!'.format(self.name))
        pass

    def backward(self):
        pass
#         for n in self.inputs:
#             print('get∂{}/∂{}'.format(self.name, n.name))


class Placeholder(Node):  # 定义节点类结构      Placeholder需要传值的参数      输入的节点，可以为，k x b
    def __init__(self, name=None, is_trainable=False):
        Node.__init__(self, name=name, is_trainable=is_trainable)

    def __repr__(self):  # 重写repr 打印的时候乎打印这个名字  为了德银能够显示名字，而不是内存
        return 'Placeholder: {}'.format(self.name)

    def forward(self):
        pass

    #         print('I am {}, I was assigned value:{} by human baba'.format(self.name, self.value))

    def backward(self):
        self.gradients[self] = self.outputs[0].gradients[self]
#         print('i got myself gradients: {}'.format(self.outputs[0].gradients[self]))


class Linear(Node):  # 线性计算的节点，为linear = k * x + b
    def __init__(self, x, k, b, name=None):
        Node.__init__(self, inputs=[x, k, b], name=name)

    def __repr__(self):
        return 'Linear: {}'.format(self.name)

    def forward(self):  # 向前传播得到  为linear = k * x + b
        x, k, b = self.inputs[0], self.inputs[1], self.inputs[2]
        self.value = k.value * x.value + b.value

    #         print('I am {}, I have no humam baba, I calculate myself value : {} by MYSEL !!!'.format(self.name, self.value))

    def backward(self):  # 向后传播，值为上层偏导的值 * 此处的偏导
        x, k, b = self.inputs[0], self.inputs[1], self.inputs[2]
        self.gradients[self.inputs[0]] = self.outputs[0].gradients[self] * k.value
        self.gradients[self.inputs[1]] = self.outputs[0].gradients[self] * x.value
        self.gradients[self.inputs[2]] = self.outputs[0].gradients[self] * 1

#         self.gradients[self.inputs[0]] = '*'.join([self.outputs[0].gradients[self], '∂{}/∂{}'.format(self.name, self.inputs[0].name)])
#         self.gradients[self.inputs[1]] = '*'.join([self.outputs[0].gradients[self], '∂{}/∂{}'.format(self.name, self.inputs[1].name)])
#         self.gradients[self.inputs[2]] = '*'.join([self.outputs[0].gradients[self], '∂{}/∂{}'.format(self.name, self.inputs[2].name)])
#         print('self.gradients[self.inputs[0]]|{}'.format(self.gradients[self.inputs[0]]))
#         print('self.gradients[self.inputs[1]]|{}'.format(self.gradients[self.inputs[1]]))
#         print('self.gradients[self.inputs[2]]|{}'.format(self.gradients[self.inputs[2]]))


class Sigmoid(Node):  # sigmoid节点，接收来自linear节点的值，经Sigmoid函数后输出值
    def __init__(self, x, name=None):
        Node.__init__(self, inputs=[x], name=name)

    def __repr__(self):
        return 'Sigmoid: {}'.format(self.name)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self):  # 向前传播，输出节点经Sigmoid函数后输出值
        x = self.inputs[0]
        self.value = self._sigmoid(x.value)

    #         print('I am {}, I have no humam baba, I calculate myself value : {} by MYSEL !!!'.format(self.name, self.value))

    def backward(self):  # 向后传播，为上层节点loss对sigmoid的偏导 * 其对输入x的偏导
        x = self.inputs[0]
        self.gradients[self.inputs[0]] = self.outputs[0].gradients[self] * (
                    self._sigmoid(x.value) * (1 - self._sigmoid(x.value)))

#         self.gradients[self.inputs[0]] = '*'.join([self.outputs[0].gradients[self], '∂{}/∂{}'.format(self.name, self.inputs[0].name)])
#         print('self.gradients[self.inputs[0]]|{}'.format(self.gradients[self.inputs[0]]))


class Loss(Node):  # 损失函数
    def __init__(self, y, yhat, name=None):
        Node.__init__(self, inputs=[y, yhat], name=name)

    def __repr__(self):
        return 'Loss: {}'.format(self.name)

    def forward(self):  # 向前传播输出既定y值与计算的y值的差，即损失
        y = self.inputs[0]
        yhat = self.inputs[1]
        self.value = np.mean((y.value - yhat.value) ** 2)

    #         print('I am {}, I have no humam baba, I calculate myself value : {} by MYSEL !!!'.format(self.name, self.value))

    def backward(self):  # 向后传播，计算节点loss对 y 与yhat的偏导值
        y = self.inputs[0]
        yhat = self.inputs[1]
        self.gradients[self.inputs[0]] = 2 * np.mean(y.value - yhat.value)  # 计算偏导值
        self.gradients[self.inputs[1]] = -2 * np.mean(y.value - yhat.value)  # 计算偏导值

#         self.gradients[self.inputs[0]] = '∂{}/∂{}'.format(self.name, self.inputs[0].name)
#         self.gradients[self.inputs[1]] = '∂{}/∂{}'.format(self.name, self.inputs[1].name)
#         print('self.gradients[self.inputs[0]]|.{}'.format(self.gradients[self.inputs[0]]))
#         print('self.gradients[self.inputs[1]]|.{}'.format(self.gradients[self.inputs[1]]))

