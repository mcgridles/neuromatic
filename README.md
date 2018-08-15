# Neuromatic

Neuromatic is a neural network visualization and prototyping tool built using Keras and TKinter.

The goal of this application is to enable developers, with minimal machine learning experience, to design and build
neural networks. A user can implement and train a simple neural network, similar to the network pictured below, using
this application. **This application is supported on Unix based operating systems**.

![neural network diagram](files/nn_diagram.png)

A neural network with three layers; an input layer with three "nodes" or "neurons", a hidden layer with four, and an output layer with two. This type of network would output a probability that a given input belongs to class 1 or class 2, corresponding to the two output nodes.

## Setup
### Installation
**Requires:**
* Python 3.6
* pip3

**Install:**
* Download from GitHub
* `cd path/to/Neuromatic`
* `python3 setup.py install`

**If errors occur during installation, run:**
* `pip3 install --upgrade tensorflow`
* `python3 setup.py install`

**Run the application:**
* `cd path/to/Neuromatic`
* `python3 Neuromatic.py`

## Usage

![neuromatic window](files/window_example.png)

### Canvas Properties Box
Click the Canvas Properties Box, at the top left of the canvas, to open the properties editor. Click OK to save
properties.

**Canvas Name**

Project files will be saved to this name, using a different file extension depending on the file type.

**Number of Component Slots**

The number of component slots that exist on the canvas. (3-10)

**Training Data Path**

User specified path to the data on which the model will be trained. (CSV)

**Project Directory**

The directory to which all project files will be saved. Project files will take on the name specified by Canvas Name.
Files stored in this directory:
* canvas property pkl file `<canvas_name>.pkl`
  * Used to reload a saved canvas design to the application
* neural network python file `<canvas_name>_network.py`
  * Used to load the canvas design into Keras
* trained model files `<canvas_name>_weights.h5`, `<canvas_name>_model.h5`, `<canvas_name>_model.json`
  * Used to reload a trained model into Keras


**Training Size**

The proportion of training data to test data, in the training data file, that the application will use to train the
model and test its accuracy.

**Optimizer**

**Loss**

**Epochs**

Number of times the training data will run through the neural network. Increasing the number of Epochs increases the
accuracy of the model, but also increases training time.

### Layers
A layer can be clicked and dragged from the top right of the application window and dropped on an empty slot on the
canvas to add the layer to the neural network design. Left clicking a layer on the canvas will open a properties editor
box. To delete a canvas layer, click and hold on the canvas layer, drag the cursor over the trash icon at the bottom
left of the canvas, and release the click. 

**Input Layer**
This must be the first layer and represents the first column of the neural network. 

The only input this takes is the dimensions of the input data, which is the number of features. For the MNIST dataset this will be 784, but it will be different for every dataset.

**Output Layer**
This represents the final column of the neural network, although it is not required to be the final layer because the ouput layer and hidden layer are functionally the same.

This layer type takes an activation function, which adds non-linearity to the network and allows it to classify more complex data, and the size. Size represents the number of classifications the network can make; for the MNIST dataset this number will be 10 because the network can classify a data point as an integer 0-9. 

**Hidden Layer**
Hidden layers are all middle columns in a neural network. More hidden layers means the network can classify more complex data, although too many hidden layers may cause the network to not "[overfit](https://en.wikipedia.org/wiki/Overfitting)", which is when it has a hard time generalizing for new data.

This layer type takes an activation function and a size, just like the output layer, but in this case the size just corresponds to the number of nodes in the layer.

**Dropout Layer**
[Dropout](https://medium.com/@amarbudhiraja/https-medium-com-amarbudhiraja-learning-less-to-learn-better-dropout-in-deep-machine-learning-74334da4bfc5) layers prevent overfitting by reducing a network's ability to rely too heavily on a single neuron.

This layer type only takes is a percentage, which represents the probability that any given node is ignored during a single epoch. By ignoring nodes no one node can become too highly weighted, which could cause it to have too much of an effect on the system. This helps improve the network's ability to generalize on data.

### Control Buttons

**New Canvas**

Erases the current canvas and sets all canvas properties to their default values.

**Generate Script**

Creates a python script capable of creating the neural network. The file is saved to the project
directory and can be used outside of neuromatic. A copy is also made for neuromatic to use in
training the network. Can only be used once a valid canvas has been created.

**Train Model**

Used after the generate script python file has been created. Trains the network on the selected
training data and saves the h5 and json files to the project directory, for the user to use outside
of neuromatic. Displays the status of the training process and outputs the created models accuracy.

**Cancel**

Cancels the training of the model.

**Clear Canvas**

Sets all current slots to empty layers

To clear all slots click the top clear slots button. To set all canvas
properties to default press the new canvas button. To open a saved canvas simply click file->open and select the pkl
file you wish to load. A well-functioning neural network .pkl configuration can be found in the file folder, just be
sure to change the project directory and csv location in project properties. Be sure that the input dimensions
correspond to the number of features in the csv file. For the Mnist data set this input dimension is 784.

Once you have a satisfactory neural network designed, click the generate button. This will create a python script in
the project directory which can be externally used to create the neural network. After a script is generated you can
train the model by clicking the train model button at the top, and can cancel it at any time by clicking the top cancel
button. The trained model will be saved to the selected directory for use outside of the program.

###Tutorial

If this is your first time working with neuromatic it is suggested you follow this short guide to create your first
network. You can begin by unzipping the mnist csv.zip file located in the files directory. Next follow the installation
steps given in the setup section and then launch the application. When the program loads begin by modifying the
canvas properties to point to the location of the mnist data set you have just unzipped. All other properties can
be set to your liking. Next, when you begin designing the network, drag an input layer into the first slot on the
canvas, and set its dimensions to 784, this is the feature size of the mnist data set. Next fill in all remaining
layers. When the design is complete, click the generate button to create the python script representation of your
network. Finally, click the train button to train a model. This will output the created model to your selected
project directory as well as tell you how accurate the model was after training.


## Data
A CSV formatted version of the MNIST dataset (example shown below) is included with this project under `neuromatic/files/mnist.csv.zip`. All data must be preprocessed to match the csv format. 

![mnist examples](files/mnist_examples.png)

### Data Processing
This system assumes the user has preprocessed their data beforehand. This includes converting data into CSV format.

Properly understanding and processing data is crucial in the field of machine learning. Here are a few resources that may help get started.

- [Data Preprocessing in Python](https://www.geeksforgeeks.org/data-preprocessing-machine-learning-python/)
- [How to Prepare Data for Machine Learning](https://machinelearningmastery.com/how-to-prepare-data-for-machine-learning/)
- [Data Processing: Data Types](https://medium.com/ai%C2%B3-theory-practice-business/the-engineers-guide-to-machine-learning-data-processing-data-types-ba40e6bf8765)
- [Data Preprocessing using Scikit Learn](https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/)
- [ML Data Preprocessing](https://medium.com/@techspecialistacademy/machine-learning-ml-data-preprocessing-d968f86b703)

## Examples
These are two baseline networks manually built using Keras and TensorFlow. Running the scripts trains them on the MNIST
dataset and displays their accuracy.

```bash
python -m examples.keras_baseline
python -m examples.tf_baseline
```

After building a network, you can test it on some custom hand-written numbers by running
```bash
python -m examples.number_prediction
```
