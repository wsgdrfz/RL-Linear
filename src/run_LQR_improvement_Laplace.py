import argparse
from lspi import *
from replay_buffer import ReplayBuffer
import gym
from env.linear_quadratic_regulator import LQREnv
from basis_func import *
import time
from collect_samples import *
from policy import *
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle
import os
from test_agent import *

# sample data files name for LQR
LQR_samples_filename = {
	2000: "samples/LQR/gaussian_actions_2000.pickle",
	5000: "samples/LQR/gaussian_actions_5000.pickle",
}
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--weight_discount', default=0.99, type=float)	# note: 1.0 only for finite
	parser.add_argument('--exploration', default=0.1, type=float)	# 0.0 means no random action
	parser.add_argument('--basis_function_dim', default=30, type=int)
	parser.add_argument('--stop_criterion', default=10**-3, type=float)
	parser.add_argument('--sample_max_steps', default="2000", choices=["2000","5000","10000","20000"])
	parser.add_argument('--max_steps', default=20, type=int)
	parser.add_argument('--reg_opt', default="wl1", choices=["l1","l2", "wl1", "none"])
	parser.add_argument('--reg_param', default=0.001, type=float)	# for l1 and l2
	parser.add_argument('--rbf_sigma', default=0.01, type=float)	# for RBFs
	# parser.add_argument('--batch_size', default=2000, type=int)
	parser.add_argument('--L', default=0.1, type=float)	# 0.0 means no random action
	

	args = parser.parse_args()
	params = vars(args)

	# env 
	env = LQREnv()
	params['n_actions'] = env.action_space.shape[0]
	params['state_dim'] = env.observation_space.shape[0]
	params['sample_max_steps'] = int(params['sample_max_steps'])
	# print(params['state_dim'])
	
	# basis function
	# real feature = n_feature**(dim of state + dim of action)
	n_features = params['basis_function_dim']
	gamma = params['weight_discount']
	# params['basis_func'] = ExactBasis4LQR()

	sample_filename = LQR_samples_filename[params['sample_max_steps']]
	# sample_filename = LQR_samples_filename["-22-10000"]
	f = open(sample_filename, 'rb')
	replay_buffer = pickle.load(f)
	batch_size = params['sample_max_steps']
	max_steps = params['max_steps']
	sample = replay_buffer.sample(batch_size)
	print("length of sample: {}".format(len(sample[0])))

	L_vec = 1.1*np.concatenate((np.max(np.abs(sample[0]), axis=0).flatten(), [np.max(np.abs(sample[1]))]))
	params['basis_func'] = Laplace_LQR(n_features, L_vec)
	params['policy'] = RBFPolicy4LQR(params['basis_func'])

	agent = BellmanAgent(params, n_iter_max=15)
	
	error_list, new_weights = agent.train(sample)

	test_agent4LQR(agent, env, gamma, ifshow=False)
	# clean
	env.close()


if __name__ == '__main__':
	main()








