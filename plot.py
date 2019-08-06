import ad
import matplotlib.pyplot as plt
import examples

x = [-1.3+x*0.01 for x in range(260)]

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

plot(examples.k, derivatives=2)
