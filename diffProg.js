class ExprConst {
  constructor(c) { this.c = c; }
  forwardProp(exprs) { this.val = this.c; } 
  backProp(exprs) {}
}

class ExprMul {
  constructor(i1, i2) { this.i1 = i1; this.i2 = i2; }
  forwardProp(exprs) {
    this.val = exprs[this.i1].val * exprs[this.i2].val;
  }
  backProp(exprs) {
    exprs[this.i1].der += exprs[this.i2].val * this.der;
    exprs[this.i2].der += exprs[this.i1].val * this.der;
  }
}

class ExprAdd {
  constructor(is) { this.is = is; }
  forwardProp(exprs) {
    this.val = 0;
    for (let i of this.is) this.val += exprs[i].val;
  }
  backProp(exprs) {
    for (let i of this.is) exprs[i].der = this.der;
  }
}

class ExprReLU {
  constructor(i) { this.i = i; }
  forwardProp(exprs) {
    this.val = exprs[this.i];
    if (this.val < 0) this.val = 0;
  }
  backProp(exprs) {
    exprs[this.i].der += this.val < 0 ? 0 : this.der;
  }
}

class Prog {
  constructor(exprs) {
    this.exprs = exprs;
  }

  forwardProp() {
    const exprs = this.exprs;
    for (let i in exprs) exprs[i].forwardProp(exprs);
  }
  
  backProp() {
    const exprs = this.exprs;
    for (let i in exprs) exprs[i].der = 0;
    exprs[exprs.length-1].der = 1;
    for (let i = exprs.length-1; i >= 0; i--)
      exprs[i].backProp(exprs);
  }
}

function step(prog, weightIndexes, learningRate) {
  prog.forwardProp();
  prog.backProp();
  for (let i of weightIndexes) {
    prog.exprs[i].c -= learningRate * prog.exprs[i].der;
  }
}

function minimize(prog, weightIndexes, learningRate) {
  for (let i = 0; i < 1000; i++) {
    step(prog, weightIndexes, learningRate);
  }
}

function setTrainingExample(prog, trainingIndexes, trainingExample) {
  for (let i = 0; i < trainingIndexes.length; i++) {
    prog.exprs[trainingIndexes[i]].c = trainingExample[i];
  }
}

function stochasticGradientDescent(prog, weightIndexes, learningRate, trainingIndexes, trainingExamples) {
  for (let i = 0; i < 1000; i++) {
    for (let trainingExample of trainingExamples) {
      setTrainingExample(prog, trainingIndexes, trainingExample);
      step(prog, weightIndexes, learningRate);
    }
  }
}

// (w-2)^2
// const exampleProg = new Prog([
//   new ExprConst(5),
//   new ExprConst(2),
//   new ExprConst(-1),
//   new ExprMul(1, 2),
//   new ExprAdd([0, 3]),
//   new ExprMul(4,4)
// ]);

// minimize(exampleProg, [0], 0.01);

// console.log(exampleProg);

const linearProg = new Prog([
  new ExprConst(5),   // [0] x
  new ExprConst(45),   // [1] w
  new ExprMul(0, 1),  // [2] wx (actual)
  new ExprConst(10),  // [3] expected
  new ExprConst(-1),  // [4]
  new ExprMul(3, 4),  // [5] -expected
  new ExprAdd([2,5]), // [6] actual-expected
  new ExprMul(6,6),   // [7] (actual-expected)^2
]);

// minimize(linearProg, [1], 0.01);

// find the slope 3 of a line
stochasticGradientDescent(linearProg, [1], 0.01, [0, 3], [
  [0,0],
  [1,3],
  [2,6],
  [3,9],
]);

console.log(linearProg);