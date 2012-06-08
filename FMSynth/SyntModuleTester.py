import sys
import SynthModule

MAX = 16
rate = 44100
chunk = 1024


if __name__ == "__main__":


    S0 = SynthModule.SynthModule()

    
    S0.add('s',0.25,0.1,0)

    S0.add('q',1.25,0.0004,0)

    S0.FM(2,1)

    S0.tone(3)
   

    

    
    
