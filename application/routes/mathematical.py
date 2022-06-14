from pprint import pprint
from typing import Optional

from fastapi import APIRouter
import requests
from sympy import init_session, log, latex, init_printing, symbols, ln, solve
import numpy as np # import log10, log2, pi  # This will import math module

from IPython.display import display, Latex
from sympy import *

router = APIRouter()


@router.get("")
async def test():
    x = symbols('x')
    display(x)
    print("log10(100) : ", np.log10(100))
    print("log10(10) : ", np.log10(10))
    print("log10(2) : ", np.log10(2))
    print("log2(2) : ", np.log2(2))
    print("log2(16) : ", np.log2(16))
    int_x = Integral(cos(x) * exp(x), x)
    display(log(x).subs(x,16))
    result = "$${} = {}$$".format(latex(int_x), latex(int_x.doit()))
    pprint(display(Latex(result)))
    return
