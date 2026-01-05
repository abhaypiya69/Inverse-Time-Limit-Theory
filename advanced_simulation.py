import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (Normalized Units) ---
# Using Planck Units: c = 1, l_p = 1
L_P = 1.0          # Planck Length (The Static Boundary)
K_INV = 1.0        # Temporal Inversion Constant
DT = 0.01          # Time step
TOTAL_STEPS = 3000 # Duration

# --- PHYSICS ENGINE: RUNGE-KUTTA 4 (RK4) ---

def get_resistance(x):
    """Calculates the Temporal Resistance based on ITLT (Piya Equation)."""
    if x <= L_P:
        return 1e9 # Infinite resistance at or below boundary
    
    try:
        # T(x) = k / sqrt(1 - (lp/x)^2)
        factor = np.sqrt(1 - (L_P / x)**2)
        if factor < 1e-9: factor = 1e-9 # Avoid division by zero
        return K_INV / factor
    except:
        return 1e9

def derivatives(t, y, mode='standard'):
    """
    Defines the differential equation: dx/dt = velocity
    y[0] is position (x).
    """
    x = y[0]
    
    # Base infall velocity (modeling a singularity pull)
    # Simple model: Constant infall or Gravity 1/x^2. 
    # For clear comparison, we use a constant driven infall.
    v_base = 0.5 
    
    if mode == 'standard':
        # Standard Physics: Nothing stops the fall
        dx_dt = -v_base 
    elif mode == 'itlt':
        # ITLT Physics: Velocity is dampened by Temporal Resistance
        resistance = get_resistance(x)
        dx_dt = -v_base / resistance
        
    return np.array([dx_dt])

def rk4_step(t, y, dt, mode):
    """
    Performs one step of Runge-Kutta 4th Order Integration.
    This is the 'Gold Standard' for numerical simulations.
    """
    k1 = derivatives(t, y, mode)
    k2 = derivatives(t + dt/2, y + k1 * dt/2, mode)
    k3 = derivatives(t + dt/2, y + k2 * dt/2, mode)
    k4 = derivatives(t + dt, y + k3 * dt, mode)
    
    y_next = y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    return y_next

def run_simulation():
    print("Initializing RK4 High-Precision Simulation...")
    
    # Initial Conditions
    start_x = 5.0
    
    # State vectors: [position]
    state_std = np.array([start_x])
    state_itlt = np.array([start_x])
    
    # Data storage
    time_points = []
    hist_std = []
    hist_itlt = []
    
    t = 0.0
    
    for _ in range(TOTAL_STEPS):
        time_points.append(t)
        hist_std.append(state_std[0])
        hist_itlt.append(state_itlt[0])
        
        # 1. Update Standard Particle (RK4)
        if state_std[0] > 0:
            state_std = rk4_step(t, state_std, DT, mode='standard')
            if state_std[0] < 0: state_std[0] = 0.0 # Crash
        else:
            state_std[0] = 0.0
            
        # 2. Update ITLT Particle (RK4)
        if state_itlt[0] > L_P:
            state_itlt = rk4_step(t, state_itlt, DT, mode='itlt')
            if state_itlt[0] < L_P: state_itlt[0] = L_P # Freeze at boundary
        else:
            state_itlt[0] = L_P
            
        t += DT

    # --- PLOTTING ---
    plt.figure(figsize=(10, 6))
    
    # Standard
    plt.plot(time_points, hist_std, 'r--', label='Standard Physics (RK4)', alpha=0.6)
    
    # ITLT
    plt.plot(time_points, hist_itlt, 'b-', linewidth=2.5, label='ITLT (Piya Eq) with RK4')
    
    # Boundaries
    plt.axhline(y=L_P, color='g', linestyle=':', linewidth=2, label='Planck Length (Static Boundary)')
    plt.axhline(y=0, color='k', linewidth=1)
    
    plt.text(0.5, 0.1, 'Singularity (x=0)', color='black')
    plt.text(0.5, L_P + 0.15, 'Resolution Limit ($l_p$)', color='green')
    
    plt.title('High-Precision RK4 Simulation: Particle Dynamics\nStandard Model vs. Inverse Time Limit Theory')
    plt.xlabel('Time (t)')
    plt.ylabel('Radial Distance (r)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    print("Simulation Complete. Generating Graph...")
    plt.savefig('rk4_simulation_result.png')
    plt.show()

if __name__ == "__main__":
    run_simulation()
