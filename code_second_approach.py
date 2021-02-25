#!/usr/bin/env python
# coding: utf-8

import gurobipy as gp
from gurobipy import *
import numpy as np
from gurobipy import GRB

#generate data (weights)
def get_data(n,seed):
    np.random.seed(seed)
    w = np.absolute(np.random.randn(n,n))
    return w

get_data(4,0)

#invoke Gurobi to solve the LP
def solve_lp(n,seed):
    
    #model setup
    gm = gp.Model("maximum weight matching")
    
    #create the data
    w = get_data(n,seed)
    
    #create the objective function
    gm.modelSense = GRB.MAXIMIZE
    
    #set up the variables
    x = {}
    for i in range(n):
        for j in range(n):
            if j>i:
                x[i,j] = gm.addVar(obj=w[i][j], vtype=GRB.CONTINUOUS, lb=0, ub=1)
    
    #matching constraints
    for k in range(n):
        gm.addConstr(quicksum(x[i,k] for i in range(k))+quicksum(x[k,j] for j in range(k+1,n))<=1)
    
    
    #odd-set constraints of cardinality 3
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i<j:
                    if j<k:
                        #if there are two or more weights which are greater than or equal to 1
                        if w[j][k] >= 1 and w[i][k] >= 1:
                            gm.addConstr(x[i,j]+x[j,k]+x[i,k]<=1)   
                        if w[i][k] >= 1 and w[i][j] >= 1:
                            gm.addConstr(x[i,j]+x[j,k]+x[i,k]<=1) 
                        if w[i][j] >= 1 and w[j][k] >= 1:
                            gm.addConstr(x[i,j]+x[j,k]+x[i,k]<=1) 
    
    #odd-set constraints of cardinality 5
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    for m in range(n):
                        if i<j:
                            if j<k:
                                if k<l:
                                    if l<m:
                                        #if there are three or more weights which are greater than or equal to 1
                                        if w[i][m] >= 1 and w[j][k] >= 1 and w[k][l] >= 1:
                                            gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)
                                        if w[i][m] >= 1 and w[j][k] >= 1 and w[l][m] >= 1:
                                            gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)
                                        if w[i][j] >= 1 and w[k][l] >= 1 and w[i][m] >= 1:
                                            gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)
                                        if w[i][j] >= 1 and w[k][l] >= 1 and w[l][m] >= 1:
                                            gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)
                                        if w[i][j] >= 1 and w[j][k] >= 1 and w[l][m] >= 1:
                                            gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)                                


    #solve the model
    gm.update()
    gm.optimize()
  
    values = []
    for v in gm.getVars():
        values.append(v.x)
        
    unique_values = np.unique(np.array(values).round(decimals=3))
    print(seed)
    print(gm)
    return(unique_values)

solve_lp(4,0)

from datetime import datetime
start_time = datetime.now()
num_int = []
alist = []
for seed in range(100):
    alist.append(solve_lp(30,seed))
    #if integer solution
    if len(solve_lp(30,seed)) == 2 or len(solve_lp(30,seed)) == 1:
        num_int.append(solve_lp(30,seed))
probability = len(num_int)/100
print(probability)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

