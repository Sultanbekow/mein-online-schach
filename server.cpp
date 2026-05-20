#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 5555
#define BUFFER_SIZE 1024

int main() {
    int server_fd, player1_fd, player2_fd;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    // 1. Socket erstellen
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        std::cerr << "Socket-Erstellung fehlgeschlagen.\n";
        return -1;
    }

    // 2. Port freigeben (verhindert Blockaden beim Neustart)
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        std::cerr << "Setsockopt fehlgeschlagen.\n";
        return -1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons(PORT);

    // 3. Socket an Port binden
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        std::cerr << "Bind fehlgeschlagen. Ist der Port 5555 besetzt?\n";
        return -1;
    }

    // 4. Auf Verbindungen warten
    if (listen(server_fd, 2) < 0) {
        std::cerr << "Listen fehlgeschlagen.\n";
        return -1;
    }

    std::cout << "[SERVER] Schach-Server läuft auf Port " << PORT << "...\n";
    std::cout << "[SERVER] Warte auf Spieler 1 (Weiß)...\n";

    // Spieler 1 (Weiß) akzeptieren
    player1_fd = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
    std::cout << "[SERVER] Spieler 1 (Weiß) über das Relay verbunden!\n";
    send(player1_fd, "COLOR:W", 7, 0); 

    std::cout << "[SERVER] Warte auf Spieler 2 (Schwarz)...\n";

    // Spieler 2 (Schwarz) akzeptieren
    player2_fd = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
    std::cout << "[SERVER] Spieler 2 (Schwarz) über das Relay verbunden!\n";
    send(player2_fd, "COLOR:B", 7, 0); 

    std::cout << "[SERVER] Beide Spieler verbunden. Match läuft!\n";

    // 5. Hauptschleife: Weiterleitung aller Züge und Befehle (z.B. Aufgeben/Remis)
    while (true) {
        // Nachricht von Spieler 1 empfangen und an Spieler 2 senden
        std::memset(buffer, 0, BUFFER_SIZE);
        int valread = recv(player1_fd, buffer, BUFFER_SIZE, 0);
        if (valread <= 0) {
            std::cout << "[SERVER] Verbindung zu Spieler 1 verloren.\n";
            break;
        }
        std::cout << "[DATEN] Weiß -> Schwarz: " << buffer << "\n";
        send(player2_fd, buffer, valread, 0);

        // Nachricht von Spieler 2 empfangen und an Spieler 1 senden
        std::memset(buffer, 0, BUFFER_SIZE);
        valread = recv(player2_fd, buffer, BUFFER_SIZE, 0);
        if (valread <= 0) {
            std::cout << "[SERVER] Verbindung zu Spieler 2 verloren.\n";
            break;
        }
        std::cout << "[DATEN] Schwarz -> Weiß: " << buffer << "\n";
        send(player1_fd, buffer, valread, 0);
    }

    // Sockets schließen
    close(player1_fd);
    close(player2_fd);
    close(server_fd);
    std::cout << "[SERVER] Server sauber beendet.\n";
    return 0;
}

