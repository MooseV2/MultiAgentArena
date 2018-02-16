import json
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import sgd


class Catch(object):
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.reset()

    def _update_state(self, action):
        """
        Input: action and states
        Ouput: new states and reward
        """

        state = self.state
        if action == 0: #left
            action = -1
            axis = 'x'
        elif action == 1: # right
            action = +1
            axis = 'x'
        elif action == 2: # up
            action = +1
            axis = 'y'
        elif action == 3: # Down
            action = -1
            axis = 'y'
        else:
            print("Invalid Action")


        x0,y0,count = state[0]

        if axis == 'x':
            if x0==0 and action == -1 :
                x0 +=1
            elif x0 ==self.grid_size and action == 1:
                x0 -=1
            elif action == -1:
                x0 -=1
            else :
                x0 +=1
        if axis == 'y' :
            if y0==0  and action == -1:
                y0+=1
            elif y0 ==self.grid_size and action == 1:
                y0-=1
            elif action == -1:
                y0 -=1
            else:
                y0 +=1
        count +=1


        out = np.asarray([x0,y0,count,state[0][0:1]])
        out = out[np.newaxis]
        # print (out)
        # print(out.shape)
        # assert len(out.shape) == 2
        self.state = out
        # print("State: ",self.state)

    def _draw_state(self):
        im_size = (self.grid_size,)*2
        state = self.state[0]
        canvas = np.zeros(im_size)
        canvas[state[0]-1,state[1]-1] = 1  # draw bot
        return canvas

    def _get_reward(self):
        x0,y0,count = self.state[0]
        if (x0 == self.targets[0] and y0 == self.targets[1]) or (x0 == self.targets[2] and y0 == self.targets[3])  :
            self.targets[2] -=1
            return 1
        elif count < 50:
            return -0.1
        else:
            return -0.2

    def _is_over(self):
        if self.targets[] == 0 or self.state[0][5] == self.grid_size**2:
            return True
        else:
            return False

    def observe(self):
        canvas = self._draw_state()
        return canvas.reshape((1, -1))

    def act(self, action):
        self._update_state(action)
        reward = self._get_reward()
        game_over = self._is_over()
        return self.observe(), reward, game_over

    def reset(self):
        x0 = np.random.randint(0, self.grid_size-1, size=1)
        y0 = np.random.randint(0, self.grid_size-1, size=1)
        targ1x = np.random.randint(0, self.grid_size-1, size=1)
        targ1y = np.random.randint(0, self.grid_size-1, size=1)
        targ2x = np.random.randint(0, self.grid_size-1, size=1)
        targ2y = np.random.randint(0, self.grid_size-1, size=1)
        # print("targ1",targ1x,targ1y)
        self.targets = [targ1x,targ1y,targ1x,targ1y,2]

        self.state = np.asarray([x0, y0,0])[np.newaxis]


class ExperienceReplay(object):
    def __init__(self, max_memory=100, discount=.9):
        self.max_memory = max_memory
        self.memory = list()
        self.discount = discount

    def remember(self, states, game_over):
        # memory[i] = [[state_t, action_t, reward_t, state_t+1], game_over?]
        self.memory.append([states, game_over])
        if len(self.memory) > self.max_memory:
            del self.memory[0]

    def get_batch(self, model, batch_size=10):
        len_memory = len(self.memory)
        num_actions = model.output_shape[-1]
        env_dim = self.memory[0][0][0].shape[1]
        inputs = np.zeros((min(len_memory, batch_size), env_dim))
        targets = np.zeros((inputs.shape[0], num_actions))
        for i, idx in enumerate(np.random.randint(0, len_memory,
                                                  size=inputs.shape[0])):
            state_t, action_t, reward_t, state_tp1 = self.memory[idx][0]
            game_over = self.memory[idx][1]

            inputs[i:i+1] = state_t
            # There should be no target values for actions not taken.
            # Thou shalt not correct actions not taken #deep
            targets[i] = model.predict(state_t)[0]
            Q_sa = np.max(model.predict(state_tp1)[0])
            if game_over:  # if game_over is True
                targets[i, action_t] = reward_t
            else:
                # reward_t + gamma * max_a' Q(s', a')
                targets[i, action_t] = reward_t + self.discount * Q_sa
        return inputs, targets


if __name__ == "__main__":
    # parameters
    epsilon = .1  # exploration
    num_actions = 4  # [move_left, stay, move_right]
    epoch = 1000
    max_memory = 500
    hidden_size = 100
    batch_size = 300
    grid_size = 10

    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size**2,), activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(num_actions))
    model.compile(sgd(lr=.2), "mse")

    # If you want to continue training from a previous model, just uncomment the line bellow
    # model.load_weights("model.h5")

    # Define environment/game
    env = Catch(grid_size)

    # Initialize experience replay object
    exp_replay = ExperienceReplay(max_memory=max_memory)

    # Train
    win_cnt = 0
    for e in range(epoch):
        loss = 0.
        env.reset()
        game_over = False
        # get initial input
        input_t = env.observe()

        while not game_over:
            _epsilon = _epsilon*(epsilon/len(epoch))
            input_tm1 = input_t
            # get next action
            if np.random.rand() <= epsilon:
                action = np.random.randint(0, num_actions, size=1)
            else:
                q = model.predict(input_tm1)
                action = np.argmax(q[0])

            # apply action, get rewards and new state
            input_t, reward, game_over = env.act(action)
            if reward == 1:
                win_cnt += 1

            # store experience
            exp_replay.remember([input_tm1, action, reward, input_t], game_over)

            # adapt model
            inputs, targets = exp_replay.get_batch(model, batch_size=batch_size)

            loss += model.train_on_batch(inputs, targets)
        print("Epoch {:03d}/999 | Loss {:.4f} | Win count {}".format(e, loss, win_cnt))

    # Save trained model weights and architecture, this will be used by the visualization code
    model.save_weights("model.h5", overwrite=True)
    with open("model.json", "w") as outfile:
        json.dump(model.to_json(), outfile)
