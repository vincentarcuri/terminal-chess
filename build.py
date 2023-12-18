import os


current_directory = os.getcwd()

PATH = os.path.join(current_directory, "cpp_chess")
os.chdir(PATH)

FILES = [
    'Pieces2',
    'Board2',
    'Game',
    'search',
    'shared',
    #'tests'
]

os.system(f"gcc -fPIC -shared -o  shared.so {'.cpp '.join(FILES)}.cpp -std=c++20 -lstdc++")