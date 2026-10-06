import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter #PillowWriter
from scipy.linalg import eigh
from scipy.io import wavfile # for sound waves

# Atomic base units:
hbar = 1  # reduced Planck constant
m_e = 1  # mass of electron

# Convenient units in terms of atomic units:
angs = 1 / 0.529177  # length
fs = 1 / (1e15 * 2.4188843265864e-17)  # time
ev = 1 / 27.211386245988  # energy

pi = math.pi

mu = 1 * m_e # reduced mass

well_depth = 2

# Variables needed for the potential energy term:
e0 = well_depth * ev
dr = 0.3 * angs
r = np.arange(-35 * angs, 35 * angs, dr)
r_l = 45 * angs
r_r = 5 * angs

pes = -e0 * (1 - np.heaviside(r - r_r /2, 0.5)) * np.heaviside(r + r_l /2, 0.5)

# For fast expansion, speed_coeff = 4.5, for slow expansion, speed_coeff = 0.5
speed_coeff = 0.5

expansion_distance = 20 * angs

# === Define Kinetic Energy and Potential Energy Equations (Do Not Change) === #

# Kinetic energy prefactor
kin_e_prefactor = -(1 / (dr ** 2)) * hbar ** 2 / (2 * mu)

# Hamiltonian
ham = np.diag(-2 * kin_e_prefactor + pes) + np.diag(kin_e_prefactor * np.ones(len(r) - 1), 1) + np.diag(kin_e_prefactor * np.ones(len(r) - 1), -1)
# === END === #

# === Solve Hamiltonian for Eigenvalues: Energies and Wave Function (Psig) (Do Not Change) === #
energies, wavefuncs = eigh(ham)
eg = np.diag(energies)
psi_g = wavefuncs[:, 0]
# === END === #

# === Define Expanding Box === #
dt = 0.01 * fs

# For fast expansion, speed_coeff = 4.5, for slow expansion, speed_coeff = 0.5
velocity = speed_coeff * angs / fs

expansion_distance = 20 * angs
t_final = (2 * expansion_distance) / velocity
#t = np.arange(0, t_final + 100 * fs, dt)
t = np.arange(0, t_final + 1 * fs, dt)
# === END === #

psi = psi_g.copy()


# === Initialize plot (Do Not Change) === #
fig, ax = plt.subplots(1, 3, figsize=(10, 4), constrained_layout=True)
ax[0].set_xlim(r[0] / angs + 5, r[-1] / angs)
ax[0].set_ylim(-well_depth-0.5, 0.5)
#wave_plot, = ax[0].plot([], [], lw=2, label="Wave Function")
wave_plot, = ax[0].plot([], [], lw=2, label=r'$\psi^2$ (25x)') # %%
pes_plot, = ax[0].plot([], [], lw=2, label="Potential Energy")

ax[0].set_ylabel("Energy [eV]", fontsize=12)
ax[0].set_xlabel("Distance [Å]", fontsize=12)
ax[0].legend(loc="upper left", fontsize=8)

ax[1].set_ylabel("Energy [eV]", fontsize=12)
ax[1].set_xlabel("Energy State", fontsize=12)

#ax[2].set_ylabel("Projection", fontsize=12)
ax[2].set_ylabel("Population", fontsize=12) # %%
ax[2].set_xlabel("Energy State", fontsize=12)

bar_positions = np.arange(1, 5)
start_vals = np.zeros_like(bar_positions)
#bars = ax[2].bar(bar_positions, start_vals, label="Projections")
bars = ax[2].bar(bar_positions, start_vals, label="Populations") # %%
ax[2].set_xticks([1, 2, 3, 4])
ax[2].set_ylim([0, 1.2])

energy = ax[1].scatter([], [], s=20, label="Energies")
ax[1].set_xlim([0.5, 4.5])
ax[1].set_ylim([-well_depth-0.5, 0.5])
total_energy_text = ax[1].text(1, 0, "")

def init():
    wave_plot.set_data([], [])
    pes_plot.set_data([], [])
    for bar, val in zip(bars, start_vals):
        bar.set_height(start_vals)
    energy.set_offsets(np.empty((0, 2)))
    total_energy_text.set_text("Total Energy=")
    return wave_plot, pes_plot, bars, energy, total_energy_text
# === END === #

pes = -e0

# === Define Plot Updating Using Runge-Kutta 4th Order For Wave Function === #
def update_plot(j):
    global psi, pes
    if t[j] < t_final:
        pes = -e0 * (1 - np.heaviside(r - (r_r + velocity * t[j]) /2 , 0.5)) * np.heaviside(r + r_l /2, 0.5)
    ham = np.diag(-2 * kin_e_prefactor + pes) + np.diag(kin_e_prefactor * np.ones(len(r) - 1), 1) + np.diag(kin_e_prefactor * np.ones(len(r) - 1), -1)

    # Runge-Kutta 4th order
    k1 = (-1j / hbar) * ham @ psi #Euler
    k2 = (-1j / hbar) * ham @ (psi + (dt / 2) * k1) #Trapezoidal Rule/ Heun's Method (Predictor-Corrector Method)
    k3 = (-1j / hbar) * ham @ (psi + (dt / 2) * k2)
    k4 = (-1j / hbar) * ham @ (psi + dt * k3)

    psi = psi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

#    ax[0].text(10, 0.05, f"Velocity={speed_coeff} \n [Å/fs]")

    if j % 10 == 0:
        # Update plots Every Ten Time Steps
        func_to_plot = 25 * (np.abs(psi) ** 2) + eg[0] / ev - well_depth
        wave_plot.set_data(r / angs, func_to_plot)
        pes_plot.set_data(r / angs, pes / ev)

        current_t = t[j]  / fs
        fig.suptitle(f"Time: {current_t:.2f} fs")

        eigenvals, eigenfuncs = np.linalg.eigh(ham)
        energies = eigenvals / ev

        projections = np.zeros(5)

        tot_time = 0.2 #0.8
        sam_freq = 40000
        t_sound = np.linspace(0, tot_time, int(sam_freq * tot_time))
        ha_to_sound = 280000
        sound_function = np.zeros(len(t_sound))

        offsets = []
        sizes = []
        sound_list = []

        for k in range(len(projections)):
            projections[k] = np.abs(np.sum(psi * eigenfuncs[:, k]))**2

            # Generate Sound
            sound_v = 800 + (energies[k] + 0.1447) * ha_to_sound
            sound_v = np.abs(sound_v)
            if projections[k] < 0.02:
                projections[k] = 0

            sound_function += projections[k] * np.cos(2 * np.pi * sound_v * t_sound)

            # Determine Sizes of Points In Second Plot
            offsets.append([k + 1, energies[k]])
            size = int(projections[k]*100)
            sizes.append(size)

        # Set Bar Heights In Third Plot
        for bar, height in zip(bars, projections):
            bar.set_height(height)

        # Generate Points In Second Plot
        energy.set_sizes(sizes)
        offsets = np.array(offsets)
        energy.set_offsets(offsets)

        total_energy = np.real(np.vdot(psi, ham @ psi)) / ev
        total_energy_text.set_text(f"Total Energy={total_energy:.2f} [eV]")

        # Generate Sound Function
        sound_function = sound_function / np.max(sound_function)
        sound_list.append(sound_function)
        sound_arr = np.array(sound_list).astype(np.float32)

        # Save sound to .wav file for each 10 timesteps
#        for i in range(0, len(sound_arr)):
#            sound_arr[i] = sound_arr[i] / np.max(sound_arr)
#            wavfile.write(f'output_eigh{j}.wav', samfreq, sound_arr[i].astype(np.float32))

    return wave_plot, pes_plot, bars, energy, total_energy_text
# === END === #

# === Run The Simulation === #
ani = FuncAnimation(fig, update_plot, init_func=init, frames=len(t), interval=2, blit=False, repeat=False)
ax[0].text(10, 0.05, f"Velocity={speed_coeff} \n [Å/fs]")
#plt.show()
# === END === #

# === Save The Animation (Will Not Plot To Notebook If Uncommented) === #
filename = "slow"
ani.save(f"{filename}.mp4", writer=FFMpegWriter(fps=60))
# === END === #
