from collections import namedtuple
import random

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayBase(object):
    r"""Replay Buffer Base Class
    Replay buffers can be used to store memory of transition states that can be used for training
    on. In the reinforcement learning a transition state is: ('state', 'action', 'next state', reward)

    API
        push: func, appends the transition state into memory
        sample: func, sample from memory to train from
        __len__: attr, number of transition states in memory buffer
    """

    def push(self, *args, **kwargs):
        """Push memory into replay buffer"""
        raise NotImplementedError

    def sample(self, *args, **kwargs):
        """Sample from the replay buffer"""
        raise NotImplementedError

    def __len__(self):
        """Length or number of transition states currently in buffer"""
        raise NotImplementedError


class ReplayBufferBasic(ReplayBase):
    r"""Basic implementation of a replay buffer"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def push_batch(self, batch):
        for replay in batch:
            self.push(replay)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def clear(self):
        self.memory.clear()
        self.position = 0


