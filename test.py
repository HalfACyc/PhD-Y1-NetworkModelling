import pickle


with open("Ref1-1000years-50.pkl", "rb") as file:
    d = pickle.load(file)

print(d)