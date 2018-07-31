def read_data(file_path):
    train_size = 0.8

    data = pandas.read_csv(file_path)
    data = train.sample(frac=1).reset_index(drop=True)
    train_mask = np.random.rand(len(data)) < train_size

    X_train = data[train_mask].loc[data.columns != 'label']
    y_train = data[train_mask]['label']

    X_test = data[~train_mask].loc[data.columns != 'label']
    y_test = data[~train_mask]['label']
