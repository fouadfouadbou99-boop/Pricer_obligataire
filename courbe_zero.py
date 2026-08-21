import numpy as np
from scipy.interpolate import interp1d

class ZeroCurve:
    def __init__(self, tenors, rates):
        self.tenors=np.array(tenors)
        self.rates=np.array(rates)
        self.curve=interp1d(self.tenors,self.rates,kind="linear",fill_value="extrapolate")

    def get_rate(self,maturity):
        return float(self.curve(maturity))

    def discount_factor(self,maturity):
        r=self.get_rate(maturity)
        return 1/((1+r)**maturity)
