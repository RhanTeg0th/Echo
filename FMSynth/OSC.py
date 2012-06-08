import sys
import math
import numpy as N
import pyaudio
import array
import waveform
from numpy import linspace,sin,cos,pi,int16,float32


Waveforms = {'s': waveform.sine, 'q': waveform.square, 't': waveform.triangle, 'w': waveform.sawtooth}

STAT = ['on','off']
STAT[0]= True
STAT[1]= False


class OSC:


    def __init__(self,waveform,amp,freq,phase):

               
        self.amp = amp
        self.freq = freq
        self.phase = phase
        self.carrierwaveform = waveform
        
        self.modwaveform = waveform
        self.modf = 0.0
        self.modph = 0.0
        self.modamp = 0.0
        
        
        self.FMstat = False
        self.PMstat = False
        self.mod = False
       
       

    def signal(self,input):

            
        t= input
        F = self.freq
        A = self.amp
        P = self.phase
        w = self.carrierwaveform
        
        m = self.modwaveform
        f = self.modf
        a = self.modamp
        p = self.modph

        
        FM = self.FMstat
        PM = self.PMstat

        
        
    
        if(FM==False and PM==False):
            
               output = Waveforms[w](F,t,A,P)

        elif(self.FMstat==True):
              
              output = Waveforms[w](F+(Waveforms[m](f,t,a,p)),t,A,P)

        elif(self.PMstat==True):

              output = Waveforms[w](F,t,A,Waveforms[m](f,t,a,p))

         
        
        
        return output

           
    
    def set_wave(self,wfr):

        self.carrierwaveform = wfr

    def set_freq(self,frequency):

        self.freq = frequency

    def set_amp(self,amplitude):

        self.amp = amplitude

    def set_phase(self,phaze):

        self.phase = phaze
        
    def get_freq(self):

        return self.freq

    def get_amp(self):

        return self.amp

    def get_phase(self):

        return self.phase

    def set_modw(self,W):

        self.modwaveform = W

    def set_modamp(self,A):

        self.modamp = A

    def set_modf(self,F):

        self.modfreq = F

    def set_modph(self,P):

        self.modph = P

   
    def set_FM(self,OSC):

        self.FMstat=True

        self.set_modw(OSC.get_wave())
        self.set_modf(OSC.get_freq())
        self.set_modamp(OSC.get_amp())
        self.set_modph(OSC.get_phase())
            

    def set_PM(self,OSC):

        self.PMstat=True

        self.set_modw(OSC.get_wave())
        self.set_modf(OSC.get_freq())
        self.set_modamp(OSC.get_amp())
        self.set_modph(OSC.get_phase())

        
        

    def FM(self):

        return self.FMstat

    def PM(self):

        return self.PMstat

    def get_wave(self):

        return self.carrierwaveform

    def setmod(self,flag):

        self.mod = flag
  

    def is_carrier(self):

        if(self.mod==False):

            return True

        elif(self.mod==True):

            return False

    

    

    
            
          
         


    

            

         
    

   








    
        
