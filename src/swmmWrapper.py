'''
Created on Jun 12, 2013

@author: mtryby
'''

from ctypes import windll, c_char_p, byref, c_double, c_float, c_int, create_string_buffer, sizeof
from os import chdir


class SwmmWrapper:
    
    def __init__(self):
        
        self.swmmlib = windll.LoadLibrary('w:\\HgRepo\\Adriatic\\swmm\\Release\\libswmm')
        
        
    def run(self, inputfile, reportfile, outputfile):

        swmm_run = getattr(self.swmmlib, 'swmm_run@12')
        err = swmm_run(c_char_p(inputfile.encode()),
                  c_char_p(reportfile.encode()),
                  c_char_p(outputfile.encode()))
        if (err):
            self._error_handler(err)


    def open(self, inputfile, reportfile, outputfile):

        swmm_open = getattr(self.swmmlib, 'swmm_open@12')
        err = swmm_open(c_char_p(inputfile.encode()),
                  c_char_p(reportfile.encode()),
                  c_char_p(outputfile.encode()))
        if (err):
            self._error_handler(err)


    def close(self):

        swmm_close = getattr(self.swmmlib, 'swmm_close@0')
        err = swmm_close()
        if (err):
            self._error_handler(err)


    def start(self, save_results):

        swmm_start = getattr(self.swmmlib, 'swmm_start@4')
        err = swmm_start(c_int(save_results))
        if (err):
            self._error_handler(err)


    def end(self):

        swmm_end = getattr(self.swmmlib, 'swmm_end@0')
        err = swmm_end()
        if (err):
            self._error_handler(err)


    def step(self):
        
        elapsed_time = c_double() 

        swmm_step = getattr(self.swmmlib, 'swmm_step@4')
        err = swmm_step(byref(elapsed_time))
        if (err):
            self._error_handler(err)

        return elapsed_time.value    


    def report(self):

        swmm_report = getattr(self.swmmlib, 'swmm_report@0')
        err = swmm_report()
        if (err):
            self._error_handler(err)

    
    def getMassBalErr(self):
        
        runoffErr = c_float()
        flowErr = c_float()
        qualErr = c_float()

        swmm_getMassBalErr = getattr(self.swmmlib, 'swmm_getMassBalErr@12')
        err = swmm_getMassBalErr(byref(runoffErr), byref(flowErr), byref(qualErr))
        if (err):
            self._error_handler(err)

        return (runoffErr.value, flowErr.value, qualErr.value)


    def getVersion(self):
        
        version = c_int()
        swmm_getVersion = getattr(self.swmmlib, 'swmm_getVersion@0')
        version = swmm_getVersion()
        return version.value

    
    def _error_handler(self, errcode):
        
        msgbuf = create_string_buffer(256)  
        swmm_getError = getattr(self.swmmlib, 'swmm_getError@12')
        swmm_getError(errcode, msgbuf, sizeof(msgbuf))
        print(msgbuf.value)

        
if __name__ == "__main__":
    chdir("w:\\HgRepo\\Adriatic\\swmm_wrapper\\example\\parking\\")
    
    swrap = SwmmWrapper()
    time = 0.0
    tend = 0.5

    swrap.open("parkinglot.inp","parkinglot.rpt","parkinglot.out")
    swrap.start(False)
    
    while(True):
        time = swrap.step()
        print(time)
        if (time <= 0.0):
            break

    swrap.end()
    swrap.report()
    swrap.close()
