# 🌐 Sonar Pro Search MCP Server

**Zaawansowany serwer MCP do inteligentnego wyszukiwania w internecie z wykorzystaniem Perplexity Sonar Pro przez OpenRouter**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Spis Treści

- [Czym Jest Ten Serwer](#czym-jest-ten-serwer)
- [Funkcje i Możliwości](#funkcje-i-możliwości)
- [Szybki Start](#szybki-start)
- [Szczegółowa Instalacja](#szczegółowa-instalacja)
- [Dostępne Narzędzia](#dostępne-narzędzia)
- [Konfiguracja Claude Desktop](#konfiguracja-claude-desktop)
- [Przykłady Użycia](#przykłady-użycia)
- [Zarządzanie](#zarządzanie)
- [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
- [Bezpieczeństwo](#bezpieczeństwo)

---

## 🎯 Czym Jest Ten Serwer

Sonar Pro Search MCP Server to profesjonalny serwer Model Context Protocol, który daje Claude dostęp do zaawansowanego wyszukiwania w internecie poprzez API Perplexity Sonar Pro (przez OpenRouter).

### Kluczowe Zalety

✅ **Informacje w Czasie Rzeczywistym** - Dostęp do aktualnych danych z internetu  
✅ **Inteligentne Wyszukiwanie** - AI-powered search z automatycznymi cytowaniami  
✅ **4 Wyspecjalizowane Narzędzia** - Od szybkiego wyszukiwania po głębokie badania  
✅ **Docker Ready** - Łatwa instalacja i deployment  
✅ **Production Quality** - Pełna obsługa błędów, limity, logowanie  
✅ **Dokumentacja PL** - Kompletna dokumentacja po polsku  

---

## ⚡ Funkcje i Możliwości

### 1. **Sonar Search** 🔍
Podstawowe wyszukiwanie z trzema poziomami głębokości:
- **Quick** (~1000 tokenów) - Szybkie odpowiedzi
- **Standard** (~2000 tokenów) - Zbalansowane wyniki
- **Detailed** (~4000 tokenów) - Kompleksowa analiza

### 2. **Sonar Ask** 💬
Konwersacyjne pytania z kontekstem:
- Naturalne pytania w języku naturalnym
- Opcjonalny kontekst do personalizacji
- Cytowania ze źródeł

### 3. **Sonar Research** 📚
Głębokie badania z wieloma źródłami:
- Do 6000 tokenów szczegółowych raportów
- Opcjonalne focus areas (do 5)
- Strukturyzowana analiza z sekcjami

### 4. **Sonar Reason** 🧠
Kompleksowe rozumowanie krok po kroku:
- Wykorzystanie modelu reasoning-pro
- Analiza wieloczynnikowa
- Uwzględnienie ograniczeń (constraints)

---

## 🚀 Szybki Start

### Wymagania

- **Docker Desktop** zainstalowany i uruchomiony
- **Klucz API OpenRouter** (darmowy tier dostępny)
- **Claude Desktop** (do integracji)

### 3 Kroki do Uruchomienia

```bash
# 1. Setup - sprawdzenie środowiska i utworzenie .env
./sonar_docker.sh setup

# 2. Build - zbudowanie obrazu Docker
./sonar_docker.sh build

# 3. Start - uruchomienie serwera
./sonar_docker.sh start
```

**To wszystko!** 🎉 Serwer jest gotowy do pracy.

---

## 📖 Szczegółowa Instalacja

### Krok 1: Pobierz Klucz API

1. Idź na: https://openrouter.ai/keys
2. Zaloguj się (GitHub/Google)
3. Skopiuj swój API key
4. (Opcjonalnie) Dodaj credits dla wyższych limitów

### Krok 2: Konfiguracja

```bash
# Sklonuj/pobierz repozytorium
cd sonar-mcp-server

# Uruchom setup
./sonar_docker.sh setup

# Edytuj .env i dodaj swój klucz API
nano .env  # lub inny edytor
```

W pliku `.env`:
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx  # Twój klucz tutaj
```

### Krok 3: Budowanie i Uruchomienie

```bash
# Zbuduj obraz Docker
./sonar_docker.sh build

# Uruchom kontener
./sonar_docker.sh start

# Sprawdź status
./sonar_docker.sh status
```

### Krok 4: Testowanie

```bash
# Uruchom testy
./sonar_docker.sh test

# Zobacz logi
./sonar_docker.sh logs
```

---

## 🛠️ Dostępne Narzędzia

### 1. `sonar_search`

**Podstawowe wyszukiwanie w internecie**

```python
{
  "query": "quantum computing trends 2024",
  "depth": "standard",  # quick / standard / detailed
  "response_format": "markdown"  # markdown / json
}
```

**Przykłady zastosowań:**
- Bieżące wydarzenia: "latest AI breakthroughs 2024"
- Porównania technologii: "PostgreSQL vs MySQL 2024"
- Badania rynku: "electric vehicle market trends"
- Weryfikacja faktów: "verify recent scientific claims"

### 2. `sonar_ask`

**Konwersacyjne pytania z kontekstem**

```python
{
  "question": "How does OAuth 2.0 authentication work?",
  "context": "I'm building a REST API",  # opcjonalnie
  "max_tokens": 2000,
  "response_format": "markdown"
}
```

**Przykłady zastosowań:**
- Wyjaśnienia techniczne: "How does Docker networking work?"
- Instrukcje: "How to deploy Django to AWS?"
- Analizy porównawcze: "REST vs GraphQL differences"
- Zapytania medyczne: "What are symptoms of vitamin D deficiency?"

### 3. `sonar_research`

**Głębokie badania z wieloma źródłami**

```python
{
  "topic": "post-quantum cryptography adoption",
  "focus_areas": [  # opcjonalnie, max 5
    "current standards",
    "implementation challenges",
    "migration strategies"
  ],
  "max_tokens": 5000,
  "response_format": "markdown"
}
```

**Przykłady zastosowań:**
- Badania rynku: "AI chip market landscape 2024"
- Ocena technologii: "Kubernetes alternatives"
- Badania akademickie: "CRISPR gene editing advances"
- Analiza biznesowa: "SaaS pricing strategies"

### 4. `sonar_reason`

**Kompleksowe rozumowanie**

```python
{
  "problem": "Choose optimal database for IoT sensor data",
  "constraints": "Budget $500/month, 1M writes/day",  # opcjonalnie
  "max_tokens": 3000,
  "response_format": "markdown"
}
```

**Przykłady zastosowań:**
- Decyzje architektoniczne: "monolithic vs microservices"
- Wybór technologii: "best database for analytics"
- Analiza bezpieczeństwa: "zero-trust architecture approaches"
- Optymalizacja wydajności: "bottlenecks in web app"

---

## 🔧 Konfiguracja Claude Desktop

### macOS

Edytuj plik konfiguracyjny:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows

Edytuj plik:
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Konfiguracja

Dodaj do pliku:

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

### Restart Claude Desktop

Po dodaniu konfiguracji:
1. Zamknij Claude Desktop całkowicie
2. Uruchom ponownie
3. Sprawdź czy narzędzia są dostępne (ikona 🔨 w interface)

---

## 💡 Przykłady Użycia

### Przykład 1: Wyszukiwanie Aktualności

**Ty:** "Użyj sonar_search żeby znaleźć najnowsze informacje o GPT-5"

**Claude wywoła:**
```python
sonar_search({
  "query": "GPT-5 latest news announcements",
  "depth": "detailed"
})
```

### Przykład 2: Techniczne Pytanie

**Ty:** "Użyj sonar_ask - jak działa Kubernetes autoscaling?"

**Claude wywoła:**
```python
sonar_ask({
  "question": "How does Kubernetes autoscaling work?",
  "context": "Explain for production environments",
  "max_tokens": 2500
})
```

### Przykład 3: Głębokie Badania

**Ty:** "Zbadaj zastosowania AI w medycynie, skup się na diagnostyce i etyce"

**Claude wywoła:**
```python
sonar_research({
  "topic": "AI applications in medicine",
  "focus_areas": ["diagnostics", "ethics", "accuracy"],
  "max_tokens": 5000
})
```

### Przykład 4: Złożone Rozumowanie

**Ty:** "Pomóż wybrać bazę danych dla aplikacji real-time analytics"

**Claude wywoła:**
```python
sonar_reason({
  "problem": "Select database for real-time analytics platform with millions of events per day",
  "constraints": "Open source, budget $1000/month, sub-100ms queries",
  "max_tokens": 3500
})
```

---

## ⚙️ Zarządzanie

### Podstawowe Komendy

```bash
# Status serwera
./sonar_docker.sh status

# Restart
./sonar_docker.sh restart

# Logi (ostatnie 100 linii)
./sonar_docker.sh logs

# Logi na żywo
./sonar_docker.sh logs-follow

# Shell w kontenerze
./sonar_docker.sh shell

# Test zdrowia
./sonar_docker.sh test

# Update serwera
./sonar_docker.sh update

# Edycja konfiguracji
./sonar_docker.sh config
```

### Wszystkie Dostępne Komendy

```bash
./sonar_docker.sh help
```

Pokaże:
- `setup` - Początkowa konfiguracja
- `build` - Zbudowanie obrazu
- `start` - Uruchomienie kontenera
- `stop` - Zatrzymanie kontenera
- `restart` - Restart
- `status` - Status i zasoby
- `logs` - Wyświetl logi
- `logs-follow` - Śledź logi na żywo
- `shell` - Otwórz shell w kontenerze
- `test` - Testy zdrowia
- `update` - Przebuduj i restart
- `config` - Edytuj .env
- `clean` - Usuń kontener i obraz

---

## 🔍 Rozwiązywanie Problemów

### Serwer się nie uruchamia

```bash
# Sprawdź logi
./sonar_docker.sh logs

# Sprawdź czy Docker działa
docker ps

# Sprawdź konfigurację
./sonar_docker.sh config
```

### Brak klucza API

```
ValueError: OpenRouter API key not found
```

**Rozwiązanie:**
1. Edytuj `.env`: `./sonar_docker.sh config`
2. Dodaj swój klucz: `OPENROUTER_API_KEY=sk-or-v1-xxxxx`
3. Restart: `./sonar_docker.sh restart`

### Błąd 401 (Authentication Failed)

**Przyczyny:**
- Nieprawidłowy klucz API
- Klucz wygasł

**Rozwiązanie:**
1. Sprawdź klucz na: https://openrouter.ai/keys
2. Wygeneruj nowy jeśli potrzeba
3. Zaktualizuj `.env`

### Błąd 429 (Rate Limit)

**Przyczyny:**
- Za dużo requestów
- Przekroczony free tier

**Rozwiązanie:**
1. Poczekaj kilka minut
2. Rozważ upgrade planu na OpenRouter
3. Użyj niższego `max_tokens`

### Timeout

**Przyczyny:**
- Zbyt długie zapytanie
- Problemy z siecią

**Rozwiązanie:**
1. Skróć zapytanie
2. Zmniejsz `max_tokens`
3. Sprawdź połączenie internetowe

### Claude nie widzi narzędzi

**Sprawdź:**
1. Czy kontener działa: `./sonar_docker.sh status`
2. Czy konfiguracja jest poprawna: `claude_desktop_config.json`
3. Czy Claude Desktop został zrestartowany

---

## 🔐 Bezpieczeństwo

### Najlepsze Praktyki

✅ **Nigdy nie commituj `.env`** - Zawiera klucz API  
✅ **Używaj `.env.example`** - Jako szablonu  
✅ **Regularnie rotuj klucze** - Co kilka miesięcy  
✅ **Monitoruj użycie** - Na dashboard OpenRouter  
✅ **Limituj zasoby** - Docker resource limits  

### Ochrona Klucza API

```bash
# Ustaw odpowiednie uprawnienia
chmod 600 .env

# Dodaj do .gitignore
echo ".env" >> .gitignore
```

### Resource Limits

W `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
```

### Monitoring

```bash
# Użycie zasobów
docker stats sonar-mcp-server

# Logi błędów
./sonar_docker.sh logs | grep ERROR
```

---

## 📊 Koszty i Limity

### OpenRouter Pricing

**Free Tier:**
- 10 requests/minute
- Idealne do testów i osobistego użytku

**Paid Plans:**
- Pay-as-you-go
- ~$0.001-0.003 per request (zależnie od modelu)
- Wyższe rate limits

**Sprawdź:**
- https://openrouter.ai/models/perplexity/sonar-pro
- https://openrouter.ai/models/perplexity/sonar-reasoning-pro

### Optymalizacja Kosztów

1. **Używaj odpowiedniego `depth`**
   - `quick` dla prostych pytań
   - `detailed` tylko gdy potrzeba

2. **Limituj `max_tokens`**
   - Nie zawsze potrzeba 6000 tokenów
   - 1000-2000 często wystarczy

3. **Cache wyniki**
   - Zapisuj często używane odpowiedzi
   - Unikaj duplikatów zapytań

---

## 📚 Dodatkowa Dokumentacja

- **[DOCKER_QUICK_START_PL.md](DOCKER_QUICK_START_PL.md)** - Szybki start w 5 minut
- **[README.md](README.md)** - English documentation
- **OpenRouter Docs**: https://openrouter.ai/docs
- **MCP Docs**: https://modelcontextprotocol.io/

---

## 🤝 Wsparcie

### Masz Problemy?

1. Sprawdź [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
2. Zobacz logi: `./sonar_docker.sh logs`
3. Testuj: `./sonar_docker.sh test`

### Dalsze Pytania

- OpenRouter Support: https://openrouter.ai/
- MCP Documentation: https://modelcontextprotocol.io/
- Docker Help: https://docs.docker.com/

---

## 📄 Licencja

MIT License - Zobacz [LICENSE](LICENSE) dla szczegółów

---

## 🎉 Gotowe!

Twój Sonar Pro Search MCP Server jest gotowy do użycia! 🚀

**Następne Kroki:**
1. ✅ Uruchom serwer: `./sonar_docker.sh start`
2. ✅ Skonfiguruj Claude Desktop
3. ✅ Zacznij wyszukiwać!

**Powodzenia w odkrywaniu wiedzy z internetu!** 🌐🔍✨
