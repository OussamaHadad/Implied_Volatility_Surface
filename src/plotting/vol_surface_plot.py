import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import griddata

def generate_iv_surface(data: pd.DataFrame, ticker: str, interpolation_method: str = "linear", plot: bool = False):
    """
    Generate a smooth implied volatility surface and optionally display it.

    Args:
        data (pd.DataFrame): Must contain columns ['strike', 'timeToMaturity', 'impliedVolatility']
        ticker (str): The asset ticker symbol.
        interpolation_method (str): 'linear', 'cubic', or 'nearest'
        plot (bool): If True, display the figure with fig.show(); otherwise return it.

    Returns:
        fig_plotly (plotly.graph_objects.Figure): The generated Plotly figure.
    """
    # --- Data preparation ---
    X_Y = data[['strike', 'timeToMaturity']].values
    Z = data['impliedVolatility'].values * 100  # Convert to percentage

    strike_grid = np.linspace(data['strike'].min(), data['strike'].max(), 80)
    time_grid = np.linspace(data['timeToMaturity'].min(), data['timeToMaturity'].max(), 80)
    K_grid, T_grid = np.meshgrid(strike_grid, time_grid)

    vol_grid = griddata(X_Y, Z, (K_grid, T_grid), method=interpolation_method)

    # --- Plotly 3D surface ---
    fig_plotly = go.Figure(data=[
        go.Surface(
            x=K_grid,
            y=T_grid,
            z=vol_grid,
            colorscale='Viridis',
            colorbar=dict(title='Implied Volatility (%)'),
        )
    ])

    fig_plotly.update_layout(
        title=f"{ticker} Implied Volatility Surface (Interactive)",
        scene=dict(
            xaxis_title='Strike ($)',
            yaxis_title='Time to Maturity (years)',
            zaxis_title='Implied Volatility (%)',
        ),
        autosize=True,
        template="plotly_dark"
    )

    # --- Show or return ---
    if plot:
        fig_plotly.show()
    else:
        return fig_plotly
