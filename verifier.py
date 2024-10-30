
import json
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

# Sample JSON structure as string (replace this with JSON loading if from file)
ip = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 9, 2, 3],
  ]

op = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 9, 2, 3],
  ]

exp_op = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 9, 5, 7],
  ]

def color_to_bin(color):
    bin_col = 0

    if color == 0 :
        bin_col = 0
    elif color == 1:
        bin_col = 2
    elif color == 2:
        bin_col = 4
    elif color == 3:
        bin_col = 8
    elif color == 4:
        bin_col = 16
    elif color == 5:
        bin_col = 32
    elif color == 6:
        bin_col = 64
    elif color == 7:
        bin_col == 128
    elif color == 8:
        bin_col = 256
    elif color == 9:
        bin_col = 512
    else:
        bin_col = 1024

    return bin_col


def shape_color_to_bin(color_shape):

    rows = len(color_shape)  # Number of rows
    cols = len(color_shape[0]) if rows > 0 else 0  # Number of columns
    converted_shape = np.zeros((rows, cols))
    for col in range(cols):
        for row in range(rows):
            converted_shape[row][col] = color_to_bin(color_shape[row][col])

    return converted_shape

# Function to compare matrices
def compare_matrices(mat1, mat2):

    rows = len(mat1)  # Number of rows
    cols = len(mat1[0]) if rows > 0 else 0  # Number of columns

    rows2 = len(mat2)  # Number of rows
    cols2 = len(mat2[0]) if rows2 > 0 else 0  # Number of columns

    #Check sizes match
    if cols - cols2 != 0 :
        #throw error
        raise ValueError("Matrices do not have the same number of columns")

    if rows - rows2 != 0 :
        #throw error
        raise ValueError("Matrices do not have the same number of rows")
    
    differences = np.zeros((rows, cols))

    #Bitwise XOR
    for col in range(cols):
        for row in range(rows):
            differences[row][col] = int(mat1[row][col]) ^ int(mat2[row][col])
    return differences


def visualizer(input, output, exp_output, diff):

    #Color map
    colors = ["black", "cyan", "red", "green", "yellow", "gray", "magenta", "orange", "azure", "brown", "white"]
    colors2 = ["black", "red"]
    bounds = [0, 1, 2, 4, 8,16,32,64,128,256,512,1024]
    bounds2 = [0, 1]
    cmap = ListedColormap(colors)
    cmap2 = ListedColormap(colors2)
    norm = BoundaryNorm(bounds, cmap.N)
    norm2 = BoundaryNorm(bounds2, cmap2.N)

    
    # Create a 3x1 grid of subplots
    fig, axs = plt.subplots(4, 1, figsize=(8, 8))

    axs[0].imshow(input, cmap=cmap, norm=norm)
    axs[0].set_title("Input")

    axs[1].imshow(output, cmap=cmap, norm=norm)
    axs[1].set_title("Output")

    axs[2].imshow(exp_output, cmap=cmap, norm=norm)
    axs[2].set_title("Expected Output")

    #Need a difference Cmap here
    axs[3].imshow(diff, cmap=cmap2, norm=norm2)
    axs[3].set_title("Error")

    #plt.colorbar()  
    plt.show()

    return

# This is the verifier 
def verifier (ip, op, exp_op, visual_flag):
    ip_c = shape_color_to_bin(ip)
    op_c = shape_color_to_bin(op)
    exp_op_c = shape_color_to_bin(exp_op)
    differences = compare_matrices(op_c, exp_op_c)
    if(visual_flag):
        visualizer(ip_c, op_c, exp_op_c, differences)


#main
verifier(ip,op,exp_op,True)







