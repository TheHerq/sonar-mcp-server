# ⚡ Sonar Pro Search MCP Server - Szybki Start

**Od zera do działającego serwera w 5 minut!** 🚀

---

## 📋 Czego Potrzebujesz

- ✅ Docker Desktop (zainstalowany i uruchomiony)
- ✅ Klucz API OpenRouter (darmowy)
- ✅ Claude Desktop

---

## 🚀 Krok 1: Pobierz Klucz API (2 minuty)

1. Idź na: **https://openrouter.ai/keys**
2. Zaloguj się przez GitHub lub Google
3. Kliknij **"Create Key"**
4. Skopiuj klucz (zaczyna się od `sk-or-v1-...`)

💡 **Darmowy tier:** 10 zapytań/minutę - wystarczy do testów!

---

## 🛠️ Krok 2: Setup Serwera (2 minuty)

```bash
# 1. Wejdź do folderu projektu
cd sonar-mcp-server

# 2. Uruchom setup (utworzy plik .env)
./sonar_docker.sh setup

# 3. Edytuj .env i wklej swój klucz API
nano .env  # lub inny edytor
```

W pliku `.env` zmień:
```bash
OPENROUTER_API_KEY=your_api_key_here
```

Na:
```bash
OPENROUTER_API_KEY=sk-or-v1-twój_klucz_tutaj
```

Zapisz i zamknij (Ctrl+X, Y, Enter w nano).

---

## 🐳 Krok 3: Uruchom Serwer (1 minuta)

```bash
# Zbuduj obraz Docker
./sonar_docker.sh build

# Uruchom kontener
./sonar_docker.sh start

# Sprawdź status
./sonar_docker.sh status
```

Powinno pokazać:
```
Status: RUNNING ✅
```

---

## 🔧 Krok 4: Konfiguracja Claude Desktop (2 minuty)

### macOS:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows:
Otwórz:
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Dodaj tę konfigurację:

```json
{
  "mcpServers": {
    "sonar-pro-search": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "sonar-mcp-server",
        "python",
        "sonar_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

**WAŻNE:** Jeśli już masz inne serwery MCP, dodaj tylko sekcję `"sonar-pro-search"` do istniejącej listy!

---

## 🎯 Krok 5: Restart Claude Desktop

1. **Zamknij** Claude Desktop całkowicie (Cmd+Q na Mac, Alt+F4 na Windows)
2. **Uruchom** ponownie
3. Otwórz nowy chat
4. Sprawdź ikonę **🔨** (narzędzia) - powinny być dostępne 4 nowe narzędzia:
   - `sonar_search`
   - `sonar_ask`
   - `sonar_research`
   - `sonar_reason`

---

## ✅ Test Działania

Napisz do Claude:

```
Użyj sonar_search żeby znaleźć najnowsze wiadomości o AI z 2024 roku
```

Jeśli działa - **Gratulacje!** 🎉

---

## 🆘 Coś Nie Działa?

### Problem: Kontener się nie uruchamia
```bash
./sonar_docker.sh logs  # Zobacz co się dzieje
```

### Problem: Błąd "API key not found"
```bash
./sonar_docker.sh config  # Sprawdź .env
```

### Problem: Claude nie widzi narzędzi
1. Sprawdź status: `./sonar_docker.sh status`
2. Sprawdź konfigurację: `claude_desktop_config.json`
3. Restart Claude Desktop

### Problem: Błąd 401
- Sprawdź czy klucz API jest poprawny
- Wygeneruj nowy na https://openrouter.ai/keys

---

## 📖 Co Dalej?

### Używaj Narzędzi!

**Szybkie wyszukiwanie:**
```
Użyj sonar_search z depth="quick": "co to jest MCP?"
```

**Pytanie z kontekstem:**
```
Użyj sonar_ask: "Jak działa Docker?" z kontekstem "jestem początkującym"
```

**Głębokie badania:**
```
Zbadaj: "kwantowe komputery w 2024" skupiając się na "zastosowania" i "wyzwania"
```

**Złożone rozumowanie:**
```
Pomóż wybrać między PostgreSQL a MongoDB dla aplikacji z 1M użytkowników
```

### Przeczytaj Pełną Dokumentację

- **[README_PL.md](README_PL.md)** - Kompletna dokumentacja po polsku
- **[README.md](README.md)** - English version

---

## 📊 Komendy Zarządzania

```bash
# Status
./sonar_docker.sh status

# Logi
./sonar_docker.sh logs

# Restart
./sonar_docker.sh restart

# Stop
./sonar_docker.sh stop

# Pomoc
./sonar_docker.sh help
```

---

## 💰 Koszty

**Free Tier OpenRouter:**
- ✅ 10 zapytań/minutę
- ✅ Idealne do nauki i testów
- ✅ Zero kosztów początkowych

**Paid Plans:**
- ~$0.001-0.003 per zapytanie
- Więcej informacji: https://openrouter.ai/models

---

## 🎉 Gotowe!

**Masz działający Sonar Pro Search MCP Server!**

### Sprawdź:
- ✅ Docker działa
- ✅ Klucz API skonfigurowany
- ✅ Claude Desktop widzi narzędzia
- ✅ Możesz wyszukiwać w internecie!

**Powodzenia w odkrywaniu wiedzy!** 🚀🌐✨

---

**PS:** Jeśli chcesz też akademickie papers, zobacz **ArXiv MCP Server**!
