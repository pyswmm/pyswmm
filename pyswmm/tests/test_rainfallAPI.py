from pyswmm import Simulation
from pyswmm.tests.data import MODEL_RAIN

def test_rainfall():
    sim = Simulation(MODEL_RAIN)
    sim._model.swmm_start()
    check = 0
    
    for i in range(0, 100):
        sim._model.setGagePrecip("Gage1", 10.00)
        sim._model.swmm_step()
        x,_,_ = sim._model.getGagePrecip("Gage1")
        if  x == 10.0:
            check += 1
        print(x)
    
    sim._model.swmm_end()
    sim._model.swmm_close()
    assert(check > 10)

