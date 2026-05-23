# ♟️ Networked Chess Game (Hybrid Python/C++ Architecture)

Ein netzwerkfähiges Schachspiel, das eine hybride Architektur aus einem **C++ Backend-Server**, einem **Python-Logik-Skript** und einem **Web-Frontend** nutzt. Das Projekt ist so konzipiert, dass es über ein automatisches Shell-Skript deployt und via ngrok weltweit online spielbar gemacht werden kann.

## 🛠️ System-Architektur & Dateien

Das Projekt demonstriert das Zusammenspiel verschiedener Sprachen und Netzwerk-Komponenten:

* **`chess_play.py`**: Die Kern-Spiellogik des Schachspiels (Regelprüfung, Zugvalidierung und Zustandserfassung) geschrieben in Python.
* **`server.cpp`**: Ein performanter C++ Server, der die Netzwerk-Verbindungen, das Routing und den Datenaustausch zwischen den Spielern verwaltet.
* **`index.html`**: Das interaktive Web-Frontend, über das die Spieler die Züge visuell ausführen.
* **`Deploy_ngrok.sh`**: Automatisierungsskript, das einen sicheren ngrok-Tunnel startet, um den lokalen Server global im Internet erreichbar zu machen.
* **`run_chess.sh`**: Das zentrale Start-Skript, das alle Komponenten (Server, Python-Logik, Webserver) mit einem einzigen Befehl initialisiert.

## 🚀 Features

* **Multiplayer über Netzwerk:** Spiele können über das Internet gegen andere Spieler ausgetragen werden.
* **Hybrider Tech-Stack:** Kombination aus der Performance von C++ (Networking) und der Entwicklungsgeschwindigkeit von Python (Spiellogik).
* **Automated Deployment:** Vollständige Orchestrierung und Tunnel-Setup über Shell-Skripting.

## 📦 Voraussetzungen & Installation

Stelle sicher, dass Python 3, ein C++ Compiler (g++) und [ngrok](https://ngrok.com) auf deinem System installiert sind.

1. **Repository klonen:**
   ```bash
   git clone https://github.com
   cd network-chess
   ```

2. **Ausführungsrechte für Shell-Skripte vergeben:**
   ```bash
   chmod +x run_chess.sh Deploy_ngrok.sh
   ```

## 🎮 Spiel starten

Führe einfach das Haupt-Skript aus. Es kompiliert den C++ Server, startet die Python-Spiellogik und öffnet den ngrok-Tunnel:

```bash
./run_chess.sh
```

Nutze die von `Deploy_ngrok.sh` generierte öffentliche URL, um das Spiel im Browser über `index.html` aufzurufen.

