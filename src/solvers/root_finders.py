from typing import Callable
from src.models import *
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

# ---------- 1. Bisection Method ----------
def iv_bisection(C_market: float, S: float, K: float, r: float, q: float, T: float, 
                 pricing_func: Callable = bs_eur, sigma_min: float = 1e-10, sigma_max: float = 20, epsilon: float = 1e-7)  ->  float:
    """
    Compute the implied volatility of an option using the bisection method.
    Given a continuous function f, and two points a & b where f(a) < 0 and f(b) > 0, there exists c in (a, b) such that f(c) == 0 (assuming a < b).
    The bisection method uses this property by starting with an interval (a, b) where f(a) and f(b) have different signs, and keeps shrinking the interval
    until convergence to the root.

    Arguments:
        C (float): Call option's market price

    Returns:
        implied_volatility (float): When used as the volatility in the Black-Scholes solution it results in a Call Price equal to the market price
    """
    def objective(sigma: float) -> float:
        return pricing_func(S, K, r, q, sigma, T) - C_market

    assert objective(sigma_min) * objective(sigma_max) <= 0, f"The root isn't in the interval [{sigma_min}, {sigma_max}]. Try another interval."

    while True:
        m = (sigma_min + sigma_max) * 0.5

        if abs(objective(m)) < epsilon:
            return m
        elif objective(m) < 0:
            sigma_min = m
        else:
            sigma_max = m


# ---------- Black-Scholes Vega Function ----------
def bs_vega(S, K, r, q, sigma, T):
    """Derivative of the BS price wrt sigma (Vega)."""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# ---------- 2. Newton Raphson Method ----------
def iv_newton_raphson(C_market: float, S: float, K: float, r: float, q: float, T: float, 
                      pricing_func: Callable = bs_eur, iv_0: float = 1e-2, epsilon: float = 1e-5, max_iter: int = 500)  ->  float:
    """
    Compute the implied volatility of an option using the Newton-Raphson method.
    Newton-Raphson is an iterative method used to find an approximate solution of the equation f(x) = 0. Starting at an initial guess,
    we keep updating its value until convergence.

    Arguments:
        C_market (float): Call option's market price
        epsilon (float): If the the absolute difference between the market price and the black-scholes price is below this value then we assume convergence

    Returns:
        implied_volatility (float): When used as the volatility in the Black-Scholes solution it results in a Call Price equal to the market price
    """
    iv = iv_0
    for _ in range(max_iter):
        # compute model price
        C_bs = pricing_func(S, K, r, q, iv, T)
        if np.isnan(C_bs):
            return np.nan

        diff = C_bs - C_market
        if abs(diff) < epsilon:
            return iv

        vega = bs_vega(S, K, r, q, iv, T)
        if np.isnan(vega) or vega < 1e-8:
            break  # avoid division by zero

        iv -= diff / vega
        # keep volatility in a reasonable range
        if not np.isfinite(iv) or iv <= 0:
            break

    return np.nan  # did not converge


# ---------- 3. Brent Method ----------
def iv_brent(C_market: float, S: float, K: float, r: float, q: float, T: float, 
             pricing_func: Callable = bs_eur, sigma_min: float = 1e-6, sigma_max: float = 5.0) -> float:
    """
    Compute the implied volatility of an option using Brent's root-finding method.
    Brent's root-finding method is an iterative method used to find an approximate solution of the equation f(x) = 0. Starting at an initial guess,
    we keep updating its value until convergence.

    Returns:
        implied_volatility (float): When used as the volatility in the Black-Scholes solution it results in a Call Price equal to the market price
    """
    def objective(sigma):
        return pricing_func(S, K, r, q, sigma, T) - C_market

    # Theoretical bounds
    intrinsic_value = max(S * np.exp(-q * T) - K * np.exp(-r * T), 0)
    max_price = S * np.exp(-q * T)

    if not intrinsic_value <= C_market <= max_price:
        return np.nan

    try:
        return brentq(objective, sigma_min, sigma_max, maxiter = 200)
    except Exception:
        return np.nan