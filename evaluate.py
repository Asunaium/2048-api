from game2048.game import Game
from game2048.displays import Display
from game2048.agents import TRAINLABEL,TRAINDATA
import numpy as np

def single_run(size, score_to_win, AgentClass, **kwargs):
    game = Game(size, score_to_win)
    agent = AgentClass(game, display=Display(), **kwargs)
    agent.play(verbose=True)
    trainData=agent.trainData
    trainLabel=agent.trainLabel
    return game.score


if __name__ == '__main__':
    GAME_SIZE = 4
    SCORE_TO_WIN = 64
    N_TESTS = 10000

    '''====================
    Use your own agent here.'''
    from game2048.agents import ExpectiMaxAgent as TestAgent
    '''===================='''

    scores = []
    for _ in range(N_TESTS):
        score = single_run(GAME_SIZE, SCORE_TO_WIN,
                           AgentClass=TestAgent)
        scores.append(score)
    np.save('Test_trainData.npy',TRAINDATA)
    np.save('Test_trainLabel.npy', TRAINLABEL)



    print("Average scores: @%s times" % N_TESTS, sum(scores) / len(scores))

