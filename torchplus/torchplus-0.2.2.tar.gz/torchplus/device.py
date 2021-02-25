import torch
from pynvml import *


available_gpus = [torch.cuda.device(i) for i in range(torch.cuda.device_count())]

def free_memory_amount(device_number):
    nvmlInit()
    h = nvmlDeviceGetHandleByIndex(device_number)
    info = nvmlDeviceGetMemoryInfo(h)
    return info.free

available_gpus_memory = [free_memory_amount(i) for i in range(torch.cuda.device_count())]

AutoDevice = torch.device("cuda:{}".format(available_gpus_memory.index(max(available_gpus_memory))) if torch.cuda.is_available() else "cpu")

__all__ = ["available_gpus", "AutoDevice"]
