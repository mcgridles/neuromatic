# Neuromatic

Neural network visualization and prototyping tool built using Keras and TKinter.

The goal of this project was to create a tool that would allow developers to design and build neural networks without needing years of machine learning or coding experience. A user should be able to take a neural network like the one pictured below and convert it into code using a GUI.

![neural network diagram](files/nn_diagram.png)

## Setup
### For Unix Distributions Only
If running Neuromatic for the first time, all that is required is the installation of Python 3.6 and pip3. To set up your environment, via a command prompt run `python3 setup.py install` in the neuromatic directory to install all dependencies and modules. If an error occurs, run `pip3 install --upgrade tensorflow` followed by `python3 setup.py install`. To run the program run `python3 Neuromatic.py` in the neuromatic folder. 

### Usage

![neuromatic window](files/window_example.png)

```bash
cd /path/to/neuromatic

python3 Neuromatic.py
```
Using the gui, a good place to start is the canvas properties box. To edit the project configuration simply click the canvas properties box on the left side to edit the configurations. If you would like to use existing training data A test csv file is located in the `files` folder, simply unzip it, and point to it in the training data path. The project directory path will be the location of all output files which include the canvas property pkl file, the python script, and the h5 trained model file. Once the project properties are set, click okay to update the canvas. 

Next, to create a neural network, drag and drop the layer types on the right side onto slots in the canvas. If you wish to edit layer properties simply click the layer on the canvas to edit its properties. To delete individual layers drag them from the canvas to the trash icon. To clear all slots click the top clear slots button. To set all canvas properties to default press the new canvas button. To open a saved canvas simply click file->open and select the pkl file you wish to load. A well-functioning neural network .pkl configuration can be found in the file folder, just be sure to change the project directory and csv location in project properties. Be sure that the input dimensions correspond to the number of features in the csv file. For the Mnist data set this input dimension is 784.

Once you have a satisfactory neural network designed, click the generate button. This will create a python script in the project directory which can be externally used to create the neural network. After a script is generated you can train the model by clicking the train model button at the top, and can cancel it at any time by clicking the top cancel button. The trained model will be saved to the selected directory for use outside of the program.

### Data
A CSV formatted version of the MNIST dataset (example shown below) is included with this project under `neuromatic/files/mnist.csv.zip`. All data must be pre-processed to match the csv format. 

![mnist examples](files/mnist_examples.png)

### Examples
These are two baseline networks manually built using Keras and TensorFlow. Running the scripts trains them on the MNIST dataset and displays their accuracy.

```bash
python -m examples.keras_baseline
python -m examples.tf_baseline
```

After building a network, you can test it on some custom hand-written numbers by running
```bash
python -m examples.number_prediction
```
