from cbio_finalproject.util.Functions import *
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
rel_path = "result_ag_2000_10_70_30_2_False_.txt"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

plt = plot_file(abs_file_path)
plt.show()