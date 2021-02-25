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

#model 1

#invoke Gurobi to solve the LP
def solve_lp_1(n,seed):
    
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
                
    #solve the model
    gm.update()
    gm.optimize()

    values = []
    for v in gm.getVars():
        values.append(v.x)
        
    unique_values = np.unique(values)
    #print(unique_values)
    print(seed)
    
    return(gm)

#model 2

#invoke Gurobi to solve the LP
def solve_lp_2(n,seed):
    
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
                        gm.addConstr(x[i,j]+x[j,k]+x[i,k]<=1)   
                
    #solve the model
    gm.update()
    gm.optimize()

    values = []
    for v in gm.getVars():
        values.append(v.x)
        
    unique_values = np.unique(values)
    #print(unique_values)
    print(seed)
    
    return(gm)

#model 3

#invoke Gurobi to solve the LP
def solve_lp_3(n,seed):
    
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
                                        gm.addConstr(x[i,j]+x[j,k]+x[k,l]+x[l,m]+x[i,m]<=2)

                
    #solve the model
    gm.update()
    gm.optimize()

    values = []
    for v in gm.getVars():
        values.append(v.x)
        
    unique_values = np.unique(values)
    print(seed)
    
    return(gm)

from datetime import datetime
start_time = datetime.now()

num_int = []
alist = []
num_constrs = []
#solve 100 times
for seed in range(100):
    model = solve_lp_1(30,seed)
    values = []
    for v in model.getVars():
        values.append(v.x)
    #get list of unique values
    unique_values = np.unique(np.array(values).round(decimals=3))
            
    if len(unique_values) == 2:
        alist.append(unique_values)
        num_constrs.append("1")
    #if we don't have an integer solution
    if len(unique_values) > 2:
        #see if integer solution from model with odd-set constraints of cardinality 3
        model2 = solve_lp_2(30,seed)
        values_2 = []
        for v in model2.getVars():
            values_2.append(v.x)
        unique_values_2 = np.unique(np.array(values_2).round(decimals=3))
        
        if len(unique_values_2) == 2:
            alist.append(unique_values_2)
            num_constrs.append("2")
        #if we don't have an integer solution
        if len(unique_values_2) > 2:
            #see if integer solution from model with odd-set constraints of cardinalities 3 and 5
            model3 = solve_lp_3(30,seed)
            values_3 = []
            for v in model3.getVars():
                values_3.append(v.x)
            unique_values_3 = np.unique(np.array(values_3).round(decimals=3))
                
            alist.append(unique_values_3)
            num_constrs.append("3")  

for element in alist:
    if len(element) == 2:
        num_int.append(element)
    
probability = len(num_int)/100
print(probability)
print(num_constrs)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

