import ad
import matplotlib.pyplot as plt

def square(x):
  return x*x
def cube(x):
  return x*x*x
def f(a):
  return (cube(a) - square(a-2)*4 + 2) / 10

def recip(x):
  return ad.reciprocal(x)

def relu(x):
  if x < 0:
    return 0
  return x

square_ = ad.diff_single(square)
square__ = ad.diff_single(square_)
square___ = ad.diff_single(square__)

x = [-5+x*0.01 for x in range(1000)]

def plot(f, derivatives=4):
  plot_data = { 'x': x }
  for i in range(0,derivatives):
    g = f
    for j in range(0,i):
      g = ad.diff_single(g)
    plot_data['f'+('_'*i)] = list(map(g, x))
  for i in range(0,derivatives):
    plt.plot ('x', 'f'+('_'*i), data=plot_data)
  plt.legend()
  plt.show()

plot(cube, derivatives=3)
