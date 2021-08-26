'''
    三角基MoM计算二维物体远场散射，简化版本
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
    '''
    for n in range(num-1):
        c_point.append(((point_array[n][0]+point_array[(n+1)][0])/2, (point_array[n][1]+point_array[(n+1)][1])/2))
    c_point.append(((point_array[0][0] + point_array[-1][0])/2 + np.pi, (point_array[0][1]+point_array[-1][1])))

    return c_point 
    '''

    for n in range(num-1):
        x1, y1 = point_array[n][1]*np.cos(point_array[n][0]), point_array[n][1]*np.sin(point_array[n][0])
        x2, y2 = point_array[n+1][1]*np.cos(point_array[n+1][0]), point_array[n+1][1]*np.sin(point_array[n+1][0])
        rho = np.sqrt((x1 + x2) ** 2 / 4 + (y1 + y2) ** 2 / 4)
        phi = np.arctan((y1+y2) / (x1+x2))
        c_point.append((phi, rho))

    x1, y1 = point_array[0][1]*np.cos(point_array[0][0]), point_array[0][1]*np.sin(point_array[0][0])
    x2, y2 = point_array[-1][1]*np.cos(point_array[-1][0]), point_array[-1][1]*np.sin(point_array[-1][0])
    rho = np.sqrt((x1 + x2) ** 2 / 4 + (y1 + y2) ** 2 / 4)
    phi = np.arctan((y1+y2) / (x1+x2))

    c_point.append((phi, rho))   

    return c_point
def Center2(point_array):
    '''
        取中点，返回序列
    '''
    num = len(point_array)
    c_point = []

    for n in range(num-1):
        c_point.append(((point_array[n][0]+point_array[(n+1)][0])/2, (point_array[n][1]+point_array[(n+1)][1])/2))
    c_point.append(((point_array[0][0] + point_array[-1][0])/2 + np.pi, (point_array[0][1]+point_array[-1][1])))

    return c_point 


def Distance(p1, p2):
    return np.sqrt(p1[1]**2 + p2[1]**2 - 2*p1[1]*p2[1]*np.cos(p1[0]-p2[0]))

def Delta(point_array):
	'''
        点与点距离序列
	'''
	num = len(point_array)
	delta = []

	for n in range(num-1):
		phi1, r1 = point_array[n][0], point_array[n][1]
		phi2, r2 = point_array[n+1][0], point_array[n+1][1]
		delta.append(np.sqrt(r1**2 + r2**2 - 2*r1*r2*np.cos(phi1-phi2)))
	phi1, r1 = point_array[-1][0], point_array[-1][1]
	phi2, r2 = point_array[0][0], point_array[0][1]		
	delta.append(np.sqrt(r1**2 + r2**2 - 2*r1*r2*np.cos(phi1-phi2)))

	return delta

def matrix_Z(c_point, delta_point, k):

    gamma = 1.78107
    M = len(c_point)
    matrix = numpy.matlib.ones((M, M), dtype=complex)

    for m in range(M):
    	for n in range(M):
    		if m == n:
    			matrix[m, n] = delta_point[n] * (1 - 1.j*2/np.pi*(np.log((gamma*k*delta_point[n])/4) - 1))
    		else:
    			matrix[m, n] = delta_point[n] * special.hankel2(0, k*Distance(c_point[m], c_point[n]))

    return matrix


def matrix_V(c_point, k):
    M =  len(c_point)
    matrix = numpy.matlib.ones((M, 1), dtype=complex)

    for m in range(M):
        matrix[m, 0] = np.exp(-1.j*k*c_point[m][1]*np.cos(c_point[m][0]))

    return matrix 

def alpha(n, c_point, delta_point, k):
    M =  len(c_point)
    matrix = numpy.matlib.ones((1, M), dtype=complex) 

    for m in range(M):
        matrix[0, m] = special.jv(n, c_point[m][1]) * np.exp(-1.j*n*c_point[m][0]) * delta_point[m]

    return matrix   

def Cn(n, c_point, delta_point, k, I):
	alpha_nm = alpha(n, c_point, delta_point, k)
	return 1/((-1.j) ** n) * alpha_nm * I

if __name__ == '__main__':


    number_of_point = 209
    kwave = 2*np.pi

    phi = np.arange(number_of_point) / number_of_point * 2*np.pi 
    #rho = np.random.rand(number_of_point) + 0.5
    rho = np.ones(number_of_point)

    point = list(zip(phi, rho))
    c_point = Center(point)
    c_point2 = Center2(point)

    delta_point = Delta(point)

    Z = matrix_Z(c_point, delta_point, kwave)
    V = matrix_V(c_point, kwave)
    Z2 = matrix_Z(c_point2, delta_point, kwave)
    V2 = matrix_V(c_point2, kwave)


    I2 = np.linalg.inv(Z2) * V2
    I = np.linalg.inv(Z) * V


    c0 = Cn(0, c_point, delta_point, kwave, I)
    c1 = Cn(0, c_point, delta_point, kwave, I2)
    print(c0,c1)
    print(special.jv(0, kwave) / special.hankel2(0, kwave))

'''
    x = np.arange(0, 10, 0.1)
    y = special.hankel2(1, x)
    plt.plot(x, abs(y))
    plt.show()
'''
	




