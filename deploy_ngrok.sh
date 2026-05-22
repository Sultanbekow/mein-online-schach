#!/bin/bash

# 1. Sicherstellen, dass ngrok läuft
if ! curl -s http://127.0.0 > /dev/null; then
    echo "❌ Fehler: ngrok läuft nicht! Bitte starte zuerst 'ngrok http 8080' in einem anderen Terminal."
    exit 1
fi

# 2. Die aktuelle wss-URL live aus der ngrok API auslesen
NGROK_URL=$(curl -s http://127.0.0 | grep -o '"public_url":"[^\"]*"' | head -n 1 | cut -d'"' -f4)

# Konvertiere https:// in wss:// (falls ngrok als http läuft)
NGROK_URL=${NGROK_URL/https:/wss:}
NGROK_URL=${NGROK_URL/http:/ws:}

echo "🔗 Erkannte ngrok URL: $NGROK_URL"

# 3. Sicherheitskopie der originalen index.html erstellen, um den Platzhalter nicht zu verlieren
cp index.html index.html.tmp

# 4. Platzhalter in der Datei durch die echte URL ersetzen (macOS-kompatibler sed Befehl)
sed -i '' "s|NGROK_URL_PLACEHOLDER|$NGROK_URL|g" index.html

# 5. Zu GitHub hochladen, damit GitHub Pages aktualisiert wird
echo "🚀 Pushe aktualisierte index.html zu GitHub..."
git add index.html
git commit -m "Update dynamic ngrok backend URL"
git push

# 6. Die lokale index.html wieder in den Originalzustand (mit Platzhalter) versetzen
mv index.html.tmp index.html
echo "✅ Fertig! GitHub Pages wird in ca. 1 Minute aktualisiert."

