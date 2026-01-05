import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# INVERSE TIME LIMIT THEORY (ITLT) SIMULATION
# Author: Independent Researcher (Abhay)
# ==========================================

# 1. CONSTANTS (The Universe's Hardware Limits)
# ---------------------------------------------
l_p = 1.616255e-35  # Planck Length (meters) - The Spatial Limit
t_p = 5.391247e-44  # Planck Time (seconds) - The Temporal Baseline

# The Temporal Inversion Constant (k_inv)
# According to ITLT, this constant governs the time dilation at the quantum boundary.
k_inv = t_p 

# 2. THE MASTER EQUATION
# ----------------------
def calculate_time_dilation(x_factor):
    """
    Calculates Time Dilation T(x) based on the Inverse Time Limit Theory.
    Equation: T(x) = k_inv / sqrt(1 - (l_p/x)^2)
    
    Args:
    x_factor: Distance from center in multiples of Planck Length (e.g., 2 means 2*l_p)
    """
    # Boundary Condition: If x <= l_p, Time Resistance is Infinite.
    if x_factor <= 1:
        return float('inf') 
    
    # The Core Logic
    denominator = np.sqrt(1 - (1 / x_factor)**2)
    return k_inv / denominator

# 3. GENERATE DATA (Simulation)
# -----------------------------
print("Initializing Temporal Inversion Simulation...")

# Creating data points from 1.001 l_p (Near Boundary) to 10 l_p (Safe Zone)
x_factors = np.concatenate([
    np.linspace(1.001, 1.1, 50),   # High Resolution near the Static Boundary
    np.linspace(1.1, 2.5, 50),     # The Transition Zone
    np.linspace(2.5, 10.0, 50)     # The Classical Physics Zone
])
x_factors = np.sort(x_factors)

t_values = [calculate_time_dilation(xf) for xf in x_factors]
dilation_factors = [t / t_p for t in t_values]

# Save Data to CSV for Peer Review
df = pd.DataFrame({
    'Distance_Factor_(x/l_p)': x_factors,
    'Time_Dilation_Value_(s)': t_values,
    'Dilation_Ratio': dilation_factors
})
df.to_csv('itlt_data_export.csv', index=False)
print("Data exported to 'itlt_data_export.csv'")

# 4. PLOTTING THE GRAPH (Visual Proof)
# ------------------------------------
plt.figure(figsize=(12, 7))

# Plot the Curve
plt.plot(df['Distance_Factor_(x/l_p)'], df['Dilation_Ratio'], 
         color='#D32F2F', linewidth=2.5, label='Temporal Resistance Curve')

# Mark the Static Boundary (l_p)
plt.axvline(x=1, color='black', linestyle='-', linewidth=2, label='Static Boundary (l_p)')

# Mark the Phase Transition (2 l_p)
plt.axvline(x=2, color='green', linestyle='--', linewidth=2, label='Phase Transition (2 l_p)')

# Labels and Title
plt.title('The Inverse Time Limit Theory (ITLT): Temporal Behavior at Planck Scale', fontsize=14, fontweight='bold')
plt.xlabel('Distance from Singularity Center (multiples of l_p)', fontsize=12)
plt.ylabel('Time Dilation Factor (Relative to Planck Time)', fontsize=12)
plt.yscale('log') # Log scale to handle infinity
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend()

# Add Explanatory Text on Graph
plt.text(2.1, 2, 'Safe Zone\n(Classical Physics Begins)', fontsize=10, color='green')
plt.text(1.05, 10, 'Infinite Resistance\n(Event Horizon)', fontsize=10, color='red')

plt.savefig('itlt_graph.png')
print("Graph generated: 'itlt_graph.png'")
plt.show()
