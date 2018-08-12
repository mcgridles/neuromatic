# neuromatic

Neural network visualization and prototyping tool built using Keras and TKinter.

![neuromatic window](files/window_example.png)

### Usage
```bash
cd /path/to/neuromatic

python -m interface.window
```

### Data
A CSV formatted version of the MNIST dataset is included with this project under `neuromatic/files/mnist.csv.zip`. 

### Examples
These are two baseline networks manually built using Keras and TensorFlow. Running the scripts trains them on the MNIST dataset and displays their accuracy.

```bash
python -m examples.keras_baseline
python -m examples.tf_baseline
```

### Integration Test
Test to show end-to-end script generation and model training.
```bash
python -m tests.end_to_end
```