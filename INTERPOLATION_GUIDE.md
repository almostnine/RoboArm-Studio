# Guida all'Interpolazione dei Movimenti

## Panoramica

Il sistema di interpolazione è stato implementato per ridurre le vibrazioni e migliorare la fluidità dei movimenti del braccio robotico. L'interpolazione avviene direttamente sull'Arduino, garantendo movimenti graduali e controllati.

## Come Funziona

### Interpolazione Hardware (Arduino)

Invece di muovere i servo direttamente alla posizione target, il sistema:

1. **Riceve la posizione target** dal server Python
2. **Calcola la differenza** tra posizione corrente e target per ogni servo
3. **Muove gradualmente** ogni servo di un piccolo step alla volta
4. **Ripete** fino a raggiungere la posizione target

Questo approccio elimina i movimenti bruschi e riduce significativamente le vibrazioni meccaniche.

## Parametri di Configurazione

Nel file `RoboArm_Studio.ino`, puoi regolare due parametri principali:

### 1. INTERPOLATION_STEP (Step di Interpolazione)

```cpp
const int INTERPOLATION_STEP = 1; // Gradi per step
```

- **Valore predefinito**: 1°
- **Valori consigliati**: 1-3°
- **Effetto**:
  - Valori più bassi (1°) = Movimenti più fluidi ma più lenti
  - Valori più alti (3-5°) = Movimenti più veloci ma meno fluidi

### 2. STEP_DELAY (Ritardo tra gli Step)

```cpp
const int STEP_DELAY = 15; // Millisecondi tra gli step
```

- **Valore predefinito**: 15ms
- **Valori consigliati**: 10-30ms
- **Effetto**:
  - Valori più bassi (10ms) = Movimenti più veloci
  - Valori più alti (30ms) = Movimenti più lenti e controllati

## Regolazione Fine

### Per Movimenti Ultra-Fluidi
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 20;
```
Ideale per: Movimenti precisi, registrazioni video, demo

### Per Movimenti Bilanciati (Predefinito)
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 15;
```
Ideale per: Uso generale, buon compromesso velocità/fluidità

### Per Movimenti Veloci
```cpp
const int INTERPOLATION_STEP = 2;
const int STEP_DELAY = 10;
```
Ideale per: Operazioni rapide, quando la fluidità estrema non è critica

### Per Carichi Pesanti
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 25;
```
Ideale per: Quando il braccio trasporta oggetti pesanti

## Vantaggi dell'Interpolazione

1. **Riduzione Vibrazioni**: I movimenti graduali riducono le sollecitazioni meccaniche
2. **Maggiore Precisione**: Il braccio raggiunge la posizione target in modo più controllato
3. **Minore Usura**: I servo e le parti meccaniche subiscono meno stress
4. **Movimenti Naturali**: I movimenti appaiono più fluidi e naturali
5. **Migliore Stabilità**: Riduce l'oscillazione dopo il raggiungimento della posizione

## Calcolo del Tempo di Movimento

Il tempo totale per completare un movimento può essere calcolato con:

```
Tempo (ms) = (Differenza Angolare / INTERPOLATION_STEP) × STEP_DELAY
```

Esempio:
- Movimento da 0° a 90° (differenza: 90°)
- INTERPOLATION_STEP = 1°
- STEP_DELAY = 15ms

Tempo = (90 / 1) × 15 = 1350ms = 1.35 secondi

## Considerazioni

### Alimentazione
Con l'interpolazione, i servo si muovono costantemente ma con meno corrente di picco. Assicurati che l'alimentazione sia stabile.

### Risposta ai Comandi
I comandi vengono processati immediatamente, ma il movimento fisico richiede tempo. Evita di inviare comandi troppo frequenti.

### Servo Accoppiati
I servo 1 e 2 (Arm A1 e Arm A2) sono accoppiati e si muovono in direzioni opposte. L'interpolazione gestisce automaticamente questo accoppiamento.

## Debug

Il server Python stampa messaggi di debug per ogni movimento:

```
[INTERPOLATION] Movimento servo 0 (Root (Pin 2)) a 45°
[INTERPOLATION] Angoli target: [45, 90, 90, 90, 90, 90, 35]
[INTERPOLATION] Comando inviato: 45 90 90 90 90 90 35
```

Questi messaggi aiutano a verificare che i comandi vengano inviati correttamente.

## Risoluzione Problemi

### Movimenti Troppo Lenti
- Aumenta `INTERPOLATION_STEP` a 2 o 3
- Riduci `STEP_DELAY` a 10-12ms

### Movimenti Scattosi
- Riduci `INTERPOLATION_STEP` a 1
- Aumenta `STEP_DELAY` a 20-25ms

### Vibrazioni Residue
- Aumenta `STEP_DELAY` a 25-30ms
- Verifica che i servo siano ben fissati
- Controlla l'alimentazione (deve essere stabile)

### Servo Non Rispondono
- Verifica la connessione seriale
- Controlla i messaggi di debug nel server Python
- Assicurati che l'Arduino sia alimentato correttamente

## Aggiornamento del Firmware

Dopo aver modificato i parametri in `RoboArm_Studio.ino`:

1. Apri il file con Arduino IDE
2. Seleziona la scheda Arduino corretta
3. Carica il firmware aggiornato
4. Riavvia il server Python
5. Testa i nuovi parametri

## Note Tecniche

- L'interpolazione avviene nel loop principale dell'Arduino
- Ogni iterazione del loop controlla se ci sono nuovi comandi e muove i servo di un passo
- Il sistema è non-bloccante: può ricevere nuovi comandi mentre sta ancora completando un movimento
- Se arriva un nuovo comando durante un movimento, il sistema passa immediatamente al nuovo target


