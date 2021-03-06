import torch
import torch.nn as nn
import numpy as np
from multiprocessing import Lock

class Player(nn.Module):
    """ Feed forward player module - default dimensions such that
        every legal tic tac toe board state is considered.

        Args:
            in_dim (int, optional): Dimension of input layer. Defaults to 9.
            fc1_dim (int, optional): Dimension of 1st hidden layer. Defaults to 250.
            fc2_dim (int, optional): Dimension of 2nd hidden layer. Defaults to 250.
            out_dim (int, optional): Dimension of output layer. Defaults to 9.

    """

    def __init__(self, in_dim=9, fc1_dim=250, fc2_dim=250, out_dim=9):
        super(Player, self).__init__()
        self.fc1 = nn.Linear(in_dim, fc1_dim)
        self.fc2 = nn.Linear(fc1_dim, fc2_dim)
        self.fc3 = nn.Linear(fc2_dim, out_dim)
        self.score = 0
        self.lock = Lock()

    def update_score(self, update):
        self.lock.acquire()
        self.score += update
        self.lock.release()

    def forward(self, x):
        """ Completes 1 forward pass through this network.

            Args:
                x (list[float]): Current board state of dimension 'in_dim'.

            Returns:
                list[float]: Transformed input of dimension 'out_dim'.

        """

        x = torch.tensor(x).float()
        y = self.fc1(x)
        y = torch.tanh(y)
        y = self.fc2(y)
        y = torch.tanh(y)
        y = self.fc3(y)
        y = torch.softmax(y, dim=0)

        return y.data.numpy()

    def save_model(self, path):
        """ Saves this network's state dictionary to file at 'path'.

            Args:
                path (str): Path to file where state dictionary will be saved.

        """
        torch.save(self.state_dict(), path)

    def load_model(self, path):
        """ Loads a saved state dictionary into this network from 'path'.

            Args:
                path (str): Path to file from which state dictionary will be loaded.

        """
        self.load_state_dict(torch.load(path))

    def state(self):
        """ Loads a saved state dictionary into this network from 'path'.

            Args:
                path (str): Path to file from which state dictionary will be loaded.

            Returns:
                (dict): The state dictionary of this network.

        """
        return self.state_dict()

    def __repr__(self):
        return f'(NN {str(abs(hash(str(self.state_dict()))))[:3]})'

    #def __eq__(self, other):
    #    return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score


if __name__ == '__main__':
    # Testing manual parameter overriding.
    p1 = Player()
    p2 = Player()
    p3 = Player()
    w1 = p1.state()['fc3.weight'].numpy()
    w2 = p2.state()['fc3.weight'].numpy()
    print(p3.state()['fc3.weight'])
    p3.state_dict()['fc3.weight'].copy_(torch.tensor((w1 + w2) / 2))
    print()
    print(p3.state()['fc3.weight'])



