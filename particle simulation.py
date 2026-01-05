import numpy as np
import matplotlib.pyplot as plt

def run_simulation():
    # --- CONFIGURATION (Normalized Units) ---
    # We use normalized units where Planck Length (l_p) = 1.0
    # This clearly demonstrates the logic without floating point underflow errors.
    l_p = 1.0
    k_inv = 1.0 # Temporal Inversion Constant

    # Simulation Parameters
    dt = 0.01  # Time step size
    total_steps = 2000
    start_distance = 5.0  # Start 5 units away from singularity

    # Arrays to store data
    time_axis = []
    dist_classical = []
    dist_itlt = []

    # Initial Conditions
    x_class = start_distance
    x_itlt = start_distance
    t = 0

    print("Starting Particle Infall Simulation...")

    for i in range(total_steps):
        time_axis.append(t)
        dist_classical.append(x_class)
        dist_itlt.append(x_itlt)
        
        # --- PHYSICS ENGINE ---
        
        # 1. Classical Gravity (Simplified Model)
        v_infall = 0.5 # Constant infall speed for demonstration
        
        # Move Classical Particle (It just falls to 0)
        if x_class > 0:
            x_class -= v_infall * dt
        else:
            x_class = 0 # Hit Singularity (Crash)
            
        # 2. ITLT Physics (Applying Piya Equation)
        # We calculate the Temporal Resistance Factor at current position x_itlt
        
        if x_itlt > l_p:
            # The Piya Equation: T(x) = k / sqrt(1 - (lp/x)^2)
            try:
                # The "Shielding" Term
                denominator = np.sqrt(1 - (l_p / x_itlt)**2)
                if denominator < 1e-9: denominator = 1e-9 
                
                time_resistance = k_inv / denominator
            except:
                time_resistance = 1e9 # Infinite resistance
                
            # The "Observed Velocity" is damped by Time Resistance
            # v_obs = v_local / T(x)
            v_observed = v_infall / time_resistance
            
            # Move ITLT Particle
            x_itlt -= v_observed * dt
            
        else:
            # If it hit the boundary, it freezes
            x_itlt = l_p

        t += dt

    # --- PLOTTING ---
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, dist_classical, 'r--', label='Standard Collapse (Singularity)', alpha=0.6)
    plt.plot(time_axis, dist_itlt, 'b-', linewidth=2.5, label='ITLT Trajectory (Piya Equation)')
    plt.axhline(y=l_p, color='g', linestyle=':', linewidth=2, label='Planck Length (Static Boundary)')
    plt.axhline(y=0, color='k', linewidth=1)
    
    plt.text(1.0, 0.1, 'Singularity (x=0)', color='black')
    plt.text(1.0, l_p + 0.1, 'Static Boundary ($l_p$)', color='green')

    plt.title('Simulation: Particle Infall Dynamics\nStandard Physics vs. Inverse Time Limit Theory')
    plt.xlabel('Time (Observer Steps)')
    plt.ylabel('Distance from Center (x)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('simulation_result.png')
    plt.show()

if __name__ == "__main__":
    run_simulation()
