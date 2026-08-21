from courbe_zero import ZeroCurve

def macaulay_duration(bond,curve):
    price=bond.price(curve)
    return sum(t*cf*curve.discount_factor(t) for t,cf in bond.cashflows())/price

def modified_duration(bond,curve):
    d=macaulay_duration(bond,curve)
    y=curve.get_rate(bond.maturity)
    return d/(1+y)

def convexity(bond,curve):
    price=bond.price(curve)
    return sum(cf*curve.discount_factor(t)*t*(t+1) for t,cf in bond.cashflows())/price

def dv01(bond,curve):
    shifted=ZeroCurve(curve.tenors, curve.rates+0.0001)
    return bond.price(shifted)-bond.price(curve)
