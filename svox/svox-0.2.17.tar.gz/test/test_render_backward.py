import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt

device = 'cuda:0'

t = svox.N3Tree(map_location=device)
t[0, :3] = 0.0
t[0, -1] = 0.0
r = svox.VolumeRenderer(t)
#  sqrt_2 = 2 ** -0.5

#  ray_ori = torch.tensor([[0.1, 0.1, -0.1],
#                          [0.9, 0.9, -0.1]], device=device)
#  ray_dir = torch.tensor([[0.0, 0.0, 1.0],
#                          [0.0, 0.0, 1.0]], device=device)

target =  torch.tensor([[0.0, 1.0, 0.5]], device=device)

ray_ori = torch.tensor([[0.1, 0.1, -0.1]], device=device)
ray_dir = torch.tensor([[0.0, 0.0, 1.0]], device=device)
ray = {
    "origins": ray_ori,
    "dirs": ray_dir,
    "viewdirs": ray_dir,
}
for i in range(50):
    rend = r(ray, cuda=True)
    print(rend, rend.requires_grad)
    #  rend.retain_grad()
    torch.abs(rend - target).sum().backward()
    #  print('rend grad', rend.grad)
    #  print('data grad', t.data.grad)
    print('data', t.data)

    t.data.data -= t.data.grad
    t.zero_grad()

#  c2w = torch.tensor([[1.0, 0.0, 0.0,  0.0],
#                      [0.0, 1.0, 0.0,  0.0],
#                      [0.0,  0.0, 1.0, 0.0]], device=device)
#
#
#
#  start = torch.cuda.Event(enable_timing=True)
#  end = torch.cuda.Event(enable_timing=True)
#  im = None
#
#  start.record()
#  im = r.render_persp(c2w, height=400, width=400, fx=300)
#  end.record()
#
#  torch.cuda.synchronize(device)
#  dur = start.elapsed_time(end)
#  print('render time', dur, 'ms =', 1000 / dur, 'fps')
#  print(im.shape)
#
#  im = im.detach().clamp_(0.0, 1.0)
#  plt.figure()
#  plt.imshow(im.cpu())
#  plt.show()
