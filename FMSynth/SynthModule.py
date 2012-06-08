import waveform
import OSC
import math
import numpy as N
import pyaudio
import array
import waveform
from numpy import linspace,sin,cos,pi,int16,float32


numbOsc=1
rate = 44100
chunk = 1024

p = pyaudio.PyAudio()


class SynthModule:



    def __init__(self):

        self.numOscillators = numbOsc
        self.oscs = [OSC.OSC('s',0.25,0.1,0.0)]
        
        
    
        
        
    def add(self,w,a,f,p):

        self.oscs.append(OSC.OSC(w,a,f,p))
        self.numOscillators += 1
        
    def osc(self,index):

        
        return self.oscs[index]

    def FM(self,i,j):
       
        self.oscs[i].set_FM(self.oscs[j])
        self.oscs[j].setmod(True)
               
        
       
    def PM(self,i,j):
        
        self.oscs[i].set_PM(self.oscs[j])
        self.oscs[j].setmod(True)

    def Print(self):

        for i in range(self.numOscillators):

            print("OSC(",self.oscs[i].get_wave(),self.oscs[i].get_freq(),i,")")

    def adjustlevel(self,index,newamp):

        self.oscs[index].set_amp(newamp)

    def adjustwave(self,index,newave):

        self.oscs[index].set_wave(newave)

    def adjustfreq(self,index,newf):

        self.oscs[index].set_freq(newf)
        

        
    def MixOut(self,data):

       
                        
        for i in range(self.numOscillators):


            out = 0.0
            

            if(self.oscs[i].is_carrier()==True):

                out += self.oscs[i].signal(data)
     
                      
                    
                

        return out


    def tone(self,seconds):

              
            p = pyaudio.PyAudio()
            stream = p.open(rate=44100,
                            channels=1,
                            format=pyaudio.paFloat32,
                            output=True)
            stream.write(array.array('f',(self.MixOut(i) for i in range(44100*seconds))).tostring())
            stream.close()
            p.terminate()

   

           

        

        

        
    

    

    
        
        
        
    
