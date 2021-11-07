import random
import nengo
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import nengo_dl
      

def createSpikingLines():
    lines = []
    labels = []
    for z in range(n):
        line, label = createLine(x,y, (z%3)*45)
        lines.append(line)
        labels.append(label)


    seed = random.random()
    random.seed(seed)
    random.shuffle(lines)
    random.seed(seed)
    random.shuffle(labels)

    return np.array(lines), np.array(labels)

def createLineX(x_size, y_size, n, ang_sep = 5):
    lines = np.zeros([n, y_size, x_size])
    labels = np.zeros(n)
    for t in range(n):
        angle = np.random.randint(0,90/ang_sep)*ang_sep
        labels[t] = angle
        cx = x_size/2
        cy = y_size/2
        for x in range(int(x_size/2)+1):
            lines[t, int(cy), int(cx)] = 1
            cx = cx + np.cos(angle*np.pi/180)
            cy = cy + np.sin(angle*np.pi/180)
            if cx > x_size-1:
                cx = x_size-1
            if cy > y_size-1:
                cy = y_size-1
        cx = x_size/2
        cy = y_size/2
        for x in range(int(x_size/2)+1):
            lines[t, int(cy), int(cx)] = 1
            cx = cx - np.cos(angle*np.pi/180)
            cy = cy - np.sin(angle*np.pi/180)
            if cx > x_size-1:
                cx = x_size-1
            if cy > y_size-1:
                cy = y_size-1

    return lines, labels
 


def createLine(x_size, y_size, angle=0):
    line = np.zeros([x_size,y_size])
    if angle == 0:
        line[int((x_size-1)/2),:] = 1
    if angle == 45:
        for x in range(y_size):
            line[x_size-1-x,x] = 1
    if angle == 90:
        line[:,int((y_size-1)/2)] = 1

    label = angle
    return line, label

def createLines(x, y, n):
    lines = []
    labels = []
    for z in range(n):
        line, label = createLine(x,y, (z%3)*45)
        lines.append(line)
        labels.append(label)


    seed = random.random()
    random.seed(seed)
    random.shuffle(lines)
    random.seed(seed)
    random.shuffle(labels)

    return np.array(lines), np.array(labels)

if __name__ == "__main__":
    #print(createLine(11,11,45))
    #lines = createLines(5,5,100)
    lines, labels = createLineX(12,12,12)
    #random.shuffle(lines[1])
    print(lines)
    print(labels)



# The lines/images should be input as a x by x image, not flattened
## Moves line in a continous direction, creates a label for that direction
def move_lines(lines, labels, randomDir = True, dir =0):
    
    #amount of timesteps it moves for, and creates "snapshots" from
    timesteps = 15

    #The two arrays that will get returned. Label and new "images/lines"
    dirs = np.zeros(lines.shape[0])
    moved_line = np.zeros([lines.shape[0],timesteps, lines.shape[1], lines.shape[2]])

    #For loop for each line that shall be moved
    for lnr, line in enumerate(lines,0):
        #Creates random direction for it to be moved in
        if randomDir == True:
            dir = np.random.randint(0,int(90/dir_amount))*dir_amount
        dirs[lnr] = dir

        # Finds original indexes for the line
        pos = np.where(lines==1)
        pos = np.asarray(pos)
        pos = pos.astype(int)

        #Creates first "image/line" in new array for first(zero) timestep
        moved_line[lnr, 0] = lines[lnr]
        
        #Goes through each timestep and moves positions of 1s / the line
        for x in range(timesteps-1):
            pos[0] = pos[0] + pos[0] * np.sin(dir*np.pi/180)
            pos[1] = pos[1] + pos[1] * np.cos(dir*np.pi/180)
            for xp, val in enumerate(pos,0):
                moved_line[lnr, x, int(pos[0][xp]), int(pos[1][xp])] = 1
    return moved_line, dirs
