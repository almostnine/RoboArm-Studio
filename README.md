# RoboArm Studio

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-orange?logo=arduino&logoColor=white)

Web interface per controllare un braccio robotico Arduino via Flask. 7 servomotori controllabili in tempo reale.

## Hardware

Basato sul design di [Emre Kalem](https://makerworld.com/en/models/1134), modificato:
- Rimosso breadboard
- Aggiunto Sensor Shield su Arduino Uno R4

**Setup**: Arduino Uno R4 con Sensor Shield

## Setup

```bash
pip3 install -r requirements.txt
python3 robot_arm_server.py
```

Poi apri `http://localhost:5001` e connetti l'Arduino.

**Importante**: Carica `RoboArm_Studio.ino` sull'Arduino prima di avviare il server.

## Servo Mapping

| Servo | Funzione | Pin Arduino |
|-------|----------|------------|
| 0 | Root (base rotante) | Pin 2 |
| 1 | Arm A1 (braccio principale) | Pin 3 |
| 2 | Arm A2 (braccio accoppiato) | Pin 4 |
| 3 | Arm B (avambraccio) | Pin 5 |
| 4 | Wrist A | Pin 6 |
| 5 | Wrist B | Pin 7 |
| 6 | Gripper | Pin 8 |

**Nota**: Arm A1 (Pin 3) e Arm A2 (Pin 4) sono accoppiati e ruotano in direzioni opposte. Quando A1 va a X°, A2 va automaticamente a (180-X)°.

## Preset

- **Home**: Posizione iniziale (servo 0-5 a 90°, gripper a 35°)
- **Rest**: Posizione di riposo
- **Reach**: Braccio esteso in avanti
- **Grab**: Posizione per afferrare oggetti

## Accesso da rete

Per controllare da altri dispositivi sulla stessa rete:

```bash
ifconfig | grep "inet "
```

Poi apri `http://TUO_IP:5001` dal dispositivo remoto.

## Personalizzazione

### Cambiare porta

In `robot_arm_server.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Aggiungere preset

In `robot_arm_server.py`, funzione `api_preset`:
```python
presets = {
    'home': [90, 90, 90, 90, 90, 90, 35],
    'nuovo_preset': [45, 120, 60, 90, 45, 180, 50],
}
```

Poi aggiungi il bottone in `templates/index.html`.

## Troubleshooting

**Arduino non trovato**: Verifica che sia connesso e che i driver siano installati. Su Mac: `ls /dev/cu.*`

**Porta già in uso**: Chiudi Arduino IDE e serial monitor.

**Permission denied** (Mac):
```bash
sudo chmod 666 /dev/cu.usbmodem*
```

## Credits

- Hardware design originale: [Emre Kalem](https://makerworld.com/en/models/1134)
- Modifiche hardware: Breadboard rimosso, Sensor Shield aggiunto

## License

MIT - Vedi [LICENSE](LICENSE) per dettagli.
