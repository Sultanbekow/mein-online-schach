#!/bin/bash

# --- KONFIGURATION ---
CPP_SERVER_SOURCE="chess_server.cpp"
CPP_SERVER_BINARY="chess_server"
PYTHON_CLIENT="schach_spiel_final.py"
PORT=5555
WEBSOCKET_PORT=8080

# Farben für Terminal-Ausgaben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/5] Kompiliere C++ Netzwerk-Server...${NC}"
if ! g++ -O3 "$CPP_SERVER_SOURCE" -o "$CPP_SERVER_BINARY"; then
    echo -e "${RED}Fehler: C++ Kompilierung fehlgeschlagen!${NC}"
    exit 1
fi
echo -e "${GREEN}C++ Server erfolgreich kompiliert.${NC}"

# Überprüfen, ob websocat installiert ist (Brücke zum Browser)
if ! command -v websocat &> /dev/null; then
    echo -e "${BLUE}[INFO] Installiere websocat als Brücke für den Browser...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install websocat
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y websocat
    fi
fi

echo -e "${BLUE}[2/5] Starte C++ Schach-Server im Hintergrund...${NC}"
./"$CPP_SERVER_BINARY" &
SERVER_PID=$!

# Kurz warten, bis der C++ Port bereit ist
sleep 1

echo -e "${BLUE}[3/5] Starte WebSocket-Relay für Webbrowser...${NC}"
# Leitet Browser-WebSocket-Traffic an den C++ TCP-Server weiter
websocat -t ws-l:127.0.0.1:$WEBSOCKET_PORT tcp:127.0.0.1:$PORT &
RELAY_PID=$!

echo -e "${BLUE}[4/5] Starte zwei autarke Python-Clients (Weiß & Schwarz)...${NC}"
python3 "$PYTHON_CLIENT" &
CLIENT1_PID=$!
sleep 0.5
python3 "$PYTHON_CLIENT" &
CLIENT2_PID=$!

echo -e "${BLUE}[5/5] Öffne das Spiel-Interface im Webbrowser...${NC}"
# Erstellt eine temporäre HTML-Datei für den Browser-Zugriff
HTML_FILE="/tmp/chess_status.html"
cat <<EOF > "$HTML_FILE"
<!DOCTYPE html>
<html>
<head>
    <title>Schachspiel Live-Status</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f3e5ab; text-align: center; padding-top: 50px; }
        .container { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1 { color: #b58863; }
        .status { font-size: 18px; color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Schachspiel Online-Verbindung</h1>
        <p class="status">● Spiel erfolgreich geladen</p>
        <p>Die Python-Clients wurden gestartet und sind über das C++ Backend auf Port $PORT (WebSocket: $WEBSOCKET_PORT) verbunden.</p>
        <p>Viel Spaß beim Spielen!</p>
    </div>
</body>
</html>
EOF

# Öffnet die Seite im Standardbrowser (macOS / Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$HTML_FILE"
else
    xdg-open "$HTML_FILE" 2>/dev/null || sensible-browser "$HTML_FILE"
fi

echo -e "${GREEN}Alles erfolgreich gestartet! Drücke [STRG+C] im Terminal, um alle Prozesse zu beenden.${NC}"

# Sicherstellen, dass beim Schließen des Skripts alle Hintergrundprozesse gekillt werden
cleanup() {
    echo -e "\n${RED}Beende alle Schach-Prozesse...${NC}"
    kill $SERVER_PID $RELAY_PID $CLIENT1_PID $CLIENT2_PID 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

# Hält das Skript aktiv
wait

