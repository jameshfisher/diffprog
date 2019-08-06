import ad

def square(x):
  return x*x
def cube(x):
  return x*x*x
def pow5(x):
  return x * x * x * x * x
def f(a):
  return (cube(a) - square(a-2)*4 + 2) / 10
def k(x):
  return x * 2 * pow5(square(x) - 1)

def recip(x):
  return ad.reciprocal(x)

def relu(x):
  if x < 0:
    return 0
  return x

training_data = [
  ([3], 11.9),
  ([2], 8.2),
  ([-2], -3),
  ([0], 2.1),
]

def linear_model(slope, intercept, input):
  return slope*input + intercept

# def line_error(slope, intercept):
#   err = 0
#   for (inputs,target) in training_data:
#     prediction = 
#     err = err + square(target-prediction)
#   return err
