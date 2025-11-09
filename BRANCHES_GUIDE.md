# 🌿 Branch Structure Guide

## Struktura branchy projektu

### 📍 **main** - Wersja lokalna (stdio)
- **Przeznaczenie:** Użycie lokalne przez Claude Desktop / Cursor
- **Tryb:** stdio (Standard Input/Output)
- **Setup:** `docker compose up` lub bezpośrednio przez Python
- **Konfiguracja MCP:**
  ```json
  {
    "mcpServers": {
      "sonar": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "--env-file", ".env", "sonar-mcp-server"]
      }
    }
  }
  ```

### 🚀 **remote-sse** - Wersja zdalna (HTTP/SSE)
- **Przeznaczenie:** Deployment na VPS (Hostinger)
- **Tryb:** Server-Sent Events (SSE) przez HTTP
- **Port:** 8081
- **Endpoint:** `http://host:8081/sse`
- **Cloudflare Tunnel:** Tak
- **Setup:** `docker compose up -d` (na VPS)
- **Konfiguracja MCP:**
  ```json
  {
    "mcpServers": {
      "sonar-remote": {
        "url": "https://sonar.yourdomain.com/sse"
      }
    }
  }
  ```

---

## 🔄 Praca z branchami

### Przełączanie między wersjami:

```bash
# Praca lokalna (stdio)
git checkout main

# Deployment na VPS (SSE)
git checkout remote-sse
```

### Synchronizacja zmian:

```bash
# Jeśli dodajesz nowe funkcje (tools) na main
git checkout main
# ... wprowadź zmiany ...
git add .
git commit -m "feat: add new tool X"

# Przenieś zmiany do remote-sse
git checkout remote-sse
git merge main -m "merge: sync new tools from main"

# Jeśli są konflikty w plikach deployment (rzadkie):
# - Dockerfile - zostaw wersję remote-sse (z EXPOSE, healthcheck HTTP)
# - docker-compose.yml - zostaw wersję remote-sse (z portami)
# - sonar_mcp_server.py - main: mcp.run() vs remote-sse: uvicorn.run()
```

### Merge strategy:

**Zwykle mergujemy:** `main → remote-sse`
(Nowe funkcje dodajemy na main, potem przenosimy do remote-sse)

**NIE mergujemy:** `remote-sse → main`
(Deployment config nie powinien wracać do main)

---

## 📋 Różnice między branchami

| Plik | main (stdio) | remote-sse (SSE) |
|------|--------------|------------------|
| **sonar_mcp_server.py** | `mcp.run()` | `uvicorn.run(mcp.sse_app())` |
| **requirements.txt** | bez uvicorn | + `uvicorn>=0.32.0` |
| **Dockerfile** | stdio, basic healthcheck | EXPOSE 8081, HTTP healthcheck |
| **docker-compose.yml** | bez portów, stdin/tty | ports: 8081:8081, env vars |
| **REMOTE_MCP_SETUP.md** | ❌ brak | ✅ pełny deployment guide |

---

## 🧪 Testowanie

### Test lokalny (main):
```bash
git checkout main
docker compose up

# W innym terminalu - test przez stdio
docker exec -i sonar-mcp-server python -c "print('test')"
```

### Test SSE (remote-sse):
```bash
git checkout remote-sse
docker compose up -d

# Test HTTP endpoint
curl -i -m 2 http://localhost:8081/sse
```

Oczekiwany wynik:
```
HTTP/1.1 200 OK
content-type: text/event-stream; charset=utf-8

event: endpoint
data: /messages/?session_id=...
```

---

## 🚢 Deployment workflow

### 1. Rozwój lokalny (main):
```bash
git checkout main
# ... dodaj nowe narzędzia, poprawki ...
git add .
git commit -m "feat: description"
git push origin main
```

### 2. Sync do remote-sse:
```bash
git checkout remote-sse
git merge main
# Rozwiąż ewentualne konflikty (deployment files)
git push origin remote-sse
```

### 3. Deploy na VPS:
```bash
# SSH na VPS Hostinger
ssh user@your-vps

# Pull najnowszej wersji
cd sonar-mcp-server
git fetch origin
git checkout remote-sse
git pull origin remote-sse

# Rebuild i restart
docker compose down
docker compose build --no-cache
docker compose up -d

# Sprawdź logi
docker compose logs -f
```

---

## 🔧 Przydatne komendy

```bash
# Sprawdź na którym branchu jesteś
git branch

# Zobacz różnice między branchami
git diff main remote-sse

# Zobacz pliki zmienione między branchami
git diff main remote-sse --name-only

# Zobacz logi commitów
git log --oneline --graph --all

# Sprawdź konkretny plik na innym branchu (bez przełączania)
git show remote-sse:sonar_mcp_server.py | tail -20

# Porównaj plik między branchami
git diff main remote-sse -- sonar_mcp_server.py
```

---

## ⚠️ Ważne zasady

1. **NIE commituj .env** - jest w .gitignore
2. **Zawsze testuj lokalnie** przed merge do remote-sse
3. **main = single source of truth** dla logiki biznesowej
4. **remote-sse = deployment config** + logika z main
5. **Deploy** zawsze z brancha remote-sse, nigdy z main

---

## 📊 Current status

```bash
# Sprawdź obecny stan
git branch -v

# Powinno pokazać:
# * main       d59510b chore: add Claude Code local settings to gitignore
#   remote-sse 496e5c7 feat: add Remote MCP support with SSE endpoint
```

---

## 🎯 Quick reference

| Chcę... | Branch | Komenda |
|---------|--------|---------|
| Dodać nowe narzędzie | `main` | `git checkout main` |
| Przetestować lokalnie | `main` | `docker compose up` |
| Deploy na VPS | `remote-sse` | `git checkout remote-sse` |
| Sync nowe funkcje | `remote-sse` | `git merge main` |
| Sprawdzić endpoint SSE | `remote-sse` | `curl http://localhost:8081/sse` |

---

**Dokumentacja utworzona:** 2025-11-09
**Ostatnia aktualizacja:** 2025-11-09
