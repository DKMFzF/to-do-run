#!/bin/bash

set -e 

REPO_URL="https://github.com/skeiigi/ToDoRun.git"
PROJECT_DIR="ToDoRun"
VENV_DIR="venv"
PLATFORM=$(uname -s)

echo "[LOG]: Начало развертывания приложения ToDoRun"

echo "[LOG]: Создание виртуального окружения"

if [[ "$PLATFORM" == "Linux" ]] || [[ "$PLATFORM" == "Darwin" ]]; then
    python3 -m venv $VENV_DIR
    ACTIVATE_CMD="source $VENV_DIR/bin/activate"
elif [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "CYGWIN"* ]]; then
    python -m venv $VENV_DIR
    ACTIVATE_CMD="source $VENV_DIR/Scripts/activate"
else
    echo "[LOG]: Неподдерживаемая платформа: $PLATFORM"
    exit 1
fi

echo "[LOG]: Активация виртуального окружения"
eval $ACTIVATE_CMD

if [[ "$PLATFORM" == "MSYS"* ]]; then
    echo "[LOG]: Для пользователей PowerShell выполните следующие команды вручную:"
    echo "[LOG]: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
    echo ".\\$VENV_DIR\\Scripts\\Activate.ps1"
fi

if [ -f "requirements.txt" ]; then
    echo "[LOG]: Установка зависимостей Python"
    pip install -r requirements.txt
else
    echo "[LOG]: Файл requirements.txt не найден. Пропуск установки зависимостей"
fi

echo "[LOG]: Настройка окружения завершена"

echo ""
echo "[LOG]: Вируталка развёрнута"
echo "[LOG]: Для повторной активации виртуального окружения нужно прописать:"
if [[ "$PLATFORM" == "Linux" ]] || [[ "$PLATFORM" == "Darwin" ]]; then
    echo "  source $VENV_DIR/bin/activate"
else
    echo "  source $VENV_DIR/Scripts/activate"
fi
