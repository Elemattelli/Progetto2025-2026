import json
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import nbody as nb
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

def main():
    parser = argparse.ArgumentParser(description='Simulazione dinamica di un sistema a N corpi',
                                     usage='python3 solar_system.py --config dati/file.json --dt --npassi --zoom')
    parser.add_argument('--config', type=str, help='File json con masse, posizioni e velocità')
    parser.add_argument('--dt', type=float, default=0.01, help='Passo temporale (default 0.01)')
    parser.add_argument('--npassi', type=int, default=10000, help='Numero passi (default 10000)')
    parser.add_argument('--zoom', type=float, help='Zoom AU')
    args = parser.parse_args()

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

    traiettoria, velocita_tot = nb.integra_sistema(m, r, v, dt, npassi)
    vx_stella = velocita_tot[:, 0, 0]

     # grafici
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # colori_fissi = ['#FFFFFF','#ADADAD', '#FF00FF', '#00FFFF', '#FF3131', '#FFAC2E', '#F5D033', '#00FF9F', '#3D52FF']
    # colors = [colori_fissi[i % len(colori_fissi)] for i in range(N)]
    colors = plt.cm.viridis(np.linspace(0, 1, N))

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
        
    if args.zoom:
        limite = args.zoom
        ax.set_xlim(-limite, limite)
        ax.set_ylim(-limite, limite)
        ax.set_zlim(-limite, limite)
    
    else:
        all_pos = traiettoria.reshape(-1, 3)
        limit = np.abs(all_pos).max()

        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)

    ax.set_title(rf'Evoluzione sistema: {args.config}\n(dt={args.dt}, passi={args.npassi})')
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

    velocita_radiale(vx_stella, nomi_corpi[0], dt)
    analisi_fourier_velocita(vx_stella, dt)

if __name__ == "__main__":
    main()

