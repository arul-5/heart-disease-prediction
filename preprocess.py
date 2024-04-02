import numpy as np

def preprocess_input(input_tuple):
    # Convert input tuple to numpy array
    input_as_numpy = np.asarray(input_tuple)
    
    # Reshape the array to have a single row and as many columns as elements in the original tuple
    input_reshaped = input_as_numpy.reshape(1, -1)
    
    return input_reshaped

def preprocess_data(data):
    data_dict = {key: int(value) if isinstance(value, np.int64) else value for key, value in data.items()}
    args = list(data_dict.values())
    return args
