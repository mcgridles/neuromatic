# Neuromatic

Neural network visualization and prototyping tool

## Setup
### For Unix Distributions Only
If running Neuromatic for the first time, all that is required is the installation of Python 3.6 and pip3. To set up your environment run `python3 setup.py install` to install all dependencies and modules. If an error occurs, run `pip3 install --upgrade tensorflow` followed by `python3 setup.py install`. To run the program run `python3 Neuromatic.py` in the main folder. 

### Usage
`TODO`

### Examples
```bash
python -m examples.keras_baseline
python -m examples.tf_baseline
```

### Integration Tests
```bash
python -m tests.test_end_to_end
```

### Unit Tests
```bash
nosetests
```
