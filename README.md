# Progetto2025-

Questo progetto implementa un simulatore gravitazionale basato sulla legge di gravitazione universale di Newton. Il software permette di studiare l'evoluzione orbitale di sistemi complessi (come il Sistema Solare) e di analizzare la velocità radiale di stelle per l'individuazione di esopianeti tramite analisi in frequenza.

Il progetto si basa sulla risoluzione numerica delle equazioni del moto

$$a_{i} = \sum_{j \ne i} G \frac{m_{j}}{|r_{ij}|^2} \frac{r_{ij}}{|r_{ij}|}$$

Partendo da condizioni iniziali note (posizioni e velocità), il sistema calcola l'evoluzione temporale procedendo per passi discreti.

Funzionalità principali:
    - implementazione dell'algoritmo di integrazione nel modulo `nbody.py`   
    - animazione interattiva e produzione di grafici statici delle traiettorie in `solar_system.py`
    - studio delle velocità radiali e spettroscopia Doppler tramite FFT in `exoplanets.py`

Il progetto richiede python3 e le seguenti librerie:
    - numpy
    - matplotlib
    - scipy

PER L'ESECUZIONE

Per simulare l'evoluzione di un sistema e generare l'animazione 3D:

    ```bash
    python3 solar_system.py --config dati/file.json --dt 0.01 --npassi 10000 --zoom 2.0
    ```

il comando salva automaticamente un grafico nella cartella outputs (se questa non esiste, viene creata).
I flag `--dt` e `--npassi` hanno un valore di default nel caso non venga specificato dall'utente.
Il flag `--zoom` seguito da un valore in AU serve per regolare la vista, data la grande differenza di distanza dal Sole tra i pianeti più interni e quelli più esterni.


Per analizzare il movimento di una stella indotto da pianeti orbitanti e calcolarne il periodo:

    ```bash
    python3 exoplanets.py --config dati/file.json --dt 0.05 --npassi 5000
    ```

Questo script produce il grafico della velocità radiale della stella nel tempo e lo spettro di potenza con la stima del periodo orbitale dominante.

STRUTTURA REPOSITORY

**nbody.py** : contiene la funzione calcola_accelerazioni e l'integratore

**solar_system.py** : script principale per studiare l'evoluzione del sistema solare a partire da diverse condizioni iniziali

**exoplanets.py** : dedicato all'analisi delle velocità radiali

**dati/** : cartella contenente i file .json con i parametri fisici (masse, coordinate e velocità)

**outputs/** : cartella creata automaticamente per il salvataggio dei grafici statici .png

**horizon/** : cartella contenente i file scaricati direttamente da NASA horizons, da cui si sono presi i dati per i file `.json`

I file `.json` nella cartella `dati/` permettono di verificare diversi scenari fisici:
    velocità di fuga : il file sistsolare_velterra41.json testa il limite in cui la Terra non è più legata gravitazionalmente al Sole

    Metodo Doppler : i file esopianeta.json (da 1 a 4) mostrano come variando massa e distanza del pianeta cambi l'ampiezza della velocità radiale della stella

    Stabilità del sistema: i file sistsolre_velgiove.json analizzano come la perturbazione di un gigante gassoso influenzi le orbite degli altri corpi

    Perturbazioni: test_disturbo.json pone Giove nella fascia degli asteroidi per forzare un'interazione gravitazionale visibile con i pianeti interni

    Ecco i file nel dettaglio:
        - esopianeta.json : file contenente i dati di una stella come il Sole e un pianeta 10 volte la massa di Giove posto a una distanza molto minore

        - esopianeta2.json : file contenente i dati di una stella come il Sole e un pianeta 100 volte la massa di Giove posto a una distanza molto minore

        - esopianeta3.json : file contenente i dati di una stella come il Sole e un pianeta 10 volte la massa di Giove posto a una distanza ancora minore rispetto al file esopianeta.json

        - esopianeta4.json : file contenente i dati di una stella come il Sole e un pianeta con massa dell'ordine di grandezza di quella della Terra

        - external.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti giganti del sistema solare (Giove, Saturno, Urano, Nettuno)

        - sistema_solare.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare (Mercurio, Venere, Terra, Marte, Giove, Saturno, Urano, Nettuno)

        - sistsolare_data : file contenente i dati presi il 29/06/2026 relativi al Sole e ai pianeti del sistema solare (Mercurio, Venere, Terra, Marte, Giove, Saturno, Urano, Nettuno)

        - sistsolare_velgiove20.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare modificati solo per Giove, la cui velocità è incrementata del 20%

        - sistsolare_velgiove-30.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare modificati solo per Giove, la cui velocità è diminuita del 30%

        - sistsolare_velterra10.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare modificati solo per la Terra, la cui velocità è incrementata del 15%

        - sistsolare_velterra-20.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare modificati solo per la Terra, la cui velocità è diminuita del 20%

        - sistsolare_velterra41.json : file contenente i dati presi il 29/12/2025 relativi al Sole e ai pianeti del sistema solare modificati solo per la Terra, la cui velocità è circa la velocità di fuga

        - test_disturbo.json : file contenente i dati presi il 29/12/2025 relativi al Sole, alla Terra e a Giove. Per scopi di test, sono state utilizzate condizioni iniziali che pongono Giove a una distanza ridotta per osservare le perturbazioni gravitazionali in un sistema più compatto

        - test_disturbo2.json : file contenente i dati presi il 29/12/2025 relativi al Sole, alla Terra e a Giove. Per scopi di test, sono state utilizzate condizioni iniziali che pongono Giove con una massa circa 100 volte quella attuale

        - tre_corpi.json : file contenente i dati presi il 29/12/2025 relativi al Sole, alla Terra e a Giove. 


