import sys
import math
import numpy as np
from numpy import linspace,sin,cos,pi,int16,float32





def sine(f,t,amp,ph):

   
    value = amp * math.sin(f*t)
    
    return value


def square(f,t,amp,ph):
    
     
     value = 0.0
     k = 32
     for n in range(k):
         
       p = (2*n)+1
       t = t + ph
       value = value + (math.pow(p,-1.0)*math.sin(p*f*t))
     
     value = value * amp
     return value


def triangle(f,t,amp,ph):
    
    
     k = 32
     value = 0.0
  
     for n in range(k):
         
       p = (2*n)+1
       t = t + ph
       value = value+ (math.pow(-1.0,n)*math.sin(p*f*t)*math.pow(p,-2.0))
     

     value = value * amp
     return value


def sawtooth(f,t,amp,ph):

      
      k = 32
      value = 0.0
      t = t + ph
      
      n = 1

      while n < 32:

          t = t + ph
          value = value + (math.pow(-1.0,n+1)*math.sin(n*f*t)*math.pow(n,-1.0))
          n = n+1
         

      value = value * amp
      return value

        
    
    

    
