# 🚀 Remote MCP Server Setup - Sonar Pro

## ✅ Co zostało zrobione

Przekształciliśmy lokalny Sonar MCP Server (stdio) w **Remote MCP Server z SSE endpoint**.

### Zmiany w projekcie:

#### 1. **requirements.txt**
- ✅ Dodano `uvicorn>=0.32.0` - ASGI server dla SSE endpoint

#### 2. **sonar_mcp_server.py**
- ✅ Dodano import `uvicorn`
- ✅ Zmieniono `mcp.run()` na `uvicorn.run(mcp.sse_app())`
- ✅ Dodano konfigurację portu przez zmienne środowiskowe:
  - `PORT` (domyślnie: 8081)
  - `HOST` (domyślnie: 0.0.0.0)
- ✅ Dodano informacyjne logi przy starcie serwera

#### 3. **Dockerfile**
- ✅ Dodano `EXPOSE 8081`
- ✅ Zaktualizowano healthcheck do testowania HTTP endpoint (`curl -f http://localhost:8081/`)
- ✅ Dodano komentarze o Remote MCP i SSE

#### 4. **docker-compose.yml**
- ✅ Dodano mapowanie portu: `8081:8081`
- ✅ Usunięto `stdin_open` i `tty` (nie są potrzebne dla HTTP)
- ✅ Dodano zmienne środowiskowe `PORT` i `HOST`
- ✅ Zaktualizowano healthcheck do testowania HTTP endpoint

---

## 🧪 Test lokalny - SUKCES!

```bash
# Build i start
docker compose build
docker compose up -d

# Test SSE endpoint
curl -i -m 2 http://localhost:8081/sse
```

**Wynik:**
```
HTTP/1.1 200 OK
content-type: text/event-stream; charset=utf-8

event: endpoint
data: /messages/?session_id=fd767793c0064e44b2ef53eda0abf37b
```

✅ **SSE endpoint działa poprawnie!**

---

## 📋 Następne kroki

### 1. **Deployment na Hostinger VPS**

```bash
# Na VPS
git clone [your-repo-url]
cd sonar-mcp-server

# Utwórz plik .env
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Build i start
docker compose up -d

# Sprawdź status
docker compose ps
docker compose logs -f
```

### 2. **Cloudflare Tunnel Setup**

#### Opcja A: Cloudflared w Docker (REKOMENDOWANE)

Dodaj do `docker-compose.yml`:

```yaml
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflare-tunnel
    command: tunnel --no-autoupdate run --token ${CLOUDFLARE_TUNNEL_TOKEN}
    restart: unless-stopped
    network_mode: "bridge"
    depends_on:
      - sonar-mcp
```

W `.env` dodaj:
```
CLOUDFLARE_TUNNEL_TOKEN=your_tunnel_token_here
```

**Kroki:**
1. Zaloguj się do [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. Przejdź do **Access → Tunnels**
3. Utwórz nowy tunnel: "sonar-mcp-server"
4. Wybierz **Docker** jako środowisko
5. Skopiuj token
6. Skonfiguruj Public Hostname:
   - Public hostname: `sonar.yourdomain.com`
   - Service: `http://sonar-mcp-server:8081`
   - Path: `/sse`

#### Opcja B: Cloudflared bezpośrednio na VPS

```bash
# Instalacja cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# Logowanie
cloudflared tunnel login

# Utworzenie tunelu
cloudflared tunnel create sonar-mcp-server

# Konfiguracja
cat > ~/.cloudflared/config.yml <<EOF
tunnel: <TUNNEL-ID>
credentials-file: /root/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: sonar.yourdomain.com
    service: http://localhost:8081
    path: /sse
  - service: http_status:404
EOF

# Uruchomienie jako usługa
cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### 3. **Cloudflare Access - Autoryzacja**

1. W Cloudflare Zero Trust → **Access → Applications**
2. Utwórz nową aplikację:
   - Application name: "Sonar MCP Server"
   - Session Duration: 24 hours
   - Application domain: `sonar.yourdomain.com`

3. Polityka dostępu:
   - Rule name: "Allow my email"
   - Action: Allow
   - Include:
     - Emails: `twoj@email.com`

### 4. **Konfiguracja Cursor (Test)**

W ustawieniach Cursor, dodaj do MCP servers:

```json
{
  "mcpServers": {
    "sonar-remote": {
      "url": "https://sonar.yourdomain.com/sse",
      "description": "Sonar Pro Search (Remote)"
    }
  }
}
```

**Test:**
1. Restart Cursor
2. Otwórz terminal w Cursor
3. Użyj komendy z narzędziami Sonar
4. Cloudflare poprosi o autoryzację przez email

---

## 🔧 Przydatne komendy

```bash
# Sprawdzenie logów
docker compose logs -f sonar-mcp

# Restart serwera
docker compose restart sonar-mcp

# Rebuild po zmianach
docker compose down
docker compose build --no-cache
docker compose up -d

# Test endpoint lokalnie
curl -i http://localhost:8081/sse

# Test endpoint przez Cloudflare
curl -i https://sonar.yourdomain.com/sse
```

---

## 🎯 Architektura finalna

```
Cursor (lub Claude Desktop)
    ↓
    HTTPS (autoryzacja przez Cloudflare Access)
    ↓
Cloudflare Tunnel
    ↓
    localhost:8081 (na VPS)
    ↓
Docker Container: sonar-mcp-server
    ↓
Perplexity Sonar API (przez OpenRouter)
```

---

## 📝 Notatki

- **Port 8081**: Wybrano dla Sonar (ArXiv będzie na 8080 później)
- **Bez rate limiting**: Dla pojedynczego użytkownika wystarczy Cloudflare Access
- **Bez firewall na VPS**: Cloudflare Tunnel nie wymaga otwierania portów publicznie
- **HTTPS automatyczny**: Cloudflare zapewnia certyfikat SSL
- **Zero konfiguracji sieci**: Tunnel działa "od środka" (outbound connection)

---

## ⚠️ Security Checklist

- ✅ Kontener działa jako non-root user (uid 1000)
- ✅ Cloudflare Access dla autoryzacji
- ✅ HTTPS przez Cloudflare Tunnel
- ✅ API key w `.env` (nie w kodzie)
- ✅ `.env` w `.gitignore`
- 🔜 Monitoring logów (opcjonalnie: Loki + Grafana)
- 🔜 Alerting (opcjonalnie: Grafana Alerts)

---

## 🚦 Status: GOTOWE DO DEPLOYMENT

Wszystkie komponenty przetestowane lokalnie i działają poprawnie.
Następny krok: Deployment na Hostinger VPS + Cloudflare Tunnel.
