# ⚡ Quick Start

Создай первый проект за 2 минуты!

---

## 1️⃣ Установка

```bash
pip install ai-toolkit
```

---

## 2️⃣ Создание проекта

**Вариант A: Web Dashboard**
```bash
ai-toolkit dashboard
```

**Вариант B: Одна команда**
```bash
ai-toolkit create my_bot --template bot
```

---

## 3️⃣ Настройка

```bash
cd my_bot

# Создать venv (вне проекта!)
./scripts/bootstrap.sh

# Активировать
source ../_venvs/my_bot-venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Настроить .env
cp .env.example .env
```

---

## 4️⃣ Запуск

```bash
python main.py
```

---

## 🎉 Готово!

### Что дальше?

- [📖 Полное руководство](GUIDE.md)
- [📦 Шаблоны проектов](../README.md#-шаблоны-проектов)
- [🎮 Context Switcher](GUIDE.md#context-switcher)
- [❓ FAQ](FAQ.md)

