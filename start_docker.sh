#!/bin/bash
echo "X11 (Grafik Arayüzü) yetkileri ayarlanıyor..."
xhost +local:docker

echo "Docker konteyneri derleniyor ve başlatılıyor..."
docker compose up --build -d

echo "Konteynerin terminaline bağlanılıyor..."
docker exec -it leo_sim_container bash
