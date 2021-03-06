# -*- coding: utf-8 -*-
from replay_buffer import ReplayBuffer
from collections import namedtuple
import numpy as np
import pickle
from env.linear_quadratic_regulator import LQREnv
import gym

Transition = namedtuple('Transition',
                        ('state', 'action','reward', 'next_state', 'done'))

def collect_samples_maxstep(env, max_steps, agent=None):
	ifRandom = False
	replay_buffer = ReplayBuffer()
	if agent==None:
		# random policy
		ifRandom = True
	i_episode_steps = 0
	state = env.reset()
	while i_episode_steps < max_steps:
		i_episode_steps += 1
		# action = env.action_space.sample()
		action = env.action_space.sample()
		state_, reward, done, info = env.step(action)
		replay_buffer.store(state, action, reward, state_, done)
		state = state_
		# if done:
		# 	break
	return replay_buffer



def collect_samples_maxepisode(env, max_episodes, agent=None, max_steps=None):
	ifRandom = False
	replay_buffer = ReplayBuffer()
	if agent==None:
		# random policy
		ifRandom = True
	if max_steps ==None:
		max_steps = np.inf
	for i_episode in range(max_episodes):
		state = env.reset()
		done  = False
		i_episode_steps = 0
		while True and i_episode_steps<1000:
			i_episode_steps += 1
			if ifRandom:
				action = env.action_space.sample()
			else:
				action = agent.get_action(state)
			state_, reward, done, info = env.step(action)
			# for cart pole
			x, xdot, theta, thetadot = state
			reward = -10*theta**2
			replay_buffer.store(state, action, reward, state_, done)
			state = state_
			if done:
				break
	return replay_buffer

# collect samples using gaussain actions
def collect_samples_gaussian(env, max_steps):
	replay_buffer = ReplayBuffer()
	i_episode_steps = 0
	state = env.reset()
	done  = False
	while i_episode_steps<max_steps:
		i_episode_steps += 1
		# action = env.action_space.sample()
		action = np.matrix(np.random.normal(0, 1, 1)[0])
		state_, reward, done, info = env.step(action)
		replay_buffer.store(state, action, reward, state_, done)
		state = state_
	return replay_buffer
	# f = open(filename, 'wb')
	# pickle.dump(replay_buffer, f)

def collect_LQR_gaussian(env, max_steps):
	# shape of state
	m = env.m
	# shape of action
	n = env.n
	replay_buffer = ReplayBuffer()
	i_episode_steps = 0
	state = env.reset()
	done  = False
	while i_episode_steps < max_steps:
		i_episode_steps += 1
		action = np.matrix(np.random.normal(0, 1, n).reshape(n,1))
		state_, reward, done, info = env.step(action)
		replay_buffer.store(state, action, reward, state_, done)
		state = state_
	return replay_buffer


def collect_LQR_uniform(env, max_steps):
	# shape of state
	m = env.m
	# shape of action
	n = env.n
	replay_buffer = ReplayBuffer()
	i_episode_steps = 0
	state = env.reset()
	done  = False
	while i_episode_steps < max_steps:
		i_episode_steps += 1
		action = np.matrix(np.random.uniform(-4, 4, n).reshape(n,1))
		state_, reward, done, info = env.step(action)
		replay_buffer.store(state, action, reward, state_, done)
		state = state_
	return replay_buffer


def collect_samples_L(env, states,L):
	replay_buffer = ReplayBuffer()
	env.reset()
	for i in range(len(states)):
		state = np.matrix(states[i])
		action = -L*state
		# print("action: {}".format(action.T))
		state_, reward, done, info = env.step(action)
		replay_buffer.store(state, action, reward, state_, done)
	return replay_buffer

if __name__ == '__main__':
	# collect samples for 2000 steps

	# env = LQREnv()
	# A = np.matrix([[0.9,0.],[0.1,0.9]])
	# B = np.matrix([[1],[0.]])
	# Z1 = np.matrix([[0,0],[0,1]])
	# Z2 = 0.1
	# noise_cov = np.matrix([[0.01,0],[0,0.01]])
	# env = LQREnv(A=A,B=B,Z1=Z1,Z2=Z2,noise_cov=noise_cov)
	
	# sample_step_list = [2000, 5000]
	# for steps in sample_step_list:
	# 	replay_buffer = collect_LQR_gaussian(env, steps)
	# 	f1 = open("samples/LQR2D/gaussian_actions_"+str(steps)+".pickle", 'wb')
	# 	pickle.dump(replay_buffer, f1)
	# 	f1.close()

	# CartPole-v0
	env = gym.make('CartPole-v0')
	fn_pre = "samples/CartPole/CartPole"
	slist = np.arange(1,10)*100
	for s in slist:
		fn  = fn_pre+str(s)+"-2.pickle"
		f = open(fn, 'wb')
		replay_buffer = collect_samples_maxepisode(env, s)
		pickle.dump(replay_buffer, f)
		f.close()

	# Mountain car
	# env = gym.make('MountainCar-v0')
	# fn_pre = "samples/MountainCar/"
	# slist = np.arange(1,10)*1000
	# for s in slist:
	# 	print(s)
	# 	fn  = fn_pre+'MC'+str(s)+".pickle"
	# 	f = open(fn, 'wb')
	# 	replay_buffer = collect_samples_maxstep(env, s)
	# 	pickle.dump(replay_buffer, f)
	# 	f.close()


	



