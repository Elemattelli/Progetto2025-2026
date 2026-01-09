# Progetto2025-2026

Questo progetto implementa un simulatore gravitazionale basato sulla legge di gravitazione universale di Newton. Il software permette di studiare l'evoluzione orbitale di sistemi complessi (come il Sistema Solare) e di analizzare la velocità radiale di stelle per l'individuazione di esopianeti tramite analisi in frequenza.

Il progetto si basa sulla risoluzione numerica delle equazioni del moto

$$a_{i} = \sum_{j \ne i} G \frac{m_{j}}{|r_{ij}|^2} \frac{r_{ij}}{|r_{ij}|}$$

Partendo da condizioni iniziali note (posizioni e velocità), il sistema calcola l'evoluzione temporale procedendo per passi discreti.

**Nota sulle Unità di misura** : Il simulatore utilizza Unità Astronomiche (AU) per le distanze, giorni per il tempo e masse solari relative. La costante gravitazionale G è impostata coerentemente nel modulo `nbody.py`

## Funzionalità principali:
- implementazione dell'algoritmo di integrazione nel modulo `nbody.py`   
- animazione interattiva e produzione di grafici statici delle traiettorie in `solar_system.py`
- studio delle velocità radiali e spettroscopia Doppler tramite FFT in `exoplanets.py`

Il progetto richiede python3 e le seguenti librerie:
    - `numpy`
    - `matplotlib`
    - `scipy`

## Per l'esecuzione
Per simulare l'evoluzione di un sistema e generare l'animazione 3D:

    ```bash
    python3 solar_system.py --config dati/solarsystem/file.json --dt 0.01 --npassi 10000 --zoom 2.0
    ```

il comando salva automaticamente un grafico nella cartella `outputs/` (se questa non esiste, viene creata).
Il flag `--config` permette di selezionare il file `.json` che definisce lo scenario della simulazione.
Il flag `--dt` rappresenta il passo temporale (ovvero l'intervallo di tempo che intercorre tra un calcolo e quello successivo), mentre `--npassi` specifica il numero totale di iterazioni; la durata totale della simulazione è data dal prodotto tra questi due valori.
I flag `--dt` e `--npassi` hanno un valore di default nel caso non venga specificato dall'utente.
Il flag `--zoom` seguito da un valore in AU serve per regolare la vista, data la grande differenza di distanza dal Sole tra i pianeti più interni e quelli più esterni.


Per analizzare il movimento di una stella indotto da pianeti orbitanti e calcolarne il periodo:

    ```bash
    python3 exoplanets.py --config dati/exoplanet/file.json --dt 0.05 --npassi 5000
    ```

Questo script produce il grafico della velocità radiale della stella nel tempo e lo spettro di potenza con la stima del periodo orbitale dominante.
**Nota**: in questo script non è previsto l'uso del flag `--zoom`. 

Per visualizzare i file di configurazione `.json` disponibili per un determinato script python è possibile utilizzare il flag `--list` nel seguente modo:

    ```bash
    python3 solar_system.py --list
    ```

    ```bash
    python3 exoplanets.py --list
    ```    

## Struttura repository

`nbody.py` : contiene la funzione calcola_accelerazioni e l'integratore

`solar_system.py` : script principale per studiare l'evoluzione del sistema solare a partire da diverse condizioni iniziali

`exoplanets.py` : dedicato all'analisi delle velocità radiali

`dati/` : cartella contenente i file `.json` con i parametri fisici (masse, coordinate e velocità). E' organizzata nelle sottocartelle `solarsystem/` ed `exoplanet/` in base alla tipologia di simulazione suggerita.

`outputs/` : cartella creata automaticamente per il salvataggio dei grafici statici `.png`

`horizon/` : cartella contenente i file scaricati direttamente da **NASA Horizons**, da cui si sono presi i dati per i file `.json`

I file `.json` nella cartella `dati/` permettono di verificare diversi scenari fisici:
**velocità di fuga** : il file `sistsolare_velterra41.json` testa il limite in cui la Terra non è più legata gravitazionalmente al Sole

**Metodo Doppler** : i file `esopianeta.json` (da 1 a 4) mostrano come variando massa e distanza del pianeta cambi l'ampiezza della velocità radiale della stella. Si consiglia un dt piccolo per questi file

**Stabilità del sistema** : i file `sistsolare_velgiove.json` analizzano come la perturbazione di un gigante gassoso influenzi le orbite degli altri corpi

**Perturbazioni** : `test_disturbo.json` pone Giove nella fascia degli asteroidi per forzare un'interazione gravitazionale visibile con i pianeti interni

### Scenari di test e configurazioni nel dettaglio (`dati/`)
Tutti i dati reali sono stati estratti dal sistema **NASA Horizons**:

1. **Evoluzione del sistema solare**:
- `sistema_solare.json` : configurazione completa (Sole e 8 pianeti) al 29/12/2025
- `sistsolare_data` : configurazione completa al 29/06/2026
- `external.json` : include solo il Sole e i pianeti giganti (Giove, Saturno, Urano, Nettuno) al 29/12/2025 
- `tre_corpi.json` : sistema semplificato con Sole, Terra e Giove al 29/12/2025 

2. **Metodo Doppler e ricerca di esopianeti**:
Questi file sono ottimizzati per `exoplanets.py` (si consiglia un `dt` piccolo)
- `esopianeta.json` : stella simile al Sole e un pianeta 10 volte la massa di Giove posto a distanza ravvicinata
- `esopianeta2.json` : caso estremo con pianeta massiccio (100 volte la massa di Giove) per segnali Doppler evidenti
- `esopianeta3.json` : pianeta 10 volte la massa di Giove in orbita strettissima
- `esopianeta4.json` : caso limite con pianeta di massa terrestre
- `esopianeti.json` : caso di due giaganti che orbitano attorno a una stella come il Sole

3. **Test di stabilità e perturbazioni**:
- `sistsolare_velterra41.json` : Terra con velocià incrementata del 41%, limite del legame gravitazionale
- **variazioni orbitali**:
    - `sistsolare_velterra15.json` : Terra con velocità incrementata del 15%
    - `sistsolare_velterra-20.json` : Terra con velocità  diminuita del 20%

    per osservare l'effetto sui pianeti interni:
    - `sistsolare_velgiove20.json` : Giove con velocità incrementata del 20%
    - `sistsolare_velgiove-30.json` : Giove con velocità diminuita del 30%
- **interazioni forti**:
- `test_disturbo.json` : Giove posizionato artificialmente nella fascia degli asteroidi
- `test_disturbo2.json` : Giove con una massa incrementata 100 volte per forzare instabilità nel sistema



