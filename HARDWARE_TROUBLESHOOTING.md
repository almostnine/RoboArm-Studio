# 🔧 Troubleshooting Hardware - Servo Non Si Muovono

## ✅ Diagnosi Completata

Il test diagnostico ha confermato che:
- ✅ **Firmware aggiornato caricato correttamente**
- ✅ **Arduino riceve i comandi dal Python**
- ✅ **Comunicazione seriale funzionante**
- ✅ **Debug output presente**: `RX: 45,90,90,90,90,90,35`

**Conclusione**: Il problema è **HARDWARE**, non software!

---

## 🔌 Problema 1: Alimentazione Insufficiente (90% dei casi)

### 🚨 Sintomi
- Servo non si muovono affatto
- Servo si muovono solo minimamente (pochi gradi)
- Servo tremano o vibrano
- Arduino si riavvia quando provi a muovere i servo

### ⚡ Causa
I servo **non possono** essere alimentati solo dall'USB di Arduino! Hanno bisogno di un **alimentatore esterno dedicato**.

### 📊 Requisiti Alimentazione

**Per 7 servo standard (SG90 o simili)**:
- **Tensione**: 5V DC (regolata)
- **Corrente**: Minimo 2-3A (meglio 5A)
- **Potenza**: 10-15W

**Calcolo**: Ogni servo può assorbire fino a 500mA sotto carico
- 7 servo × 500mA = 3.5A (picco)
- Consigliato: Alimentatore 5V 5A

### ✅ Soluzione

#### Opzione A: Alimentatore Esterno Dedicato (Consigliato)

```
┌─────────────────┐
│  Alimentatore   │
│    5V 3-5A      │
└────┬────────────┘
     │
     ├──[+5V]──→ Rail positivo servo
     │
     └──[GND]──→ GND Arduino + Rail negativo servo
                  (IMPORTANTE: GND comune!)
```

**Setup**:
1. Collega il **+5V** dell'alimentatore al **rail positivo** dei servo
2. Collega il **GND** dell'alimentatore al **GND di Arduino** E al **rail negativo** dei servo
3. I **segnali PWM** (pin 2-8) vanno da Arduino ai servo
4. Arduino alimentato via USB (per la logica)

#### Opzione B: Batteria LiPo (Per Robot Mobile)

- **Tensione**: 7.4V (2S LiPo) con regolatore 5V
- **Capacità**: Minimo 2000mAh
- **Scarica**: 20C o superiore

### ⚠️ Errori Comuni

❌ **NON fare**:
- Alimentare i servo dal pin 5V di Arduino (max 500mA totali!)
- Usare alimentatore USB (max 500mA)
- Dimenticare di collegare GND comune

✅ **Fare**:
- Usare alimentatore esterno dedicato
- Collegare GND comune (Arduino + Alimentatore)
- Usare cavi di sezione adeguata (almeno 22 AWG)

---

## 🔧 Problema 2: Connessioni Fisiche

### 🔍 Verifica Connessioni

#### Pin Arduino → Servo (Segnale PWM)
```
Pin 2 → Root (Servo 0)
Pin 3 → Arm A1 (Servo 1)
Pin 4 → Arm A2 (Servo 2)
Pin 5 → Arm B (Servo 3)
Pin 6 → Wrist A (Servo 4)
Pin 7 → Wrist B (Servo 5)
Pin 8 → Gripper (Servo 6)
```

#### Cavi Servo (Standard)
```
🟤 Marrone/Nero  → GND (-)
🔴 Rosso         → +5V (Alimentazione esterna!)
🟠 Arancione/Giallo → Segnale PWM (da Arduino)
```

### ✅ Checklist Connessioni

- [ ] Tutti i cavi servo sono ben inseriti (non allentati)
- [ ] I colori dei cavi corrispondono (GND, +5V, Signal)
- [ ] I pin PWM sono corretti (2-8)
- [ ] GND comune collegato (Arduino + Alimentatore + Servo)
- [ ] Nessun cavo danneggiato o rotto
- [ ] Connettori puliti (no ossidazione)

### 🧪 Test Singolo Servo

Per isolare il problema, testa un servo alla volta:

1. **Disconnetti tutti i servo tranne Root (Pin 2)**
2. **Muovi solo Root dall'interfaccia web**
3. **Se Root funziona**: Problema è alimentazione insufficiente per tutti
4. **Se Root non funziona**: Problema specifico del servo o connessione

---

## 🤖 Problema 3: Servo Bloccati o Danneggiati

### 🔍 Verifica Meccanica

#### Test Manuale
1. **Scollega alimentazione**
2. **Prova a muovere manualmente ogni servo**
3. **Dovrebbero muoversi con leggera resistenza**

#### Sintomi Servo Danneggiato
- ❌ Servo completamente bloccato (non si muove manualmente)
- ❌ Servo gira liberamente senza resistenza (ingranaggi rotti)
- ❌ Servo fa rumore strano (grinding, clicking)
- ❌ Servo si scalda eccessivamente

### ✅ Soluzioni

**Servo Bloccato Meccanicamente**:
- Rimuovi ostacoli fisici
- Verifica che il braccio robotico non sia in posizione di stallo
- Controlla che le viti non siano troppo strette

**Servo Danneggiato**:
- Sostituisci il servo
- Usa servo di qualità (SG90, MG90S, MG996R)

---

## 🧪 Procedura di Test Sistematica

### Step 1: Verifica Alimentazione

```bash
# Misura tensione con multimetro
# Tra +5V e GND dei servo: dovrebbe essere 4.8-5.2V
```

**Risultato**:
- ✅ 4.8-5.2V → Alimentazione OK
- ❌ < 4.5V → Alimentazione insufficiente
- ❌ > 5.5V → Tensione troppo alta (rischio danni!)

### Step 2: Test Singolo Servo

1. **Disconnetti tutti tranne Root**
2. **Muovi Root a 45°** (dall'interfaccia web)
3. **Osserva**:
   - ✅ Si muove fluidamente → Alimentazione OK per 1 servo
   - ❌ Non si muove → Problema servo o connessione

### Step 3: Test Incrementale

1. **Collega 2 servo** (Root + Arm A1)
2. **Muovi entrambi**
3. **Se funzionano**: Aggiungi il terzo
4. **Se non funzionano**: Alimentazione insufficiente

### Step 4: Test Sotto Carico

1. **Collega tutti i servo**
2. **Muovi tutti contemporaneamente** (preset "Reach")
3. **Osserva**:
   - ✅ Tutti si muovono → Sistema OK!
   - ❌ Alcuni si muovono, altri no → Alimentazione al limite
   - ❌ Nessuno si muove → Alimentazione insufficiente

---

## 📊 Tabella Diagnostica Rapida

| Sintomo | Causa Probabile | Soluzione |
|---------|----------------|-----------|
| Nessun servo si muove | Alimentazione assente | Collega alimentatore esterno |
| Servo si muovono minimamente | Alimentazione insufficiente | Usa alimentatore più potente (5A) |
| Solo alcuni servo si muovono | Alimentazione al limite | Aumenta corrente alimentatore |
| Servo tremano | Tensione instabile | Aggiungi condensatore 1000µF |
| Arduino si riavvia | Picco di corrente | Alimentazione separata per servo |
| Un servo non funziona | Servo danneggiato o connessione | Verifica connessione o sostituisci |

---

## ✅ Setup Ideale Consigliato

### Hardware Necessario

```
✅ Arduino Uno R4 (o compatibile)
✅ 7× Servo (SG90, MG90S, o MG996R)
✅ Alimentatore 5V 5A (switching, regolato)
✅ Breadboard o shield per distribuire alimentazione
✅ Cavi jumper di qualità (22 AWG o migliore)
✅ Condensatore elettrolitico 1000µF 16V (opzionale ma consigliato)
```

### Schema Connessioni

```
┌──────────────┐
│  Alimentatore│         ┌─────────────┐
│   5V 5A      │         │  Arduino    │
└──┬───────┬───┘         │  Uno R4     │
   │       │             └──┬──────────┘
   │       │                │
   │       │                │ USB (PC)
   │       │                │
   │       └────[GND]───────┤ GND
   │                        │
   └────[+5V]───────────────┤ (Non usare pin 5V!)
                            │
                            ├─[Pin 2]─→ Root Servo (Signal)
                            ├─[Pin 3]─→ Arm A1 (Signal)
                            ├─[Pin 4]─→ Arm A2 (Signal)
                            ├─[Pin 5]─→ Arm B (Signal)
                            ├─[Pin 6]─→ Wrist A (Signal)
                            ├─[Pin 7]─→ Wrist B (Signal)
                            └─[Pin 8]─→ Gripper (Signal)

Tutti i servo:
  - GND (marrone) → GND comune
  - +5V (rosso) → Alimentatore 5V
  - Signal (arancione) → Pin Arduino corrispondente
```

---

## 🎯 Prossimi Passi

1. **Verifica alimentazione esterna** (causa più probabile)
2. **Controlla connessioni fisiche**
3. **Testa un servo alla volta**
4. **Se tutto è OK ma non funziona**: Contattami con foto del setup

---

## 📞 Informazioni da Fornire per Supporto

Se il problema persiste, fornisci:
- [ ] Foto del setup completo
- [ ] Modello dei servo utilizzati
- [ ] Specifiche alimentatore (V, A)
- [ ] Risultato test singolo servo
- [ ] Output del test diagnostico (già fatto ✅)

---

**Ricorda**: Il software funziona perfettamente! Il problema è solo hardware, quindi è risolvibile facilmente con l'alimentazione corretta! 💪


