import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

current_dir = os.getcwd()
dir_list = os.listdir(current_dir)


book_results = {
                'Ref1':[404,10,0.1],
                'Ref2':[361,8,0.1],
                'Ref3':[263,4,0.04]
}


pickle_files = []
for file in dir_list:
    if '.pkl' and 'plusamps' in file:
        pickle_files.append(file)

print(pickle_files)
print()
file = pickle_files[1]
print(file)


file_data = file.split('-')
topology = file_data[0]
years = file_data[1]
seeds = file_data[3]

with open(file, "rb") as file:
    d = pickle.load(file)

# print(d)
print(topology)

def print_data():
    for no_failures in d:
        # print(d[no_failures])
        scaled_data = np.array(d[no_failures]) / int(years)

        print('number of concurrent failures:', no_failures)
        print('number of seeds present in:',len(scaled_data))
        print('mean:',np.mean(scaled_data))
        print('variance:',np.var(scaled_data))
        print()



def plot_altogether():
    for no_failures in d:
        # print(d[no_failures])
        d[no_failures] = np.array(d[no_failures])/int(years)
        # print(d[no_failures])
        # print(no_failures)
        plot_array = d[no_failures]
        plt.plot(plot_array, np.full_like(plot_array, int(no_failures)), 'x', color='red')
        if topology in book_results:
            try:
                plt.plot(book_results[topology][int(no_failures)-1],int(no_failures),'.',color='blue')
            except:
                print('not possible')
            # print('yay')

    plt.title('Simulation results for '+topology+' without catastrophe')
    plt.xlabel('Average hours per year with N failed network links')
    plt.ylabel('Number of concurrent failed network links')
    plt.plot([],[],'x', color='red', label='Simulation Results')
    # plt.plot([],[],'.',color='blue',label='Textbook Result')
    plt.xscale('log')
    plt.axvline(x = 0.0876, color = "#307434", label = 'five nines', linestyle='--')
    plt.axvline(x = 0.00876, color = "#2AB5B9", label = 'six nines', linestyle='-.')
    plt.legend(loc='upper right')

    plt.show()

# print_data()
plot_altogether()