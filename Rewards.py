class DefaultReward:
    possible_rewards = [0, -1, -1000]

    @staticmethod
    def reward(old_state, new_state):
        if old_state[5] == 1:
            print('nomnomnomnom')
            return 0
        if new_state[5] == 2:
            print('skill issue')
            return -1000
        return -1
    
class ManhattanReward:
    possible_rewards = [-i for i in range(16*2-1)] + [-1000]

    @staticmethod
    def reward(old_state, new_state):
        if old_state[5]:
            return 0
        if new_state[5]:
            return -1000
        return - abs(new_state[2] - new_state[0]) - abs(new_state[3] - new_state[1])