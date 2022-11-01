import torch
import math

def made_atan2(A_tensor, B_tensor):
    new_tensor = []
    A = A_tensor.numpy()
    B = B_tensor.numpy()
    for a_num, b_num in zip(A, B):
        new_tensor.append(math.atan2(a_num, b_num))

    return torch.tensor(new_tensor)
