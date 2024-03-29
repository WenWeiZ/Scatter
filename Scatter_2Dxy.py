'''
    三角基MoM计算二维物体远场散射，直角坐标
'''
import numpy as np 
import numpy.matlib
import numpy.linalg
from scipy import special
from matplotlib import pyplot as plt


def Center(point_array):
    '''
        取中点，返回序列
    '''
    num = len(point_array)
    c_point = []
    
    for n in range(num-1):
        c_point.append(((point_array[n][0]+point_array[(n+1)][0])/2, (point_array[n][1]+point_array[(n+1)][1])/2))
    c_point.append(((point_array[0][0] + point_array[-1][0])/2, (point_array[0][1]+point_array[-1][1])/2))

    return c_point 


def Distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def Delta(point_array):
    '''
        点与点距离序列
    '''
    num = len(point_array)
    delta = []

    for n in range(num-1):
        x1, y1 = point_array[n][0], point_array[n][1]
        x2, y2 = point_array[n+1][0], point_array[n+1][1]
        delta.append(np.sqrt((x1-x2)**2 + (y1-y2)**2))
    x1, y1 = point_array[-1][0], point_array[-1][1]
    x2, y2 = point_array[0][0], point_array[0][1]
    delta.append(np.sqrt((x1-x2)**2 + (y1-y2)**2))
    return delta

def matrix_Z(c_point, delta_point, k):

    gamma = 1.78107
    M = len(c_point)
    matrix = numpy.matlib.ones((M, M), dtype=complex)

    for m in range(M):
        for n in range(M):
            if m == n:
                matrix[m, n] = delta_point[n] * (1 - 1.j*(2/np.pi)*(np.log((gamma*k*delta_point[n])/4) - 1)) 
            else:
                #matrix[m, n] = delta_point[n] * special.hankel2(0, k*Distance(c_point[m], c_point[n]))
                matrix[m, n] = delta_point[n] * (special.j0(k*Distance(c_point[m], c_point[n])) - 1.j*special.y0(k*Distance(c_point[m], c_point[n]))) 

    return matrix


def matrix_V(c_point, k):
    M =  len(c_point)
    matrix = numpy.matlib.ones((M, 1), dtype=complex)

    for m in range(M):
        matrix[m, 0] = np.exp(-1.j*k*c_point[m][0])

    return matrix 

def alpha(n, c_point, delta_point, k):
    M =  len(c_point)
    matrix = numpy.matlib.ones((1, M), dtype=complex) 

    for m in range(M):
        R = np.sqrt(c_point[m][0]**2 + c_point[m][1]**2)
        matrix[0, m] = special.jv(n, k*R) * np.exp(-1.j*n*(np.arctan(c_point[m][1]/c_point[m][0]) + np.pi*(c_point[m][0] < 0))) * delta_point[m]

    return matrix   

def Cn(n, c_point, delta_point, k, I):
	alpha_nm = alpha(n, c_point, delta_point, k)
	return 1/((-1.j) ** n) * alpha_nm * I

def RCS(phi, I, c_point, delta_point, k):
    result = 0
    num = len(c_point)
    for n in range(num):
        result += I[n, 0] * np.exp(1.j * k * (c_point[n][0]*np.cos(phi)+c_point[n][1]*np.sin(phi))) * delta_point[n]

    return abs(result)**2


if __name__ == '__main__':


    number_of_point = 512
    kwave = 2*np.pi

    phi = np.arange(number_of_point) / number_of_point * 2*np.pi 
    #rho = np.random.rand(number_of_point) + 0.5
    rho = np.ones(number_of_point)

    point = []
    for n in range(number_of_point):
        point.append((rho[n]*np.cos(phi[n]), rho[n]*np.sin(phi[n])))
    c_point = Center(point)

    delta_point = Delta(point)

    Z = matrix_Z(c_point, delta_point, kwave)
    V = matrix_V(c_point, kwave)

    I = np.linalg.inv(Z) * V


    c0 = Cn(1, c_point, delta_point, kwave, I)
    print(c0)
    print(special.jv(1, kwave) / special.hankel2(1, kwave))
'''
    #RCA画图
    x = np.arange(0, 360) / 360 * 2*np.pi
    y = []

    for n in range(360):
        y.append(RCS(x[n], I, c_point, delta_point, kwave))

    x = [i/np.pi*180 for i in x]

    y = 10 * np.log10(y)
    plt.plot(x, y)
    plt.show()
'''
	





