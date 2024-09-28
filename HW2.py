import math
import random
import time
import matplotlib.pyplot as plt

def dot_v(A, B):
    S = 0
    for i in range(len(A)):
        S += A[i] * B[i]
    return S

def norm_v(A):
    return math.sqrt(dot_v(A, A))

def vec_v(A, B):
    V = []
    for i in range(len(A)):
        V.append(A[i] - B[i])
    return V  

def gaussian_kernel(A, B):
    return math.exp(-norm_v(vec_v(A, B)))

def random_generator_inRange(R):
    return random.uniform(0, R)

def unif(RangeDimension):
    return [random_generator_inRange(2 * math.pi) for _ in range(RangeDimension)]

def normal_generator(mean, variance):
    z0 = math.sqrt(-2.0 * math.log(random_generator_inRange(1))) * math.cos(random_generator_inRange(2 * math.pi))
    normal_random = mean + math.sqrt(variance) * z0
    return normal_random

def weights(d, RangeDimension, MEAN, VARIANCE):
    w = []
    for i in range(RangeDimension):
        w.append([normal_generator(MEAN, VARIANCE) for j in range(d)])
    return w
#-----------------------------------------------------------------------------Cos and offset method
def phi_hat(W, X, T, RangeDimension):
    phi = []
    for i in range(RangeDimension):
        phi.append(math.cos(dot_v(W[i], X) + T[i]) / math.sqrt(RangeDimension))
    return phi

#-----------------------------------------------------------------------------Sin-cos method
def phi_tilde(W, X, T, RangeDimension):
    phi = []
    for i in range(RangeDimension):
        phi.append(math.cos(dot_v(W[i], X) + T[i]) / math.sqrt(RangeDimension))
        phi.append(math.sin(dot_v(W[i], X) + T[i]) / math.sqrt(RangeDimension))
    return phi

def error_computer(x, p, d, m, variance, iteration, phi_status ="hat"):
    original_kernel = gaussian_kernel(x, p)
    error = []
    for i in range(iteration):
        t = unif(m)
        w = weights(d, m, 0, variance)

        if phi_status == "hat":
            phi_x = phi_hat(w, x, t, m)
            phi_p = phi_hat(w, p, t, m)
        elif phi_status == "tilde":
            phi_x = phi_tilde(w, x, t, m)
            phi_p = phi_tilde(w, p, t, m)
        approximate_kernel = dot_v(phi_x, phi_p)

        err = abs(original_kernel - approximate_kernel)
        error.append(err)
    
    return sum(error)/iteration

#------------------------------------------------------------------------------------
d = 4
x = [random.uniform(-1e-10, 1e+10) for i in range(d)]
p = [random.uniform(-1e-10, 1e+10) for i in range(d)]
variance = 1
m = 2

#------------------------------------------------------------------------------------
phi_status = "hat"
iter = 10
# Cal_Time = []
# First_Errors = []
# First_m = []
# for i in range(10):
# m = 2
x_axis_values = []
y_axis_values = []
t1 = time.time()
B = True
while True:
    value = error_computer(x, p, d, m, variance, iter, phi_status)
    x_axis_values.append(m)
    y_axis_values.append(value)
    if value < 0.01 and B == True:
        m_first = m
        value_first = value
        t2 = time.time()
        B = False
    if value < 0.005:
        break
    m += 1
    if m >= 3000:
        print("Calculation exceeds. m = ", m)
        break
    # Cal_Time.append(t2-t1)
    # First_Errors.append(value_first)
    # First_m.append(m_first)

# for i in range(10):
#     print("Dimension: ",First_m[i], " ErrorValues = ", First_Errors[i])
# print("time = ", t2-t1)

plt.figure("phi_hat_zoom")
plt.axis([-50, m+50, 0, 0.05])
colors = ['red' if y < 0.01 else 'blue' for y in y_axis_values]
plt.scatter(x_axis_values, y_axis_values, c=colors)
#plt.scatter(x_axis_values, y_axis_values)
#plt.plot([2, 0.01], [m, 0.01])
plt.xlabel('Dimension')
plt.ylabel('Error (phi_hat)')
plt.title('Random Fourier Features to approximate the Gaussian kernel\n ---------------- \n  ***RFF = cos and offset*** \n ---------------- \n  dimension = {}\n time = {}\n error = {}'.format(m_first, t2-t1, value_first))
plt.grid(True)


plt.figure("phi_hat")
colors = ['red' if y < 0.01 else 'blue' for y in y_axis_values]
plt.scatter(x_axis_values, y_axis_values, c=colors)
plt.xlabel('Dimension')
plt.ylabel('Error (phi_hat)')
plt.title('Random Fourier Features to approximate the Gaussian kernel\n ---------------- \n  ***RFF = cos and offset*** \n ---------------- \n  dimension = {}\n time = {}\n error = {}'.format(m_first, t2-t1, value_first))
plt.grid(True)

#------------------------------------------------------------------------------------
# phi_status = "tilde"
# iter = 4
# x_axis_values = []
# y_axis_values = []
# t1 = time.time()
# while True:
#     value = error_computer(x, p, d, m, variance, iter, phi_status)
#     x_axis_values.append(2*m)
#     y_axis_values.append(value)
#     if value < 0.005:
#         print("error = ", value)
#         print("dimension = ", 2*m)
#         break
#     m += 1
#     if m >= 7000:
#         print("Calculation exceeds. m = ", 2*m)
#         break
# t2 = time.time()
# print("time = ", t2-t1)

# plt.figure("phi_tilde")
# colors = ['red' if y < 0.01 else 'blue' for y in y_axis_values]
# plt.scatter(x_axis_values, y_axis_values, c=colors)
# plt.xlabel('Dimension')
# plt.ylabel('Error (phi_tilde)')
# plt.title('Random Fourier Features to approximate the Gaussian kernel\n ---------------- \n ***RFF = cos-sin*** \n ---------------- \n dimension = {}\n time = {}\n error = {}'.format(2*m, t2-t1, value))
# plt.grid(True)
#------------------------------------------------------------------------------------

plt.show()