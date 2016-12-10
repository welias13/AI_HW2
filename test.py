# 90274,18567

import subprocess
import main
import main2
import ways.graph
import abstract
import pickle as pkl
python_path_emad = "python"
python_path = "C:\\Users\\welias\\AppData\\Local\\Continuum\\Anaconda3\\python.exe"

source = 43333
target = 21150

Roads = ways.graph.load_map_from_csv()
# source = 86936
# target = 37951

# subprocess.call(python_path + " main2.py a_star 90274 18567", shell=True)
# subprocess.call(python_path + " main.py base 90274 18567",shell=True)

# subprocess.call(python_path_emad + " main2.py a_star " + str(source) + ' ' + str(target), shell=True)
# subprocess.call(python_path_emad + " main.py base " + str(source) + ' ' + str(target), shell=True)

# subprocess.call(python_path + " main2.py a_star_exp3 90274 18567 abstractSpace.pkl", shell=True)
# subprocess.call(python_path + " main.py bw 90274 18567 abstractSpace.pkl",shell=True)
#
# abstract.centrality(Roads)

# abstract.build_abstract_dict(Roads, k=0.005, m=0.1)
# file_name = "abstractSpace.pkl"
# #
# with open(file_name, 'rb') as pk:
#     abstractMap = pkl.load(pk)
# #
#
#
source = 712
target = 41761
print(main.base_exp(Roads, source, target))
print(main2.a_star_exp(Roads, source, target))

# print(main.betterWaze_exp(Roads, source, target, abstractMap))
# print(main2.a_star_exp3_aux(Roads, source, target, abstractMap, True))
