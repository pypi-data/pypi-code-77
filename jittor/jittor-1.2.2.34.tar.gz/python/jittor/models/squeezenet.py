# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers: 
#     Wenyang Zhou <576825820@qq.com>
#     Dun Liang <randonlang@gmail.com>. 
# 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
# This model is generated by pytorch converter.
import jittor as jt
from jittor import nn
__all__ = ['SqueezeNet', 'squeezenet1_0', 'squeezenet1_1']

class Fire(nn.Module):

    def __init__(self, inplanes, squeeze_planes, expand1x1_planes, expand3x3_planes):
        super(Fire, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.Relu()
        self.expand1x1 = nn.Conv(squeeze_planes, expand1x1_planes, kernel_size=1)
        self.expand1x1_activation = nn.Relu()
        self.expand3x3 = nn.Conv(squeeze_planes, expand3x3_planes, kernel_size=3, padding=1)
        self.expand3x3_activation = nn.Relu()

    def execute(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return jt.contrib.concat([self.expand1x1_activation(self.expand1x1(x)), self.expand3x3_activation(self.expand3x3(x))], dim=1)

class SqueezeNet(nn.Module):

    def __init__(self, version='1_0', num_classes=1000):
        super(SqueezeNet, self).__init__()
        self.num_classes = num_classes
        if (version == '1_0'):
            self.features = nn.Sequential(
                nn.Conv(3, 96, kernel_size=7, stride=2), 
                nn.Relu(), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(96, 16, 64, 64), 
                Fire(128, 16, 64, 64), 
                Fire(128, 32, 128, 128), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(256, 32, 128, 128), 
                Fire(256, 48, 192, 192), 
                Fire(384, 48, 192, 192), 
                Fire(384, 64, 256, 256), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(512, 64, 256, 256)
            )
        elif (version == '1_1'):
            self.features = nn.Sequential(
                nn.Conv(3, 64, kernel_size=3, stride=2), 
                nn.Relu(), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(64, 16, 64, 64), 
                Fire(128, 16, 64, 64), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(128, 32, 128, 128), 
                Fire(256, 32, 128, 128), 
                nn.Pool(kernel_size=3, stride=2, ceil_mode=True, op='maximum'), 
                Fire(256, 48, 192, 192), 
                Fire(384, 48, 192, 192), 
                Fire(384, 64, 256, 256), 
                Fire(512, 64, 256, 256)
            )
        else:
            raise ValueError('Unsupported SqueezeNet version {version}:1_0 or 1_1 expected'.format(version=version))
        final_conv = nn.Conv(512, self.num_classes, kernel_size=1)
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5), 
            final_conv, 
            nn.Relu(), 
            nn.AdaptiveAvgPool2d((1, 1))
        )

    def execute(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return jt.reshape(x, (x.shape[0], (- 1)))

def _squeezenet(version, **kwargs):
    model = SqueezeNet(version, **kwargs)
    return model

def squeezenet1_0(pretrained=False, **kwargs):
    model = _squeezenet('1_0', **kwargs)
    if pretrained: model.load("jittorhub://squeezenet1_0.pkl")
    return model

def squeezenet1_1(pretrained=False, **kwargs):
    model = _squeezenet('1_1', **kwargs)
    if pretrained: model.load("jittorhub://squeezenet1_1.pkl")
    return model
