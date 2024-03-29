import logging
import decimal

import azure.functions as func


def pi():
    """
    Compute Pi to the current precision.

    Examples
    --------
    >>> print(pi())
    3.141592653589793238462643383

    Notes
    -----
    Taken from https://docs.python.org/3/library/decimal.html#recipes
    """
    decimal.getcontext().prec += 2  # extra digits for intermediate steps
    three = decimal.Decimal(3)      # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    decimal.getcontext().prec -= 2
    return +s               # unary plus applies the new precision


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    len = req.params.get('len')
    if not len:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            len = req_body.get('len')

    decimal.getcontext().prec = int(len)+1 if len else 10000
    return func.HttpResponse(str(pi()))
