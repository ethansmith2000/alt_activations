import torch
from torch import nn



class NormalizedExp(nn.Module):

    def __init__(self, beta=0.99):
        super().__init__()
        self.register_buffer("avg_max", torch.tensor(1.0))
        self.beta = beta

    def forward(self, x):
        max_val = torch.max(x) / 2
        self.avg_max = self.beta * self.avg_max + (1 - self.beta) * max_val
        return torch.exp(x - self.avg_max)


class Activation(nn.Module):

    def __init__(self, activation_type: str = 'relu', power=1.0):
        super().__init__()
        self.activation_type = activation_type
        if activation_type == 'relu':
            activation = lambda x: torch.nn.functional.relu(x)
        elif activation_type == 'gelu':
            activation = lambda x: torch.nn.functional.gelu(x)
        elif activation_type == 'silu':
            activation = lambda x: torch.nn.functional.silu(x)
        elif activation_type == 'tanh':
            activation = lambda x: torch.tanh(x)
        elif activation_type == 'sin':
            activation = lambda x: torch.sin(x)
        elif activation_type == 'sin_residual':
            activation = lambda x: torch.sin(x) + (x/2)
        elif activation_type == 'relu_sin':
            activation = lambda x: torch.sin(torch.relu(x)) + torch.relu(x/2)
        elif activation_type == 'norm_exp':
            activation = NormalizedExp()

        if power != 1.0:
            self.activation = lambda x: torch.pow(activation(x), power)
        else:
            self.activation = activation

    def forward(self, x):
        return self.activation(x)