import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    ambi = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)

    total = [ambi[x]+diff[x]+spec[x] for x in range(3)]
    total = limit_color(total)
    # print(total)
    return total

def calculate_ambient(alight, areflect):
    ambient = []
    for x in range(3):
        ambient.append(alight[x]*areflect[x])
    return ambient

def calculate_diffuse(light, dreflect, normal):
    diffuse = []
    normalize(light[0])
    normalize(normal)
    for x in range(3):
        diffuse.append(dreflect[x]*max(0, dot_product(normal, light[0]))*light[1][x])
    return diffuse


def calculate_specular(light, sreflect, view, normal):
    specular = []
    sum = [view[x]+light[0][x] for x in range(3)]
    normalize(sum)
    normalize(normal)

    for x in range(3):
        specular.append(sreflect[x]*(dot_product(normal,sum))**SPECULAR_EXP*light[1][x])
    print(specular)
    return specular

def limit_color(color):
    # print(color)
    new = [int(x) if x < 255 else 255 for x in color]
    return new

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
