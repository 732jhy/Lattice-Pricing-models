# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 23:48:28 2020

@author: Justin Yu, M.S. Financial Engineering, Stevens Institute of Technology

Trinomial tree pricing model for European and American call and put options
"""

import numpy as np

def tapm(S0,K,r,sigma,T,q,n,CallPut,EurAm):
    '''
    Trinomial Asset Pricing model for European and American Call and Put options
    
    Args:
        S0 - initial asset price
        K - strike price
        r - risk-free rate
        sigma - volatility
        T - time to maturity
        q - dividend rate
        n - number of time steps in the tree
        CallPut - 'Call' or 'Put'
        EurAm - 'European' or 'American'
    
    Returns the option price estimated by the trinomial tree
    '''
    deltaT = T/n  
    deltaX = np.sqrt(deltaT*(sigma**2) + ((r-q-0.5*sigma**2)**2)*(deltaT**2)) 
    u = np.exp(sigma*np.sqrt(3*deltaT));    d=1/u
    D = r-q-(0.5*sigma**2)
    
    #check for convergence
    if deltaX < sigma*np.sqrt(3*deltaT):
        deltaX = sigma*np.sqrt(3*deltaT)
    
    pu = 0.5*(((sigma**2*deltaT +D**2*deltaT**2)/deltaX**2) + (deltaT*D/deltaX))
    pm = 1 - ((deltaT*sigma**2 + D**2*deltaT**2)/deltaX**2)
    pd = 0.5*(((sigma**2*deltaT +D**2*deltaT**2)/deltaX**2) - (deltaT*D/deltaX))
    
    underlying = np.zeros((n+1,n+1,n+1))
    underlying[0,0,0] = S0
    
    for i in range(1,n+1):
        underlying[i,0,0] = underlying[i-1,0,0]
        
        for j in range(1,i+1):
            underlying[i,j,0] = underlying[i-1,j-1,0]*u
            
            for k in range(1,j+1):
                underlying[i,j,k] = underlying[i-1,j-1,k-1]*d
    
    optionval = np.zeros((n+1,n+1,n+1))   
    
    for i in range(n+1):
        for j in range(i+1):

            if CallPut == 'Call':
                optionval[n,i,j] = max(0, underlying[n,i,j] - K)
           
            elif CallPut == 'Put':
                optionval[n,i,j] = max(0, K - underlying[n,i,j])
    
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            for k in range(j+1):

                if CallPut == 'Call' and EurAm == 'European':
                    optionval[i,j,k] = np.exp(-r*deltaT)*(pu*optionval[i+1,j+1,k]+pm*optionval[i+1,j,k]+pd*optionval[i+1,j+1,k+1])              
    
                elif CallPut == 'Put' and EurAm == 'European':
                    optionval[i,j,k] = np.exp(-r*deltaT)*(pu*optionval[i+1,j+1,k]+pm*optionval[i+1,j,k]+pd*optionval[i+1,j+1,k+1])

                elif CallPut == 'Call' and EurAm == 'American':
                    optionval[i,j,k] = max(0, underlying[i,j,k]-K, np.exp(-r*deltaT)*(pu*optionval[i+1,j+1,k]+pm*optionval[i+1,j,k]+pd*optionval[i+1,j+1,k+1]))               

                elif CallPut == 'Put' and EurAm == 'American':
                    optionval[i,j,k] = max(0, K-underlying[i,j,k], np.exp(-r*deltaT)*(pu*optionval[i+1,j+1,k]+pm*optionval[i+1,j,k]+pd*optionval[i+1,j+1,k+1]))                    
    
    return optionval[0,0,0]






