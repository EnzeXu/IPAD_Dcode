import pickle

if __name__ == "__main__":
    with open("data.pkl", 'rb') as file:
        data = pickle.load(file)
    print(data.keys())
    print(data["params_config"])