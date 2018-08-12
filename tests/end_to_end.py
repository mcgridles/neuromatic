import os
import subprocess

from backend.control import Control

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
add_text = lambda msg: print(msg)
properties = {
    'output_path': '{0}/files/'.format(project_dir),
    'training_data_path': '{0}/files/mnist.csv'.format(project_dir),
    'train_size': 0.8,
    'optimizer': 'adam',
    'loss': 'sparse_categorical_crossentropy',
    'metrics': ['accuracy'],
    'epochs': 5,
    'layers': [
        {
            'type': 'input',
            'size': 10,
            'activation': 'softmax',
            'input_dim': 784
        },
    ]
}

subprocess.call('unzip {0}/files/mnist.csv.zip -d {0}/files/'.format(project_dir), shell=True)

controller = Control(add_text)
controller.set_properties(properties)
controller.generate_network()
controller.train_network()

os.remove('{0}/files/mnist.csv'.format(project_dir))
os.remove('{0}/backend/network.py'.format(project_dir))