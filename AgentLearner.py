import time

import numpy as np
import tensorflow as tf
import numpy.random as rd

import matplotlib.pyplot as plt
from tf_tools import variable_summaries, parameter_summaries
from Simulator import Simulator
from DKTGame import DKTGame

MANUAL, AUTO, AI = 0, 1, 2


class AgentLearner:
    n_actions = 2
    n_obs = 35

    print_per_episode = 50

    max_episode_len = 500
    batch_size = 200
    n_train_trials = 1000
    n_test_trials = 100
    gamma = 0.9999
    learning_rate = 0.01

    constant_baseline = 1.

    def __init__(self):
        parameter_summaries([self.batch_size, self.n_train_trials, self.n_test_trials, self.gamma, self.learning_rate],
                            ['batch_size', 'n_train_trials', 'n_test_trials', 'gamma', 'learning_rate'])

        self.state_holder = tf.placeholder(dtype=tf.float32, shape=(None, self.n_obs), name='symbolic_state')
        self.actions_one_hot_holder = tf.placeholder(dtype=tf.float32, shape=(None, self.n_actions),
                                                name='symbolic_actions_one_hot_holder')

        self.discounted_rewards_holder = tf.placeholder(dtype=tf.float32, shape=None, name='symbolic_reward')

        with tf.name_scope('linear_policy'):
            nr_hidden = 20

            w0 = np.array(rd.randn(self.n_obs, nr_hidden) / np.sqrt(self.n_obs),dtype=np.float32)
            b0 = np.zeros(nr_hidden, dtype=np.float32)

            w1 = np.array(rd.randn(nr_hidden, self.n_actions) / np.sqrt(self.n_obs),dtype=np.float32)
            b1 = np.zeros(self.n_actions, dtype=np.float32)

            w0_var = tf.Variable(initial_value=w0, trainable=True, name='weight_variable_input')
            variable_summaries(w0_var, '/w0_var')
            b0_var = tf.Variable(initial_value=b0, trainable=True, name='bias_input')
            variable_summaries(b0_var, '/b0_var')

            w1_var = tf.Variable(initial_value=w1, trainable=True, name='weight_variable_hidden_output')
            variable_summaries(w1_var, '/w1_var')
            b1_var = tf.Variable(initial_value=b1, trainable=True, name='bias_hidden_output')
            variable_summaries(b1_var, '/b1_var')

            a_z = tf.matmul(self.state_holder, w0_var, name='hidden_activation') + b0_var
            variable_summaries(a_z, '/a_z')
            out_hidden = tf.nn.relu(a_z, name='hidden_tanh_out')
            variable_summaries(out_hidden, '/out_hidden')

            a_z2 = tf.matmul(out_hidden, w1_var, name='output_activation') + b1_var
            variable_summaries(a_z2, '/a_z2')

            self.action_probabilities = tf.nn.softmax(a_z2, name='action_probabilities')
            variable_summaries(self.action_probabilities, '/action_probabilities')

            # This operation is used for action selection during testing, to select the action with the maximum action probability
            self.testing_action_choice = tf.argmax(self.action_probabilities, dimension=1, name='testing_action_choice')

        with tf.name_scope('loss'):
            log_probabilities = tf.log(tf.reduce_sum(tf.multiply(self.action_probabilities, self.actions_one_hot_holder), 1), name='log_probabilities')
            variable_summaries(log_probabilities, '/log_probabilities')

            sum_of_probabilities = tf.reduce_sum(log_probabilities, name='sum_of_probabilities')
            variable_summaries(sum_of_probabilities, '/sum_of_probabilities')

            sum_of_rewards = tf.reduce_sum(self.discounted_rewards_holder, name='sum_of_rewards')
            variable_summaries(sum_of_rewards, '/sum_of_rewards')

            pos_loss = tf.multiply(sum_of_probabilities, sum_of_rewards, name='positive_loss')
            variable_summaries(pos_loss, '/pos_loss')

            L_theta = tf.negative(pos_loss, name='L_theta')
            variable_summaries(L_theta, '/L_theta')

        with tf.name_scope('train'):
            self.gd_opt = tf.train.AdamOptimizer(self.learning_rate).minimize(L_theta)

        self.sess = tf.Session()
        self.merged = tf.summary.merge_all()
        suffix = time.strftime('%Y-%m-%d--%H-%M-%S')
        self.train_writer = tf.summary.FileWriter('tensorboard/DKT/{}'.format(suffix) + '/train', self.sess.graph)
        self.test_writer = tf.summary.FileWriter('tensorboard/DKT/{}'.format(suffix) + '/test')

        self.sess.run(tf.initialize_all_variables())

    def run(self, train=True, gui=False):
        self.reset()
        self.train = train
        while self.episode_no <= (self.n_train_trials if self.train else self.n_test_trials):
            if gui:
                self.game = DKTGame(nrPlayers=3, nrMaxRounds=self.max_episode_len)
                self.sim = self.game.s
            else:
                self.sim = Simulator(3, verbose=False)
            self.agent = self.sim.players[0]
            self.agent.control = AI
            self.agent.learner = self
            self.done = False

            winner = self.game.run() if gui else self.sim.run(showResults=False, rounds=1000)
            self.done = True
            self.decide(self.agent.getObservations())
            if self.agent == winner:
                self.gamesWon += 1
                self.react(10)
            elif winner is None:
                self.react(0)
            else:
                self.react(-10)

        self.plotResults(self.train)

    def trainNtest(self, gui=False):
        self.run()
        self.run(False, gui)

    def reset(self):
        self.batch_rewards = []
        self.states = []
        self.action_one_hots = []

        self.episode_rewards = []
        self.episode_rewards_list = []
        self.episode_steps_list = []

        self.step = 0
        self.episode_no = 0
        self.done = False
        self.gamesWon = 0

    def plotResults(self, train=False):
        if train: plt.figure()
        ax = plt.subplot(122 - train)
        ax.plot(range(len(self.episode_rewards_list)), self.episode_rewards_list)
        ax.set_title("Training" if train else "Testing" + " rewards")
        ax.set_xlabel('Episode number')
        ax.set_ylabel('Episode reward')
        if not self.train:
            plt.show()

    def decide(self, observation):
        self.step = self.sim.currentRound
        if self.train:
            action_probability_values = self.sess.run(self.action_probabilities,
                                                 feed_dict={self.state_holder: [observation]})

            action = np.random.choice(np.arange(self.n_actions), p=action_probability_values.ravel())
            action_arr = np.zeros(self.n_actions)
            action_arr[action] = 1.
            self.action_one_hots.append(action_arr)

            # Record states
            self.states.append(observation)

            return action

        else:
            test_action, = self.sess.run([self.testing_action_choice],
                                    feed_dict={self.state_holder: [observation]})

            return test_action[0]

    def react(self, reward):
        if self.step >= self.max_episode_len or self.agent.dead:
            self.done = True

        self.batch_rewards.append(reward)
        self.episode_rewards.append(reward)

        if self.train and len(self.batch_rewards) > 0 and self.done:

            # First calculate the discounted rewards for each step
            batch_reward_length = len(self.batch_rewards)
            discounted_batch_rewards = self.batch_rewards.copy()
            for i in range(batch_reward_length):
                discounted_batch_rewards[i] *= (self.gamma ** (batch_reward_length - i - 1))

            summary, gradients = self.sess.run([self.merged, self.gd_opt],
                          feed_dict={self.actions_one_hot_holder: self.action_one_hots, self.state_holder: self.states,
                                     self.discounted_rewards_holder: discounted_batch_rewards})
            self.train_writer.add_summary(summary, self.episode_no)

            self.action_one_hots = []
            self.states = []
            self.batch_rewards = []

        if self.done:
            # Done with episode. Reset stuff.
            self.episode_no += 1

            self.episode_rewards_list.append(np.sum(self.episode_rewards))
            self.episode_steps_list.append(self.step)

            self.episode_rewards = []
            self.step = 0

            if self.episode_no % self.print_per_episode == 0:
                print("{} of {} games won!".format(self.gamesWon, self.print_per_episode))
                self.gamesWon = 0
                print("Episode {}: Average steps in last {} episodes".format(self.episode_no, self.print_per_episode),
                      np.mean(self.episode_steps_list[(self.episode_no - self.print_per_episode):self.episode_no]), '+-',
                      np.std(self.episode_steps_list[(self.episode_no - self.print_per_episode):self.episode_no])
                      )


if __name__ == "__main__":
    learner = AgentLearner()
    withGUI = False
    learner.trainNtest(withGUI)