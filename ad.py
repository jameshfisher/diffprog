class Expr:
  def __init__(self, deps):
    self.der = 0
    self.deps = deps
    self.height = max(map((lambda d: d.height), deps)) + 1
  def __neg__(self):
    return ExprNeg([self])
  def __add__(self, b):
    return ExprAdd([self, const(b)])
  def __sub__(self, b):
    return self + (-b)
  def __mul__(self, b):
    return ExprMul([self, const(b)])

def const(v):
  if type(v) is int or type(v) is float:
    return ExprConst(v)
  else:
    return v

class ExprConst(Expr):
  def __init__(self, val):
    self.der = 0
    self.deps = []
    self.height = 0
    self.val = val
  def backprop(self):
    pass
class ExprNeg(Expr):
  def __init__(self, deps):
    super().__init__(deps)
    self.val = -self.deps[0].val
  def backprop(self):
    self.deps[0].der = self.deps[0].der - self.der
class ExprAdd(Expr):
  def __init__(self,deps):
    super().__init__(deps)
    self.val = self.deps[0].val + self.deps[1].val
  def backprop(self):
    self.deps[0].der = self.deps[0].der + self.der
    self.deps[1].der = self.deps[1].der + self.der
class ExprMul(Expr):
  def __init__(self,deps):
    super().__init__(deps)
    self.val = self.deps[0].val * self.deps[1].val
  def backprop(self):
    self.deps[0].der = (self.deps[1].val * self.der) + self.deps[0].der
    self.deps[1].der = (self.deps[0].val * self.der) + self.deps[1].der

def backprop(root):
  exprs = set()
  todo = set([root])
  while todo:
    e = todo.pop()
    for d in e.deps:
      todo.add(d)
    exprs.add(e)

  root.der = 1
  for e in sorted(exprs, key=(lambda e: e.height), reverse=True):
    e.backprop()

def diff(f):
  def derivative(*args):
    input_exprs = list(map(ExprConst, args))
    output_expr = const(f(*input_exprs))
    backprop(output_expr)
    return list(map((lambda e: e.der), input_exprs))
  return derivative

def square(x):
  return x*x
def f(a):
  return square(a-2)

square_der = diff(square)
print(square_der(-2))
print(square_der(0))
print(square_der(2))
print(square_der(4))

square_der_der = diff(lambda x: square_der(x)[0])
print(square_der_der(-2))
print(square_der_der(0))
print(square_der_der(2))
print(square_der_der(4))

square_der_der_der = diff(lambda x: square_der_der(x)[0])
print(square_der_der_der(-2))
print(square_der_der_der(0))
print(square_der_der_der(2))
print(square_der_der_der(4))