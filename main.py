from game2048.agents import Agent


class YourOwnAgent(Agent):

    def step(self):
        '''To define the agent's 1-step behavior given the `game`.
        You can find more instance in [`agents.py`](game2048/agents.py).

        :return direction: 0: left, 1: down, 2: right, 3: up
        '''
        direction = Agent.ExpectiMaxAgent(self.game)
        return direction