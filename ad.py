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
  def __truediv__(self, b):
    return self * reciprocal(b)
  
  def __radd__(self, a):
    return ExprAdd([const(a), self])
  def __rsub__(self, a):
    return a + (-self)
  def __rmul__(self, a):
    return ExprMul([const(a), self])
  def __rtruediv__(self, a):
    return a * reciprocal(self)

  def __lt__(self, b):
    if isinstance(b,Expr):
      return self.val < b.val
    return self.val < b

def const(v):
  if type(v) is int or type(v) is float:
    return ExprConst(v)
  else:
    return v

def add(a,b):
  if isinstance(b, Expr):
    return b+a
  return a+b
def mul(a,b):
  if isinstance(b, Expr):
    return b*a
  return a*b
def sub(a,b):
  if isinstance(b, Expr):
    return (-b)+a
  return a-b
def reciprocal(a):
  if isinstance(a, Expr):
    return ExprReciprocal([a])
  if a == 0:
    return float("inf")
  return 1/a

def eq(a,b):
  if isinstance(a, Expr):
    a = a.val
  if isinstance(b, Expr):
    b = b.val
  return a == b

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
    self.deps[0].der = sub(self.deps[0].der, self.der)
class ExprAdd(Expr):
  def __init__(self,deps):
    super().__init__(deps)
    self.val = add(self.deps[0].val, self.deps[1].val)
  def backprop(self):
    self.deps[0].der = add(self.deps[0].der, self.der)
    self.deps[1].der = add(self.deps[1].der, self.der)
class ExprMul(Expr):
  def __init__(self,deps):
    super().__init__(deps)
    self.val = mul(self.deps[0].val, self.deps[1].val)
  def backprop(self):
    self.deps[0].der = add(mul(self.deps[1].val, self.der), self.deps[0].der)
    self.deps[1].der = add(mul(self.deps[0].val, self.der), self.deps[1].der)
class ExprReciprocal(Expr):
  def __init__(self,deps):
    super().__init__(deps)
    self.val = reciprocal(self.deps[0].val)
  def backprop(self):
    self.deps[0].der = add(self.deps[0].der, 
      mul(self.der,
        -reciprocal(mul(self.deps[0].val,self.deps[0].val))))

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

# Differentiate a function.
# Input function can take any number of input numbers,
# and must return a single number.
# Returns a new function that
# accepts arguments in the same form,
# and returns an array of the derivatives of each argument
# with respect to the single output number.
def diff(f):
  def derivative(*args):
    input_exprs = list(map(ExprConst, args))
    output_expr = const(f(*input_exprs))
    backprop(output_expr)
    return list(map((lambda e: e.der), input_exprs))
  return derivative

# Special-case of the above, for functions that accept a single number.
# In this case, the derivative function returns the single derivative,
# instead of an array of one derivative.
def diff_single(f):
  return lambda x: diff(f)(x)[0]
