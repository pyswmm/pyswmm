
from swmmWrapper import SwmmWrapper
from timeit import timeit
from os import chdir

class TimingHarness:

    def __init__(self):

        self.wrap = SwmmWrapper()    
        self.nsteps = 0

        
    def initialize(self, inputfile, reportfile, outputfile):

        self.wrap.open(inputfile, reportfile, outputfile)
        self.wrap.start(True)


    def exec_steps(self):
        
        while(True):
            time = self.wrap.step()
            self.nsteps = self.nsteps + 1
            if (time <= 0.0):
                break

        return self.nsteps

    
    def cleanup(self):
        
        self.wrap.end()
        self.wrap.report()
        self.wrap.close()


if __name__ == "__main__":
    chdir("..\example\\user05\\")
    
    harness = TimingHarness()

    harness.initialize("user5.inp","user5.rpt","user5.out")

    time = timeit(stmt="harness.exec_steps()", number=1,
                  setup = "from __main__ import harness")
    
    harness.cleanup()
    
    print(time, harness.nsteps - 1, time/(harness.nsteps - 1))
    
