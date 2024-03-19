import torch
import numpy as np
import random
import BaseNet as net
from Playground import Direction
import time


def action_wrapper(action_idx):
    if action_idx.__eq__(0):
        direction = Direction.UP
    elif action_idx.__eq__(1):
        direction = Direction.DOWN
    elif action_idx.__eq__(2):
        direction = Direction.LEFT
    elif action_idx.__eq__(3):
        direction = Direction.RIGHT
    return direction


def deep_q_learning(world, episodes=10000, step_limit=2000, epsilon=0.5, gamma=1, learning_rate=10**-9):
    Q = net.BaseNet()
    episode_progress = []
    actions = [0, 1, 2, 3]
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(Q.parameters(), lr=learning_rate)

    for episode in range(episodes):
        world.reset()
        print(f'im episode: {episode + 1}')
        running_loss = 0.0
        ep_return = 0
        final_step = step_limit
        current_state = world.current_state

        for step in range(step_limit):
            # time.sleep(0.05)
            if random.random() < epsilon:
                current_action = random.choice(actions)
            else:
                with torch.no_grad():
                    current_action = np.argmax([Q(torch.from_numpy(np.append(current_state[:5], 0)).double()), Q(torch.from_numpy(np.append(current_state[:5], 1)).double()), 
                                                Q(torch.from_numpy(np.append(current_state[:5], 2)).double()), Q(torch.from_numpy(np.append(current_state[:5], 3)).double())])
            # actual_action = action_wrapper(current_action)
            # print(actual_action)
            new_state, reward, done = world.ai_move(current_action)

            # check collisions
            if world.checkCollision():
                print('Loser')
                final_step = step + 1
                break
            world.foodCollision()
            # print(new_state[:5])
            ep_return += reward
            with torch.no_grad():
                y = reward + gamma * np.max([Q(torch.from_numpy(np.append(new_state[:5], 0)).double()), Q(torch.from_numpy(np.append(new_state[:5], 1)).double()), 
                                             Q(torch.from_numpy(np.append(new_state[:5], 2)).double()), Q(torch.from_numpy(np.append(new_state[:5], 3)).double())])
            # print(current_state[:5], current_action)
            output = Q(torch.from_numpy(np.append(current_state[:5], current_action)).double())
            # print('this is the nan output: ', output)
            optimizer.zero_grad()
            loss = criterion(output, torch.tensor(y))
            loss.backward()
            optimizer.step()

            # print('this is the nan loss: ', loss.item())
            running_loss += loss.item()

            current_state = new_state
            # print(done)

            if done == 2:
                final_step = step + 1
                break

        episode_progress.append(ep_return)
        print(running_loss)
        print(final_step)
        print(f'Episode {episode + 1} terminated after {final_step} steps. Total '
              f'Return was {ep_return} with a running loss of {running_loss/final_step} and epsilon of {epsilon}.')
        
        print('All episodes completed')

    return np.array(episode_progress)
