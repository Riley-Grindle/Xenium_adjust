import sys
import io
from alive_progress import alive_bar
import math
import numpy as np
import itertools
from sympy import symbols, Eq, solve


with open(sys.argv[1], "r") as tx_file:
    transcripts = tx_file.readlines()

boundaries = sys.argv[2]
boundaries = boundaries.split(",")

if (len(boundaries) != 8):
    print("Boundary coordinates do not match input format. See --help for details.")
    exit()


def vector_from_points(p1, p2):
    """Returns the vector from point p1 to point p2"""
    return np.array([p2[0] - p1[0], p2[1] - p1[1]])

def angle_between_vectors(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  
    return np.degrees(angle)

def get_boundary_eq(boundaries):

    numbers = [0,1,2]
    p1 = [float(boundaries[0]), float(boundaries[1])]
    p2 = [float(boundaries[2]), float(boundaries[3])]
    p3 = [float(boundaries[4]), float(boundaries[5])]
    p4 = [float(boundaries[6]), float(boundaries[7])]
    p_list = [p1, p2, p3, p4]

    connections = [[2,3,4],[1,3,4],[1,2,4],[1,2,3]]
    vectors   = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    x_range = []
    y_range = []
    for i in range(len(connections)):
        for j in range(len(connections[i])):
            if len(x_range) == 0 and len(y_range) == 0:
                x_range.append(p_list[i][0])
                x_range.append(p_list[i][0])
                y_range.append(p_list[i][1])
                y_range.append(p_list[i][1])
            else:
                if p_list[i][0] < x_range[0]:
                    x_range[0] = p_list[i][0]
                if p_list[i][0] > x_range[1]:
                    x_range[1] = p_list[i][0]
                if p_list[i][1] < y_range[0]:
                    y_range[0] = p_list[i][1]
                if p_list[i][1] > y_range[1]:
                    y_range[1] = p_list[i][1]
                            
            vectors[i][j] = vector_from_points(p_list[i], p_list[connections[i][j]-1])
    
    max_angle = 0
    combos = list(itertools.combinations(numbers, 2))
    selected = []
    for i in range(len(vectors)):
        max_angle = 0
        selected = []
        for j in range(len(vectors[i])):
            angle = angle_between_vectors(vectors[i][combos[j][0]], vectors[i][combos[j][1]])
            if angle > max_angle:
                max_angle = angle
                selected = [combos[j][0], combos[j][1]]
        for k in range(len(vectors[i])):
            if k in selected:
                pass
            else:
                vectors[i][k] = 0


    eq_list = set()
    key = 0
    for i in range(len(vectors)):
        for j in range(len(vectors[i])):
            if isinstance(vectors[i][j], np.ndarray):
                try:
                    slope = round((p_list[i][1] - p_list[connections[i][j]-1][1]) / (p_list[i][0] - p_list[connections[i][j]-1][0]), 4)
                except ZeroDivisionError:
                    slope = p_list[i][0]
                    key = 1
                if not key :
                    intercept = round((p_list[i][1] - (p_list[i][0] * slope)), 4)
                    x_lim = list([p_list[i][0], p_list[connections[i][j]-1][0]])
                    y_lim = list([p_list[i][1], p_list[connections[i][j]-1][1]])
                    eq_list.add(tuple([slope, intercept, tuple(sorted(x_lim)), tuple(sorted(y_lim))]))
                else:
                    key = 0
                    eq_list.add(tuple([slope, None, tuple([p_list[i][0], p_list[connections[i][j]-1][0]]), tuple([p_list[i][1], p_list[connections[i][j]-1][1]])]))

    rm_list = []
    for eq in eq_list:
        for comp_eq in eq_list:
            if eq[1] - comp_eq[1] > 0 and eq[1] - comp_eq[1] < 0.05 and eq[0] == comp_eq[0]:
                rm_list.append(eq)
    
    for eq in rm_list:
        eq_list.remove(eq)

    return eq_list, x_range, y_range



def find_ROI_transcripts(eq_list, x_range, y_range, point):
    
    eq_list = list(eq_list)

    point = [float(point[0]), float(point[1])]

    if round(point[0], 1) > x_range[0] and round(point[0], 1) < x_range[1] and round(point[1], 1) > y_range[0] and round(point[1], 1) < y_range[1]:
        key = 0
        y1 = None
        y2 = None
        for eq in eq_list:
            if None not in eq:
                if point[0] > eq[2][0] and point[0] < eq[2][1] and not key:
                    y1 = eq[0]*point[0] + eq[1]
                    key = 1
                if key and point[0] > eq[2][0] and point[0] < eq[2][1]:
                    y2 = eq[0]*point[0] + eq[1]
        
        if y1 is not None and y2 is not None:
            if point[1] > y1 and point[1] < y2:
                return True
            elif point[1] > y2 and point[1] < y1:
                return True
            else:
                return False
    else:
        return False


kept_transcripts = [None] * len(transcripts)
eq_list, x_lim, y_lim = get_boundary_eq(boundaries)
count = 0
total = len(transcripts)
with alive_bar(total) as bar:
    for line in transcripts:
        if count == 0:
            count += 1
            continue
        fields = line.split(",")
        x = fields[4].strip()
        y = fields[5].strip()
        if (find_ROI_transcripts(eq_list, x_lim, y_lim, [x,y])):
            kept_transcripts[count] = line
        count +=1 
        bar()

cleaned_list = list(filter(None, kept_transcripts))

transcript_writeable = "".join(cleaned_list)

with open("subset_transcripts.csv", "w") as  subset_tx_file:
    subset_tx_file.write(transcript_writeable)
subset_tx_file.close()
