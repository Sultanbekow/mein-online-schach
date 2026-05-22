# Basis-Image mit C++ und Python
FROM ubuntu:22.04

# Zeitzone-Abfragen während der Installation unterdrücken
ENV DEBIAN_FRONTEND=noninteractive

# Benötigte Pakete installieren (C++ Compiler, CMake, Python)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# Projektdateien in den Container kopieren
COPY . .

# Ausführungsrechte für Ihr Bash-Skript vergeben
RUN chmod +x run_chess.sh

# WebSocket-Port (8080) im Container öffnen
EXPOSE 8080

# Das Bash-Skript beim Start des Containers ausführen
CMD ["./run_chess.sh"]

