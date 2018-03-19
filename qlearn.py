import json
import numpy as np
import csv
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import sgd, Adam
from keras.layers.advanced_activations import PReLU


class Catch(object):
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.reset()

    def _get_Current(self):
        x = self.state[0][0]
        y = self.state[0][1]
        return [x,y]

    def _overlap(self):
        self.overlap += 1

    def _get_overlap(self):
        return self.overlap

    def valid_actions(self):

        actions = [0,1,2,3]

        pos = self._get_Current()
        if pos[0] == 0:
            actions.remove(0)
        if pos[1] == 0:
            actions.remove(3)
        if pos[0] == self.grid_size-1:
            actions.remove(1)
        if pos[1] == self.grid_size-1:
            actions.remove(2)

        return actions



    def _update_state(self, action):
        """
        Input: action and states
        Ouput: new states and reward
        """
        state = self.state
        #Current Position
        pos = self._get_Current()

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



        # if action == 0: #left
        #     pos[0] -= 1
        # elif action == 1: # right
        #     pos[0] += 1
        # elif action == 2: # up
        #     pos[1] += 1
        # elif action == 3: # Down
        #     pos[1] -= 1
        # else:
        #     print("Invalid Action")





        if axis == 'x':
            if pos[0]==0 and action == -1 :
                # pos[0] +=1
                pass
            elif pos[0] ==self.grid_size-1 and action == 1:
                # pos[0] -=1
                pass
            elif action == -1:
                pos[0] -=1
            else :
                pos[0] +=1
        if axis == 'y' :
            if pos[1]==0  and action == -1:
                # pos[1]+=1
                pass
            elif pos[1] ==self.grid_size-1 and action == 1:
                # pos[1]-=1
                pass
            elif action == -1:
                pos[1] -=1
            else:
                pos[1] +=1

        # print("pos :",pos)

        out = self.state
        out = np.insert(out,0,pos)

        self.state = np.reshape(out, (int(len(out)/2),2))

    def _draw_state(self):
        im_size = (self.grid_size,)*2
        points = self.targets
        state = self.state
        head = state[0]
        canvas = np.zeros(im_size)

        for pos in state:
            if np.all(head == pos):
                canvas[pos[0],pos[1]] = 1
            else:
                canvas[pos[0],pos[1]] = 0.5

        canvas[points[1],points[2]] = 0.1
        return canvas

    def _get_reward(self):
        count = len(self.state)
        pos = self.state[0]
        if (pos[0] == self.targets[1] and pos[1] == self.targets[2]):# or (pos[0] == self.targets[2] and pos[1] == self.targets[3])  :
            print ("Found a target in {} moves".format(count))
            self.targets[0] -=1
            return 1
        elif ([pos[0],pos[1]] in pos ):
            self._overlap()
            # print("On my tail")
            return -0.05
        else:
            return 0.001

    def _is_over(self):
        if self.targets[0] == 0: #or len(self.state) >= 250:
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
        self.overlap = 0
        # targ2x = np.random.randint(0, self.grid_size-1, size=1)
        # targ2y = np.random.randint(0, self.grid_size-1, size=1)
        # print("targ1",targ1x,targ1y)
        self.targets = [1,targ1x,targ1y]
        i = [x0,y0]
        # print(i)
        self.state = np.asarray(i).T
        # print (self.state)


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
        env_dim = self.memory[0][0][0].shape[1] #
        # print ("Memory: ",self.memory)
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
    metrics = []
    moves=0
    # parameters
    epsilon = 0.8  # exploration
    _epsilon = epsilon
    num_actions = 4  # [move_left, stay, move_right]
    epoch = 1000
    max_memory = 500
    hidden_size = 100
    batch_size = 100
    grid_size = 10
    decay = 0.01

    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size**2,)))
    model.add(PReLU())
    model.add(Dense(hidden_size))
    model.add(PReLU())
    model.add(Dense(num_actions))
    # model.compile(sgd(lr=0.001), "mse")
    model.compile(Adam(lr=0.01, beta_1=0.9, beta_2=0.999,
    epsilon=1e-08, decay=0.0), "mse")

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
        moves = 0
        env.reset()
        game_over = False
        # get initial input
        input_t = env.observe()
        _epsilon = _epsilon-(epsilon/epoch) # linear
        # _epsilon = epsilon*pow(1-decay,e) # exponential

        while not game_over:

            moves +=1

            input_tm1 = input_t
            # get next action
            if np.random.rand() <= _epsilon:

                # action = np.random.randint(0, num_actions, size=1)
                action = np.random.choice(env.valid_actions())
            else:
                q = model.predict(input_tm1)
                action = np.argmax(q[0])



            # apply action, get rewards and new state
            input_t, reward, game_over = env.act(action)

            if action not in env.valid_actions():
                reward = -1

            # store experience
            exp_replay.remember([input_tm1, action, reward, input_t], game_over)

            # adapt model
            inputs, targets = exp_replay.get_batch(model, batch_size=batch_size)

            loss += model.train_on_batch(inputs, targets)
        print("Epoch {:03d}/1000 | Loss {:.4f} | ".format(e+1, loss, ))

        metrics.append([e+1, loss, moves, env._get_overlap()])
        # print (metrics)

        # Save trained model weights and architecture, this will be used by the visualization code
        if (e%100 ==0):
            modelname = "model/model"+str(e)
            model.save_weights(modelname+".h5", overwrite=True)
            with open(modelname+".json", "w") as outfile:
                json.dump(model.to_json(), outfile)
    with open("model/metrics","wb") as metricfile:
        wr = csv.writer(metricfile,quoting=csv.QUOTE_ALL)
        wr.writerow(metrics)
