# gNB_GUI
## Descrizione
L'applicazione **gNB Command** è un'interfaccia grafica basata su **Tkinter** per configurare e avviare una gNodeB (gNB) utilizzando lo stack **srsRAN**. Consente agli utenti di configurare i parametri della gNB tramite un'interfaccia intuitiva e di eseguire i relativi comandi in ambiente Linux.

---

## Caratteristiche
- Interfaccia grafica per configurare i parametri della gNB.
- Supporto per configurazioni multiple (COTSUE e non-COTSUE).
- Lettura in tempo reale dell'output del processo.
- Inserimento della password `sudo` tramite una finestra dedicata.
- Arresto e gestione sicura del processo gNB.

---

## Requisiti
1. **Sistema operativo**: Linux.
2. **Python**: Versione 3.8 o superiore.
3. **Dipendenze Python**:
   - `tkinter`
   - `os`
   - `subprocess`
   - `signal`
   - `threading`
4. **Software richiesti**:
   - **srsRAN_Project** installato.
   - **Docker** configurato per emulare la core network.
5. **Permessi**:
   - Permessi di root per l'esecuzione dei comandi `sudo`.

---

## Installazione
1. Clona il repository:
   ```bash
   git clone <repository_url>
   cd <nome_cartella_repo>
   ```
2. Assicurati di avere Python 3.8 o superiore installato:
   ```bash
   python3 --version
   ```
3. Installa eventuali librerie mancanti (Tkinter è spesso preinstallato):
   ```bash
   sudo apt-get install python3-tk
   ```
4. Verifica che **srsRAN** sia installato e configurato correttamente.
5. Configura Docker per emulare la core network.

---

## Utilizzo
1. **Avvio della core network**:
   - Prima di eseguire il programma, avvia la core network con i seguenti comandi:
     ```bash
     cd srsRAN_Project/docker
     sudo docker compose up --build 5gc
     ```

2. **Avvio dell'applicazione**:
   - Esegui il programma principale:
     ```bash
     python3 <nome_file_script>.py
     ```

3. **Configurazione dei parametri**:
   - Inserisci i valori richiesti nei campi di input:
     - **gnb_id**
     - **ran_node_name**
     - **AMF address**
     - **Port**
     - Altri parametri specifici della configurazione.

4. **Avvio della gNB**:
   - Premi il pulsante **Start** per avviare il processo.
   - L'applicazione cercherà automaticamente i file di configurazione necessari (ad esempio, `gnb_zmq` e `gnb_COTSUE.yml`) in tutto il filesystem.

5. **Gestione del processo**:
   - Usa il pulsante **Stop** per arrestare il processo.
   - Usa il pulsante **T** per inviare comandi specifici al processo in esecuzione.

6. **Output in tempo reale**:
   - L'output del processo viene visualizzato nella finestra di log in fondo all'applicazione.

---

## Struttura dei file
- **`gnb_zmq`**: Configurazione della gNB in modalità normale.
- **`gnb_COTSUE.yml`**: Configurazione della gNB in modalità COTSUE.
- **Script principale**: Contiene il codice per l'interfaccia grafica e la gestione dei processi.

---

## Personalizzazioni
1. **Percorsi dei file**:
   - L'applicazione cerca i file di configurazione automaticamente usando il comando `find`.
   - I percorsi vengono aggiornati dinamicamente nei comandi.

2. **Parametri predefiniti**:
   - Modifica i valori preimpostati nei campi di input per adattarli al tuo ambiente.

