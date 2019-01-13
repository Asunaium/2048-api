import numpy as np
OUT_SHAPE=(4,4)
CAND=16
map_table={2**i :i for i in range(1,16)}
map_table[0]=0
direction_tabel={0: [1, 0, 0, 0], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0], 3: [0, 0, 0, 1]}
TRAINDATA=[]
TRAINLABEL=[]
def grid_ohe(arr):
    ret= np.zeros(shape =OUT_SHAPE+(CAND,),dtype=bool)
    for r in range(4):
        for c in range(4):
            ret[r,c,map_table[arr[r,c]]]=1

    return ret

class Agent:
    '''Agent Base.'''

    def __init__(self, game, display=None,trainData =[],trainLabel=[]):
        self.game = game
        self.display = display
        self.trainData = trainData
        self.trainLabel =trainLabel

    def play(self, max_iter=np.inf, verbose=False):
        n_iter = 0
        while (n_iter < max_iter) and (not self.game.end):
            direction = self.step()
            print(self.game.board)
            self.trainData.append(grid_ohe(self.game.board))
            self.trainLabel.append(direction_tabel[direction])
            TRAINDATA.append(grid_ohe(self.game.board))
            TRAINLABEL.append(direction_tabel[direction])
            self.game.move(direction)
            n_iter += 1
            if verbose:
                print("Iter: {}".format(n_iter))
                print("======Direction: {}======".format(
                    ["left", "down", "right", "up"][direction]))

                if self.display is not None:
                    self.display.display(self.game)


        '''np.save("trainData.npy", self.trainData)
        np.save("trainLabel.npy", self.trainLabel)'''

    def step(self):
        direction = int(input("0: left, 1: down, 2: right, 3: up = ")) % 4
        return direction


class RandomAgent(Agent):

    def step(self):
        direction = np.random.randint(0, 4)
        return direction


class ExpectiMaxAgent(Agent):

    def __init__(self, game, display=None):
        if game.size != 4:
            raise ValueError(
                "`%s` can only work with game of `size` 4." % self.__class__.__name__)
        super().__init__(game, display)
        from .expectimax import board_to_move
        self.search_func = board_to_move

    def step(self):
        direction = self.search_func(self.game.board)
        return direction
