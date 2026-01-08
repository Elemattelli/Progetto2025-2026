import numpy as np

G = 0.0002959122
def calcola_accelerazioni(r, m, G, N):
    acc = np.zeros((N, 3))
    epsilon = 1e-9 
    for i in range(N):
        for j in range(N):
            if i != j:
                diff = r[j] - r[i]
                dist_sq = np.sum(diff**2) + epsilon**2
                dist = np.sqrt(dist_sq)
                acc[i] += G * m[j] / (dist**3) * diff
    return acc

def integra_sistema(m, r_init, v_init, dt, npassi):
    N = len(m)
    r = np.array(r_init, dtype=float)
    v = np.array(v_init, dtype=float)

    traiettoria = np.zeros((npassi, N, 3))
    velocita_tot = np.zeros((npassi, N, 3))

    acc_attuale = calcola_accelerazioni(r, m, G, N)

    for pp in range(npassi):
        r += v * dt + 0.5 * acc_attuale * dt **2
        acc_nuova = calcola_accelerazioni(r, m, G, N)
        v += 0.5 * (acc_attuale + acc_nuova) * dt

        acc_attuale = acc_nuova
        traiettoria[pp] = r.copy()
        velocita_tot[pp] = v.copy()
    
    return traiettoria, velocita_tot