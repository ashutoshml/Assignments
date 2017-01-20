from __future__ import print_function

import numpy as np
import os
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
from logistic_sgd import load_data
from utils import tile_raster_images
import timeit
import theano.tensor as T
import glob
import sys
import theano

try:
	import PIL.Image as Image 
except ImportError:
	import Image

class dA(object):
	def __init__(
		self, 
		numpy_rng, 
		theano_rng=None, 
		input=None, 
		n_visible=784, 
		n_hidden=500, 
		W=None, 
		bhid=None, 
		bvis= None
	):
		self.n_visible = n_visible
		self.n_hidden = n_hidden

		if not theano_rng:
			theano_rng = RandomStreams(numpy_rng.randint(2**30))

		if not W:
			initial_W = np.asarray(
				numpy_rng.uniform(
					low = -4*np.sqrt(6./(n_hidden + n_visible)),
					high = 4*np.sqrt(6./(n_hidden + n_visible)),
					size=(n_visible, n_hidden)
				),
				dtype = theano.config.floatX
			)
			W = theano.shared(value=initial_W, name='W', borrow=True)

		if not bvis:
			bvis= theano.shared(
				value = np.zeros(
					n_visible,
					dtype=theano.config.floatX
				),
				name= 'bvis',
				borrow=True
			)

		if not bhid:
			bhid = theano.shared(
				value = np.zeros(
					n_hidden,
					dtype=theano.config.floatX
				),
				name='bhid',
				borrow=True
			)

		self.W = W
		self.b = bhid
		
		self.b_prime = bvis
		self.W_prime = W.T

		self.theano_rng = theano_rng
		if input is None:
			self.x = T.dmatrix(name='input')
		else:
			self.x = input

		self.params = [self.W,self.b, self.b_prime]

	def get_hidden_values(self, input):
		return T.nnet.sigmoid(T.dot(input,self.W) + self.b)

	def get_reconstructed_input(self, hidden):
		return T.nnet.sigmoid(T.dot(hidden, self.W_prime) + self.b_prime)
	
	def get_corrupted_input(self, input, corruption_level):
		return self.theano_rng.binomial(size=input.shape, n=1,
										p=1-corruption_level,
										dtype=theano.config.floatX) * input

	def get_cost_updates(self, corruption_level, learning_rate):
		tilde_x = self.get_corrupted_input(self.x, corruption_level)
		y = get_hidden_values(tilde_x)
		z = get_reconstructed_input(y)

		L = -1*T.sum(self.x * T.log(z) + (1-self.x)*T.log(1-z), axis=1)

		cost = T.mean(L)

		gparams = T.grad(cost, self.params)

		updates = [
			(param, param - learning_rate*gparam)
			for param, gparam in zip(self.params, gparams)
		]

		return (cost, updates)
	


def main():
	main

if __name__=="__main__":
	main()