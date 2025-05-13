""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n):
    x_vals = [random.uniform(-1, 1) for item in range(n)]
    y_vals = [random.uniform(-1, 1) for item in range(n)]

    inside_x, inside_y = [], []
    outside_x, outside_y = [], []

    inside = 0
    for x, y in zip(x_vals, y_vals):
        if x**2 + y**2 <= 1:
            inside += 1
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)

    pi_approx = 4 * inside / n


    # Plotting
    plt.figure(figsize=(6, 6))
    plt.scatter(inside_x, inside_y, color='red', s=1, label='Inside Circle')
    plt.scatter(outside_x, outside_y, color='blue', s=1, label='Outside Circle')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f"Monte Carlo π Approximation\nn = {n}, π ≈ {pi_approx:.4f}")
    plt.legend()
    plt.savefig(f"pi_approximation_n{n}.png")
    plt.close()

    return pi_approx
            
        

def sphere_volume(n, d): #Ex2, approximation
    points = [[random.uniform(-1, 1) for item in range(d)] for item in range(n)] 
    inside = list( filter(lambda x: x <= 1,map(lambda point: sum(coord**2 for coord in point),  points)))

    # Step 3: Volume estimate = (fraction inside) * volume of cube = 2^d
    return (len(inside) / n) * (2 ** d)


def hypersphere_exact(d): #Ex2, real value
    return m.pi**(d / 2) / m.gamma(d / 2 + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    with future.ProcessPoolExecutor() as executor:
       results = executor.map(sphere_volume, [n]*np, [d]*np)

    return mean(results)

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):

    n_per_process = n // np
    with future.ProcessPoolExecutor() as executor:
        futures = [executor.submit(sphere_volume, n_per_process, d) for _ in range(np)]
        results = [f.result() for f in futures] 
    return mean(results)
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start = pc()
    sphere_volume_parallel1(n,d,np=10)
    stop = pc()
    print(f"Ex3: Paralel time of {d} and {n}: {stop-start}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start = pc()
    sphere_volume_parallel2(n, d, np=10)
    stop = pc()
    print(f"Ex4: Parallel time of {d} and {n}: {stop-start}")

    
    

if __name__ == '__main__':
	main()
