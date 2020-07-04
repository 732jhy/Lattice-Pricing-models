# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 23:27:55 2020

@author: Justin Yu, M.S. Financial Engineering, Stevens Institute of Technology

Binomial Asset Pricing Model for European and American call and put options
"""

import numpy as np

def bapm(S0, K, r, sigma, T, n, CallPut, EurAm):
    '''
    Additive Binomial Tree pricing algorithm for European and American calls and puts
    
    Args:
        S0 - initial stock price
        K - strike price
        r - risk-free rate
        sigma - volatility
        n - number of time steps
        CallPut - 'Call' or 'Put'
        EurAm - 'European; or 'American''
        
    Returns the option price estimated by the binomial tree
    '''
    deltaT = T/n
    u = np.exp(sigma*np.sqrt(deltaT));    d = 1/u
    p = (np.exp(r*deltaT) - d)/(u - d);    q = 1- p   
    underlying = np.zeros((n+1,n+1))
    underlying[0,0] = S0
    
    for i in range(1, n+1):
        underlying[i,0] = underlying[i-1,0]*u
        for j in range(1,i+1):
            underlying[i,j] = underlying[i-1,j-1]*d
    
    optionval = np.zeros((n+1,n+1))
    
    for i in range(n+1):
        if CallPut == 'Call':
            optionval[n,i] = max(0, underlying[n,i] - K)
        elif CallPut == 'Put':
            optionval[n,i] = max(0, K - underlying[n,i])
    
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            if CallPut == 'Call' and EurAm == 'American':    
                optionval[i,j] = max(0, underlying[i,j]-K, np.exp(-r*deltaT)*(p*optionval[i+1,j]+q*optionval[i+1,j+1]))
            elif CallPut == 'Put' and EurAm == 'American':
                optionval[i,j] = max(0, K-underlying[i,j], np.exp(-r*deltaT)*(p*optionval[i+1,j]+q*optionval[i+1,j+1]))
            elif CallPut == 'Call' and EurAm == 'European':
                optionval[i,j] = np.exp(-r*deltaT)*(p*optionval[i+1,j]+q*optionval[i+1,j+1])         
            elif CallPut == 'Put' and EurAm == 'European':
                optionval[i,j] = np.exp(-r*deltaT)*(p*optionval[i+1,j]+q*optionval[i+1,j+1])
    
    return optionval[0,0]





















