# 🚀 SONAR PRO SEARCH MCP SERVER - INSTALACJA KROK PO KROKU

**Kompletny przewodnik od zera do działającego serwera**

---

## ✅ Przed Rozpoczęciem

### Upewnij Się Że Masz:

- [ ] **Docker Desktop** zainstalowany
- [ ] **Docker Desktop** uruchomiony (sprawdź ikonę w pasku zadań)
- [ ] **Dostęp do internetu**
- [ ] **Konto na OpenRouter** (darmowe)
- [ ] **Claude Desktop** zainstalowany

### Czego Nie Potrzebujesz:

❌ Instalacji Python  
❌ Konfiguracji virtualenv  
❌ Zaawansowanej wiedzy technicznej  
❌ Płatnego konta (free tier wystarczy na start)  

---

## 📦 KROK 1: Pobierz Pliki Projektu

### Opcja A: Z Repository

```bash
# Sklonuj lub pobierz ZIP
git clone <repository-url> sonar-mcp-server
cd sonar-mcp-server
```

### Opcja B: Ręcznie

Stwórz folder `sonar-mcp-server` i skopiuj wszystkie pliki:

```
sonar-mcp-server/
├── sonar_mcp_server.py
├── Dockerfile
├── docker-compose.yml
├── sonar_docker.sh
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
├── LICENSE
├── README_PL.md
├── README.md
├── DOCKER_QUICK_START_PL.md
└── PROJECT_SUMMARY.md
```

---

## 🔑 KROK 2: Uzyskaj Klucz API OpenRouter

### 2.1 Rejestracja (2 minuty)

1. **Otwórz:** https://openrouter.ai/keys
2. **Zaloguj się:**
   - GitHub (zalecane)
   - Google
   - Email
3. **Weryfikuj email** (jeśli wymagane)

### 2.2 Stwórz Klucz API

1. Kliknij **"Create Key"**
2. Nazwij klucz: `claude-mcp-server`
3. Kliknij **"Create"**
4. **Skopiuj klucz** - wygląda tak: `sk-or-v1-xxxxxxxxxxxxx`

⚠️ **WAŻNE:** Zapisz klucz w bezpiecznym miejscu! Nie będziesz mógł go zobaczyć ponownie.

### 2.3 Opcjonalnie: Dodaj Credits

**Free Tier:**
- 10 requests/minute
- Wystarczy do testów

**Paid:**
- Wejdź w **"Credits"**
- Dodaj od $5 (wystarczy na miesiące użytkowania)
- Płatność kartą kredytową

---

## 🛠️ KROK 3: Konfiguracja Projektu

### 3.1 Otwórz Terminal

**macOS:**
```bash
# Otwórz Terminal.app
cd ~/Downloads/sonar-mcp-server  # lub gdzie pobrałeś
```

**Windows:**
```bash
# Otwórz PowerShell lub CMD
cd C:\Users\TwojaNazwa\Downloads\sonar-mcp-server
```

### 3.2 Nadaj Uprawnienia Skryptowi (tylko macOS/Linux)

```bash
chmod +x sonar_docker.sh
```

### 3.3 Uruchom Setup

```bash
./sonar_docker.sh setup
```

**Windows:**
```bash
bash sonar_docker.sh setup
```

### 3.4 Konfiguruj .env

Setup utworzył plik `.env`. Teraz go edytuj:

**macOS/Linux:**
```bash
nano .env
```

**Windows:**
```bash
notepad .env
```

**Zmień linię:**
```bash
OPENROUTER_API_KEY=your_api_key_here
```

**Na:**
```bash
OPENROUTER_API_KEY=sk-or-v1-twój_skopiowany_klucz
```

**Zapisz i zamknij:**
- nano: `Ctrl+X`, `Y`, `Enter`
- notepad: `Ctrl+S`, zamknij

---

## 🐳 KROK 4: Budowanie i Uruchomienie

### 4.1 Sprawdź Docker

```bash
docker --version
```

Powinno pokazać: `Docker version 24.0.0` (lub wyższą)

Jeśli błąd:
1. Uruchom Docker Desktop
2. Poczekaj aż się zainicjalizuje (30-60 sekund)
3. Spróbuj ponownie

### 4.2 Zbuduj Obraz

```bash
./sonar_docker.sh build
```

**Windows:**
```bash
bash sonar_docker.sh build
```

To zajmie **2-5 minut** przy pierwszym razie.

Zobaczysz:
```
Building Docker image...
[+] Building 123.4s (12/12) FINISHED
✓ Image built successfully: sonar-mcp-server:latest
```

### 4.3 Uruchom Serwer

```bash
./sonar_docker.sh start
```

**Windows:**
```bash
bash sonar_docker.sh start
```

Powinno pokazać:
```
Starting Sonar MCP Server...
✓ Container started successfully

Status: RUNNING ✅
CONTAINER NAME       STATUS              PORTS
sonar-mcp-server    Up 3 seconds
```

### 4.4 Sprawdź Status

```bash
./sonar_docker.sh status
```

Jeśli pokazuje `RUNNING` - **gratulacje!** 🎉

---

## 🧪 KROK 5: Testowanie

### 5.1 Uruchom Testy

```bash
./sonar_docker.sh test
```

Powinno pokazać:
```
Testing Sonar MCP Server...

ℹ Testing container health...
✓ Container is healthy

ℹ Testing Python imports...
✓ All dependencies installed correctly

✓ All tests passed!
```

### 5.2 Zobacz Logi

```bash
./sonar_docker.sh logs
```

Powinny być bez błędów (ERROR).

---

## 💻 KROK 6: Konfiguracja Claude Desktop

### 6.1 Znajdź Plik Konfiguracyjny

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/
```

Otwórz plik: `claude_desktop_config.json`

**Windows:**
```
%APPDATA%\Claude\
```

Otwórz plik: `claude_desktop_config.json`

### 6.2 Edytuj Konfigurację

Jeśli plik **nie istnieje**, stwórz go z tym contentem:

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

Jeśli plik **już istnieje** i ma inne serwery MCP, dodaj tylko sekcję `"sonar-pro-search"`:

```json
{
  "mcpServers": {
    "existing-server": {
      ...
    },
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

### 6.3 Zapisz Plik

Upewnij się że:
- ✅ Składnia JSON jest poprawna (przecinki, nawiasy)
- ✅ Nazwa serwera to dokładnie `"sonar-pro-search"`
- ✅ Ścieżka do kontenera to `"sonar-mcp-server"`

---

## 🔄 KROK 7: Restart Claude Desktop

### 7.1 Zamknij Claude Całkowicie

**macOS:**
- `Cmd + Q` (lub prawy klik → Quit)
- Upewnij się że proces się zakończył (sprawdź Activity Monitor)

**Windows:**
- `Alt + F4`
- Sprawdź Task Manager że nie ma procesów Claude

### 7.2 Uruchom Ponownie

Otwórz Claude Desktop na nowo.

### 7.3 Sprawdź Narzędzia

W nowym chacie, kliknij ikonę **🔨** (Tools/Narzędzia) w lewym dolnym rogu.

Powinny być widoczne:
- ✅ `sonar_search`
- ✅ `sonar_ask`
- ✅ `sonar_research`
- ✅ `sonar_reason`

---

## ✨ KROK 8: Pierwszy Test

### 8.1 Napisz do Claude

```
Użyj sonar_search żeby znaleźć najnowsze informacje o GPT-5
```

### 8.2 Sprawdź Wynik

Claude powinien:
1. Wywołać narzędzie `sonar_search`
2. Pokazać parametry zapytania
3. Wyświetlić wyniki z internetu z cytowaniami

### 8.3 Jeśli Działa

**🎉 GRATULACJE! Wszystko działa poprawnie!**

### 8.4 Jeśli Nie Działa

Zobacz sekcję **Rozwiązywanie Problemów** poniżej.

---

## 🔍 Rozwiązywanie Problemów

### Problem: Container nie startuje

**Sprawdź logi:**
```bash
./sonar_docker.sh logs
```

**Możliwe przyczyny:**
1. Port zajęty - restart Dockera
2. Brak zasobów - zamknij inne aplikacje
3. Błąd w .env - sprawdź klucz API

### Problem: "API key not found"

**Rozwiązanie:**
```bash
./sonar_docker.sh config  # Edytuj .env
```

Upewnij się że:
- Klucz zaczyna się od `sk-or-v1-`
- Brak spacji przed/po kluczu
- Nie ma cudzysłowów wokół klucza

### Problem: "401 Unauthorized"

**Przyczyny:**
- Nieprawidłowy klucz API
- Klucz wygasł

**Rozwiązanie:**
1. Sprawdź klucz na https://openrouter.ai/keys
2. Wygeneruj nowy
3. Update .env: `./sonar_docker.sh config`
4. Restart: `./sonar_docker.sh restart`

### Problem: "429 Rate Limit"

**Przyczyny:**
- Za dużo requestów
- Przekroczony free tier (10/min)

**Rozwiązanie:**
1. Poczekaj 1 minutę
2. Rozważ paid plan
3. Użyj mniejszych `max_tokens`

### Problem: Claude nie widzi narzędzi

**Sprawdź:**

1. **Container działa?**
   ```bash
   ./sonar_docker.sh status
   ```
   Jeśli `STOPPED`, uruchom: `./sonar_docker.sh start`

2. **Konfiguracja poprawna?**
   - Otwórz `claude_desktop_config.json`
   - Sprawdź składnię JSON
   - Nazwa kontenera: `sonar-mcp-server`

3. **Claude zrestartowany?**
   - Zamknij całkowicie (Cmd+Q / Alt+F4)
   - Poczekaj 10 sekund
   - Uruchom ponownie

4. **Docker działa?**
   ```bash
   docker ps
   ```
   Powinien pokazać `sonar-mcp-server`

### Problem: Timeout

**Przyczyny:**
- Długie zapytanie
- Wolny internet
- Overloaded OpenRouter

**Rozwiązanie:**
1. Skróć zapytanie
2. Użyj `depth="quick"`
3. Zmniejsz `max_tokens`
4. Spróbuj ponownie za chwilę

---

## 📚 Następne Kroki

### Naucz Się Używać Narzędzi

**1. Podstawowe wyszukiwanie:**
```
Użyj sonar_search z depth="quick": "co to jest Docker?"
```

**2. Szczegółowe pytanie:**
```
Użyj sonar_ask: "Jak działa Kubernetes?" z kontekstem "dla początkujących"
```

**3. Głębokie badania:**
```
Zbadaj: "AI w medycynie" skupiając się na "diagnostyka", "etyka", "precyzja"
```

**4. Złożone rozumowanie:**
```
Pomóż wybrać bazę danych: PostgreSQL vs MongoDB dla e-commerce z 100k użytkowników
```

### Czytaj Dokumentację

- **[README_PL.md](README_PL.md)** - Kompletna dokumentacja
- **[DOCKER_QUICK_START_PL.md](DOCKER_QUICK_START_PL.md)** - Szybki start
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Szczegóły projektu

### Poznaj Komendy Zarządzania

```bash
./sonar_docker.sh help  # Wszystkie komendy
```

Najważniejsze:
- `status` - Status serwera
- `logs` - Ostatnie logi
- `restart` - Restart serwera
- `test` - Testy zdrowia
- `config` - Edycja .env

---

## 💡 Porady Pro

### Optymalizacja Kosztów

1. **Używaj `depth` mądrze:**
   - `quick` - Proste pytania
   - `standard` - Większość przypadków
   - `detailed` - Tylko gdy naprawdę potrzeba

2. **Limituj tokeny:**
   - 1000 - Krótkie odpowiedzi
   - 2000 - Standard
   - 4000+ - Tylko dla badań

3. **Cache wyniki:**
   - Zapisuj często używane informacje
   - Nie pytaj dwa razy o to samo

### Najlepsze Praktyki

1. **Specyficzne pytania = lepsze wyniki:**
   - ❌ "Jak działa AI?"
   - ✅ "Jak działa transformer architecture w GPT-4?"

2. **Używaj kontekstu:**
   - ❌ "Który framework wybrać?"
   - ✅ "Który Python web framework dla API z 10k requests/sec?"

3. **Focus areas w research:**
   - ❌ "Zbadaj blockchain"
   - ✅ "Zbadaj blockchain: 'skalowanie', 'bezpieczeństwo', 'koszty'"

### Monitorowanie

```bash
# Status co 5 sekund
watch -n 5 './sonar_docker.sh status'

# Logi na żywo
./sonar_docker.sh logs-follow

# Resource usage
docker stats sonar-mcp-server
```

---

## 🎓 Dodatkowe Zasoby

### Dokumentacja Zewnętrzna

- **OpenRouter:** https://openrouter.ai/docs
- **MCP Protocol:** https://modelcontextprotocol.io/
- **Docker:** https://docs.docker.com/
- **Perplexity API:** https://docs.perplexity.ai/

### Community

- **MCP Discord:** (link if available)
- **OpenRouter Discord:** https://discord.gg/openrouter
- **Docker Community:** https://forums.docker.com/

---

## ✅ Checklist Końcowa

Przed zamknięciem tego przewodnika, sprawdź:

- [ ] Docker Desktop zainstalowany i działa
- [ ] Klucz API OpenRouter otrzymany i zapisany
- [ ] Wszystkie pliki projektu pobrane
- [ ] `./sonar_docker.sh setup` wykonany
- [ ] `.env` skonfigurowany z kluczem API
- [ ] `./sonar_docker.sh build` ukończony bez błędów
- [ ] `./sonar_docker.sh start` uruchomiony, status RUNNING
- [ ] `./sonar_docker.sh test` przeszedł wszystkie testy
- [ ] `claude_desktop_config.json` poprawnie skonfigurowany
- [ ] Claude Desktop zrestartowany
- [ ] Narzędzia widoczne w Claude (ikona 🔨)
- [ ] Pierwszy test wykonany pomyślnie

Jeśli wszystko ✅ - **GRATULACJE!** 🎉

---

## 🎊 Sukces!

**Masz teraz w pełni działający Sonar Pro Search MCP Server!**

### Co Możesz Teraz Robić:

✅ Wyszukiwać aktualne informacje z internetu  
✅ Zadawać pytania z web-augmented answers  
✅ Prowadzić głębokie badania z wieloma źródłami  
✅ Rozwiązywać złożone problemy z reasoning  
✅ Dostawać odpowiedzi z cytowaniami  
✅ Wszystko w czasie rzeczywistym!  

### Baw Się Dobrze!

```
"Jakie są najnowsze trendy w AI 2024?"
"Porównaj React vs Vue - który lepszy dla mojego projektu?"
"Zbadaj quantum computing: zastosowania, wyzwania, przyszłość"
"Pomóż wybrać cloud provider dla startup'u"
```

---

**Powodzenia w odkrywaniu wiedzy!** 🚀🌐✨

**Built with ❤️ following MCP best practices**

---

*Przewodnik instalacyjny - wersja 1.0*  
*Data: 2024-11-09*
