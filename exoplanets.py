import json
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import nbody as nb
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import argparse

def velocita_radiale(vx_stella, nomi_corpi, dt):
    time = np.linspace(0, len(vx_stella) * dt, len(vx_stella))

    plt.style.use('dark_background')
    plt.figure(figsize=(12, 10))
    plt.plot(time, vx_stella, color='mediumslateblue', label=rf'Velocità di {nomi_corpi[0]}')
    plt.axhline(0, color='crimson', linestyle='--', alpha=0.8)
    plt.title(rf'Metodo delle Velocità radiali per ricerca di esopianeti')
    plt.xlabel(r'Tempo [giorni]')
    plt.ylabel(r'Velocità radiale [AU/Giorno]')
    plt.legend(fontsize=13)
    plt.grid(True, alpha=0.2)
    plt.show()

def analisi_fourier_velocita(vx_stella, dt):
    n = len(vx_stella)
    yf = fft(vx_stella - np.mean(vx_stella)) 
    xf = fftfreq(n, dt)
    
    xf = xf[:n//2]
    yf = 2.0/n * np.abs(yf[:n//2])
    
    # Trova la frequenza dominante (escludendo lo zero)
    idx_max = np.argmax(yf[1:]) + 1 
    freq_dominante = xf[idx_max]
    periodo = 1 / freq_dominante
    
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    plt.plot(xf, yf, color='gold')
    plt.title(f"Spettro di Frequenza (FFT) - Periodo stimato: {periodo:.2f} giorni")
    plt.xlabel("Frequenza [1/giorni]")
    plt.ylabel("Ampiezza")
    plt.grid(True)
    plt.show()
    return periodo

def anima_sistema(nomi_corpi, traiettoria, N, args, colors):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 8), facecolor='#0B0E14')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0B0E14')

    # griglia
    grid_params = {'linewidth': 0.2, 'color': (0.5, 0.5, 0.5, 0.2)}
    ax.xaxis._axinfo["grid"].update(grid_params)
    ax.yaxis._axinfo["grid"].update(grid_params)
    ax.zaxis._axinfo["grid"].update(grid_params)
    
    ax.xaxis.set_pane_color((0,0,0,0))
    ax.yaxis.set_pane_color((0,0,0,0))
    ax.zaxis.set_pane_color((0,0,0,0))

    ax.scatter(0, 0, 0, color='crimson', marker='.', s=100, label='Baricentro', alpha=0.7)
    punti = [ax.plot([], [], [], 'o', color=colors[i], markersize=6,
                     markeredgecolor='white', markeredgewidth=0.5, label=nomi_corpi[i])[0] for i in range(N)]
    scie = [ax.plot([], [], [], '-', color=colors[i], alpha=0.4, linewidth=0.8)[0] for i in range(N)]
    testi = [ax.text(0, 0, 0, nomi_corpi[i], color=colors[i], fontsize=8, fontweight='bold', zdir=(1, 0, 0)) for i in range(N)]

    def init():
        for punto, scia, testo in zip(punti, scie, testi):
            punto.set_data([], [])
            punto.set_3d_properties([])
            scia.set_data([], [])
            scia.set_3d_properties([])
            testo.set_position((0, 0))
        return punti + scie + testi

    def update(frame):
        for i in range(N):
            x, y, z = traiettoria[frame, i, 0], traiettoria[frame, i, 1], traiettoria[frame, i, 2]
            punti[i].set_data([x], [y])
            punti[i].set_3d_properties([z])
                
            scia_x = traiettoria[:frame, i, 0]
            scia_y = traiettoria[:frame, i, 1]
            scia_z = traiettoria[:frame, i, 2]
            scie[i].set_data(scia_x, scia_y)
            scie[i].set_3d_properties(scia_z)

            testi[i].set_position((x, y))
            testi[i].set_3d_properties(z, 'z')
            testi[i].set_horizontalalignment('left') 
            testi[i].set_verticalalignment('bottom') 
        return punti + scie + testi

    all_pos = traiettoria.reshape(-1, 3)
    limite = np.abs(all_pos).max() * 1.1

    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_zlim(-limite, limite)

    ax.legend(loc='upper left', frameon=False, fontsize=8)
    ani = FuncAnimation(fig, update, frames=range(0, args.npassi, 10), 
                            init_func=init, blit=False, interval=20)

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Simulazione dinamica di un sistema a N corpi',
                                     usage='python3 exoplanets.py --config dati/exoplanet/file.json --dt --npassi')
    parser.add_argument('--list', action='store_true', help='Mostra tutti i file di configurazione JSON disponibili')
    parser.add_argument('--config', type=str, help='File json con masse, posizioni e velocità')
    parser.add_argument('--dt', type=float, default=0.001, help='Passo temporale (default 0.001)')
    parser.add_argument('--npassi', type=int, default=100000, help='Numero passi (default 100000)')
    args = parser.parse_args()

    if args.list:
        file_json = glob.glob("dati/exoplanet/*.json")
        print("File di configurazione trovati:")
        if file_json:
            for f in file_json:
                print(f"  > {f}")
        else:
            print("Nessun file .json trovato.")
        return 
    if not args.config:
        print("Errore: E' necessario specificare un file con --config dati/exoplanet/nomefile.json")
        print("Usa --list per vedere i file disponibili.")
        return


    with open(args.config, 'r') as f:
        sistema = json.load(f)

    nomi_corpi = list(sistema.keys())
    N = len(nomi_corpi)

    masse, posizioni, velocita = [], [], []
    for nome in nomi_corpi:
        masse.append(sistema[nome]['m'])
        posizioni.append(sistema[nome]['r'])
        velocita.append(sistema[nome]['v'])

    m = np.array(masse) / masse[0] 
    r = np.array(posizioni)
    v = np.array(velocita)
    dt = args.dt
    npassi = args.npassi

    v_cm = np.sum(m[:, np.newaxis] * v, axis=0) / np.sum(m)
    v -= v_cm

    r_cm = np.sum(m[:, np.newaxis] * r, axis=0) / np.sum(m)
    r -= r_cm

    traiettoria, velocita_tot = nb.integra_sistema(m, r, v, dt, npassi)
    vx_stella = velocita_tot[:, 0, 0]

     # grafici
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = plt.cm.spring(np.linspace(0, 1, N))

    fig.patch.set_facecolor('#0B0E14') #sfondo esterno
    ax.set_facecolor('#0B0E14') # sfondo del plot

    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # griglia
    grid_params = {'linewidth': 0.3, 'color': (0.5, 0.5, 0.5, 0.2)}
    ax.xaxis._axinfo["grid"].update(grid_params)
    ax.yaxis._axinfo["grid"].update(grid_params)
    ax.zaxis._axinfo["grid"].update(grid_params)

    ax.tick_params(axis='both', which='major', colors='gray', labelsize=9)

    for i in range(N):
        ax.plot(traiettoria[:, i, 0], traiettoria[:, i, 1], traiettoria[:, i, 2],
                label=nomi_corpi[i], color=colors[i], alpha=0.6, linewidth=1)
        
        ax.scatter(traiettoria[-1, i, 0], traiettoria[-1, i, 1], traiettoria[-1, i, 2],
                   color=colors[i], s=40, edgecolors='white', linewidth=0.5)
        
        ax.text(traiettoria[-1, i, 0], traiettoria[-1, i, 1], traiettoria[-1, i, 2],
                f' {nomi_corpi[i]}', fontsize=9, color=colors[i], fontweight='semibold', va='center')

    ax.scatter(0, 0, 0, color='crimson', marker='.', s=50, label='Baricentro')

    all_pos = traiettoria.reshape(-1, 3)
    limite = np.abs(all_pos).max() * 1.1

    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_zlim(-limite, limite)

    ax.set_title(rf'Evoluzione sistema: {args.config} (dt={args.dt}, passi={args.npassi})')
    ax.set_xlabel(r'X [Au]')
    ax.set_ylabel(r'Y [Au]')
    ax.set_zlabel(r'Z [Au]')
    ax.legend(loc='center left', bbox_to_anchor=(1.07, 0.5), fontsize=10)

    base_name = os.path.basename(args.config).replace('.json', '.png')

    cartella_output = "outputs"
    if not os.path.exists(cartella_output):
        os.makedirs(cartella_output)
    percorso_finale = os.path.join(cartella_output, base_name)
    plt.savefig(percorso_finale, dpi=300, bbox_inches='tight')
    print(f'Grafico salvato in: {percorso_finale}')

    anima_sistema(nomi_corpi, traiettoria, N, args, colors)
    
    velocita_radiale(vx_stella, nomi_corpi[0], dt)
    analisi_fourier_velocita(vx_stella, dt)

if __name__ == "__main__":
    main()

