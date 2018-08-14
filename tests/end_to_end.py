import os
import subprocess

from backend import control

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
properties = {
    'project_directory': '{0}/files/'.format(project_dir),
    'data_path': '{0}/files/mnist.csv'.format(project_dir),
    'training_size': 0.8,
    'optimizer': 'adam',
    'loss': 'sparse_categorical_crossentropy',
    'metrics': ['accuracy'],
    'epochs': 5,
    'layers': [
        {
            'type': 'input',
            'dimensions': 784
        },
        {
            'type': 'output',
            'size': 10,
            'activation': 'softmax',
        }
    ]
}

# Unzip MNIST dataset
subprocess.call('unzip {0}/files/mnist.csv.zip -d {0}/files/'.format(project_dir), shell=True)

controller = control.Control()
controller.init_status(lambda msg: print(msg))
controller.set_properties(properties)
controller.generate_network()
controller.train_in_new_thread()

# Remove files created while running
os.remove('{0}/files/mnist.csv'.format(project_dir))
os.remove('{0}/backend/network.py'.format(project_dir))