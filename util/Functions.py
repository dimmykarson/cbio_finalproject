import os, csv
import numpy as np
import matplotlib.pyplot as plt
script_dir = os.path.dirname(__file__)


def empty(v):
    return v==None or len(v)==0

def plot_file(file_path):
    #abs_file_path = os.path.join(script_dir, file)
    file = open(file_path, "r")
    x = []
    y = []
    reader = csv.reader(file, delimiter=";")
    for r in reader:
        x.append(int(r[0]))
        y.append(float(r[1]))
    plt.plot(x, y)
    plt.yscale('log')
    return plt

def plot_array(plot, array):
    x = []
    y = []
    for r in array:
        x.append(int(r[0]))
        y.append(float(r[1]))
    plot.plot(x, y)
    plot.yscale('log')
    return plot
#plot("result_10000_100_70_30_0_.txt")


