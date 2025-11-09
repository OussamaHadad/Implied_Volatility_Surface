import numpy as np
from scipy.stats import norm


def bs_eur(S: float, K: float, r: float, q: float, sigma: float, T: float, option_type = "call") ->  float:
    """
    Closed-form solution of the Black-Scholes equation for European Call Options.

    Arguments:
        S (float): Current asset price
        K (float): Strike price
        r (float): Risk-free interest rate
        q (float): Dividend yield (continuous)
        sigma (float): Volatility
        T (float): Time to expiration / Maturity (in years)

    Returns:
        C_bs (float): European Call Option price
    """
    if T < 0 or sigma < 0:
      return np.nan

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == "call":
        return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

