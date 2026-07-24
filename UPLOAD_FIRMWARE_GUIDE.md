# 🔧 Guida Caricamento Firmware Arduino

## ⚠️ IMPORTANTE
Il file `RoboArm_Studio.ino` è stato modificato sul computer, ma NON è ancora stato caricato su Arduino!
Devi seguire questi passi per applicare il fix.

## 📋 Procedura Passo-Passo

### Passo 1: Disconnetti Arduino dal Server Web
```
1. Apri browser: http://localhost:5001
2. Click sul pulsante "Disconnect Arduino"
3. Attendi conferma disconnessione
```
**Perché?** Il server Python tiene occupata la porta seriale. Arduino IDE non può caricare il firmware se la porta è occupata.

### Passo 2: Apri Arduino IDE

```
1. Apri l'applicazione Arduino IDE
2. File → Open
3. Naviga a: /Users/marcodisanto/Documents/projects/RoboArm-Studio/
4. Seleziona: RoboArm_Studio.ino
5. Click "Open"
```

### Passo 3: Configura Arduino IDE

```
1. Tools → Board → Arduino AVR Boards → Arduino Uno
   (oppure "Arduino Uno R4" se hai R4)

2. Tools → Port → Seleziona la porta USB
   (es. /dev/cu.usbmodem14101 o simile)
   
   ⚠️ Se non vedi porte disponibili:
   - Verifica che Arduino sia collegato via USB
   - Prova a scollegare e ricollegare il cavo USB
```

### Passo 4: Verifica il Codice

Prima di caricare, verifica che il codice contenga le modifiche:

```cpp
// Cerca queste righe nel file (circa linea 78-153):

void loop()
{
  // Check for new commands from serial port
  if (Serial.available() > 0)
  {
    // Read target angle values
    for (int i = 0; i < 7; i++)
    {
      targetAngles[i] = Serial.parseInt();
    }
    
    // DEBUG: Print received target angles  ← QUESTA RIGA DEVE ESSERCI
    Serial.print("RX: ");                   ← QUESTA RIGA DEVE ESSERCI
    for (int i = 0; i < 7; i++)             ← QUESTA RIGA DEVE ESSERCI
    {
      Serial.print(targetAngles[i]);
      if (i < 6) Serial.print(",");
    }
    Serial.println();
  }
  
  // ... codice interpolazione ...
  
  // Write current positions to servos ONLY when moving  ← IMPORTANTE
  if (isMoving)                                          ← IMPORTANTE
  {
    servo1.write(currentAngles[0]);
    servo2.write(currentAngles[1]);
    // ... altri servo ...
    delay(STEP_DELAY);
  }
  else                                                   ← IMPORTANTE
  {
    delay(1); // Small delay when idle                  ← IMPORTANTE
  }
}
```

✅ Se vedi queste modifiche → Procedi al Passo 5
❌ Se NON vedi queste modifiche → Il file non è stato salvato correttamente

### Passo 5: Compila e Carica

```
1. Click sul pulsante "Verify" (✓) per compilare
   - Attendi: "Done compiling"
   - Verifica che non ci siano errori

2. Click sul pulsante "Upload" (→) per caricare
   - Attendi: "Uploading..."
   - Attendi: "Done uploading"
   
⏱️ Tempo stimato: 10-30 secondi
```

### Passo 6: Verifica Caricamento

Dopo "Done uploading", Arduino si riavvierà automaticamente.

**Verifica con Serial Monitor**:
```
1. Arduino IDE → Tools → Serial Monitor
2. Imposta baud rate: 9600 (in basso a destra)
3. Dovresti vedere: (vuoto, Arduino in attesa di comandi)
```

### Passo 7: Riconnetti dal Server Web

```
1. Chiudi Serial Monitor di Arduino IDE (IMPORTANTE!)
2. Torna al browser: http://localhost:5001
3. Click "Connect Arduino"
4. Attendi conferma: "✅ Connesso!"
```

### Passo 8: Testa il Movimento

```
1. Muovi lo slider "Root" da 90° a 0°
2. Osserva il servo fisicamente
3. Dovrebbe muoversi GRADUALMENTE e COMPLETAMENTE
```

## ✅ Verifica Successo

### Test Rapido
- Muovi slider Root: 90° → 0° → 180° → 90°
- Il servo dovrebbe:
  ✅ Muoversi fluidamente
  ✅ Raggiungere ogni posizione
  ✅ Non vibrare quando fermo

### Test Debug (Opzionale)
Se vuoi vedere i comandi ricevuti da Arduino:

```
1. Disconnetti dal server web
2. Apri Arduino IDE → Tools → Serial Monitor
3. Baud rate: 9600
4. Riconnetti dal server web
5. Muovi uno slider
6. Nel Serial Monitor dovresti vedere: "RX: 70,90,90,90,90,90,35"
```

## 🆘 Problemi Comuni

### Errore: "Port already in use"
**Causa**: Il server Python sta ancora usando la porta seriale
**Soluzione**: 
1. Disconnetti dall'interfaccia web
2. Se non funziona, ferma il server Python (Ctrl+C nel terminale)
3. Riprova a caricare

### Errore: "Board not found"
**Causa**: Arduino non rilevato o porta sbagliata
**Soluzione**:
1. Verifica cavo USB collegato
2. Tools → Port → Seleziona porta corretta
3. Se non vedi porte, scollega/ricollega USB

### Errore: "Compilation error"
**Causa**: Errori nel codice
**Soluzione**:
1. Verifica che il file sia `RoboArm_Studio.ino`
2. Leggi il messaggio di errore in basso
3. Verifica che tutte le modifiche siano corrette

### Servo ancora fermi dopo caricamento
**Causa**: Firmware non caricato correttamente o problema hardware
**Soluzione**:
1. Verifica "Done uploading" in Arduino IDE
2. Riavvia Arduino (scollega/ricollega USB)
3. Verifica alimentazione esterna dei servo
4. Controlla connessioni fisiche

## 📊 Checklist Completa

Prima di caricare:
- [ ] Server web disconnesso da Arduino
- [ ] Arduino IDE aperto con RoboArm_Studio.ino
- [ ] Board selezionata (Arduino Uno/R4)
- [ ] Porta USB selezionata
- [ ] Codice compilato senza errori (✓)

Durante caricamento:
- [ ] Click su Upload (→)
- [ ] Attesa "Uploading..."
- [ ] Attesa "Done uploading"

Dopo caricamento:
- [ ] Serial Monitor chiuso
- [ ] Riconnessione dal server web
- [ ] Test movimento slider
- [ ] Servo si muove fluidamente ✅

## 🎯 Risultato Atteso

Dopo il caricamento corretto:
- ✨ Movimenti fluidi e graduali
- 🎯 Servo raggiungono posizione target
- 🔇 Nessun jitter quando fermi
- ⏱️ Tempo movimento 90°: ~1.35 secondi

---

**Importante**: Ogni volta che modifichi `RoboArm_Studio.ino`, devi ripetere questa procedura per caricare le modifiche su Arduino!


