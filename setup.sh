#!/bin/bash
set -e

echo "=== Deep Talk Bot — Setup ==="

# 1. Обновляем систему
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# 2. Создаём virtualenv и устанавливаем зависимости
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Настраиваем .env (если нет)
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo ">>> Заполни .env:"
    echo "    nano .env"
    echo ""
fi

# 4. Устанавливаем systemd-сервис
sudo cp deep_talk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable deep_talk

echo ""
echo "=== Готово! ==="
echo ""
echo "Следующие шаги:"
echo "  1. nano .env              — вставить BOT_TOKEN и OPENROUTER_API_KEY"
echo "  2. sudo systemctl start deep_talk  — запустить бота"
echo "  3. sudo systemctl status deep_talk — проверить статус"
echo "  4. journalctl -u deep_talk -f      — следить за логами"
