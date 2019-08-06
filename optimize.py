import ad
def gradient_descent(f, params, learning_rate=0.01):
  f_der = ad.diff(f)
  for i in range(0, 100):
    grads = f_der(*params)
    for i in range(0, len(params)):
      params[i] = params[i] - learning_rate * grads[i]
  return params