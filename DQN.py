import torch
import numpy as np
import random
import BaseNet as net
from Playground import Direction


def deep_q_learning(world, episodes=1000, step_limit=1000, epsilon=10**-2, gamma=1, learning_rate=10**-3):
    Q = net.BaseNet()
    episode_progress = []
    actions = [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(Q.parameters(), lr=learning_rate)
    running_loss = 0.0

    for episode in range(episodes):
        ep_return = 0
        final_step = step_limit
        current_state = world.current_state

        for step in range(step_limit):
            if random.random() < epsilon:
                current_action = random.choice(actions)
            else:
                with torch.no_grad():
                    current_action = Q(torch.from_numpy(world.current_state)) # gotta fix that and make network have one input node more so action fits in there and then take argmax
            new_state, reward, done = world.ai_move(current_action)
            
            ep_return += reward

            with torch.no_grad():
                y = reward + gamma * np.max(Q(torch.from_numpy(new_state).double()).numpy()) # same as above but its late/early and too lazy for this right now

            output = Q(torch.from_numpy(np.append(current_state, current_action))) # this is prolly gonna the format we use but who knows where this is going right now
            optimizer.zero_grad()
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            current_state = new_state

            if done:
                final_step = step + 1
                break
            episode_progress.append(ep_return)
            print(f'Episode {episode + 1} terminated after {final_step} steps. Total '
                  f'Return was {ep_return} with a running loss of {running_loss/final_step} and epsilon of {epsilon}.')
        
        print('All episodes completed')

        return np.array(episode_progress)
