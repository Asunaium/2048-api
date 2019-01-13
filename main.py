from game2048.agents import Agent
import numpy as np
import theano
import theano.tensor as T
import lasagne
from lasagne.layers import DenseLayer
floatX = theano.config.floatX
OUT_SHAPE = (4, 4)
CAND = 16
map_table = {2 ** i: i for i in range(1, 16)}
map_table[0] = 0
r_table = {0: 0, 1: 3, 2: 2, 3: 1}
table = {2 ** (i + 1): i for i in range(20)}

input_var = T.tensor4()
target_var = T.ivector()
_ = lasagne.layers.InputLayer(shape=(None, 4, 4, 20), input_var=input_var)
_ = DenseLayer(_, num_units=900, nonlinearity=lasagne.nonlinearities.rectify)
_ = DenseLayer(_, num_units=300, nonlinearity=lasagne.nonlinearities.rectify)
_ = DenseLayer(_, num_units=200, nonlinearity=lasagne.nonlinearities.rectify)
l_out = DenseLayer(_, num_units=4, nonlinearity=lasagne.nonlinearities.softmax)
prediction = lasagne.layers.get_output(l_out)
P = theano.function([input_var], prediction)



with np.load('model.npz') as f:
    param_values = [f['arr_%d' % i] for i in range(len(f.files))]
lasagne.layers.set_all_param_values(l_out, param_values)


def grid_ohe(arr):
    ret = np.zeros(shape=OUT_SHAPE + (CAND,), dtype=bool)
    for r in range(4):
        for c in range(4):
            ret[r, c, map_table[arr[r, c]]] = 1

    return ret

table ={2**(i+1):i for i in range(20)}

def make_input(grid, d=0):
    g0 = np.rot90(grid, -d)
    r = np.zeros(shape=(4, 4, 20), dtype=floatX)
    for i in range(4):
        for j in range(4):
            v = g0[i, j]
            if v:
                r[i, j][table[v]] = 1
    return r

class YourOwnAgent(Agent):


    def step(self):
        board = np.array([make_input(self.game.board)], dtype=floatX)
        move=np.argsort(P(board)[0])[::-1][0]
        mov=r_table[move]



        direction = mov
        return direction