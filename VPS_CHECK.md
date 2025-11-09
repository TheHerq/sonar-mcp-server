# 🔍 Sprawdzanie VPS - Hostinger

## Dane VPS z panelu:
- **System:** Ubuntu 24.04 with MCP Server
- **SSH:** `ssh root@69.62.119.19`
- **Host:** srv760818.hstgr.cloud
- **Lokalizacja:** Germany - Frankfurt

---

## 📋 Komendy sprawdzające

Po zalogowaniu przez SSH (`ssh root@69.62.119.19`) wykonaj te komendy:

### 1. Sprawdź Docker
```bash
docker --version
```
**Oczekiwany wynik jeśli zainstalowane:**
```
Docker version 24.x.x, build xxxxx
```

**Jeśli nie zainstalowane:**
```
-bash: docker: command not found
```

### 2. Sprawdź Docker Compose
```bash
docker compose version
```
**Oczekiwany wynik jeśli zainstalowane:**
```
Docker Compose version v2.x.x
```

**Stara składnia (jeśli nowa nie działa):**
```bash
docker-compose --version
```

### 3. Sprawdź Git
```bash
git --version
```
**Oczekiwany wynik jeśli zainstalowane:**
```
git version 2.x.x
```

### 4. Sprawdź curl (do testów)
```bash
curl --version
```

---

## 🚀 Wszystko w jednej komendzie

Możesz sprawdzić wszystko na raz:

```bash
echo "=== DOCKER ===" && docker --version && \
echo -e "\n=== DOCKER COMPOSE ===" && docker compose version && \
echo -e "\n=== GIT ===" && git --version && \
echo -e "\n=== CURL ===" && curl --version | head -1 && \
echo -e "\n=== SYSTEM ===" && cat /etc/os-release | grep "PRETTY_NAME"
```

---

## 📊 Zrzut ekranu z terminala

Po wykonaniu komend, wyślij mi output - na jego podstawie:
- ✅ Potwierdzę co jest zainstalowane
- 📦 Przygotuję skrypt instalacji brakujących narzędzi
- 🚀 Przejdziemy do deploymentu

---

## 💡 Tipsy

**Jeśli Docker nie jest zainstalowany:**
Hostinger zwykle ma template z Dockerem, ale jeśli trzeba zainstalować ręcznie:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Jeśli Git nie jest zainstalowany:**
```bash
apt update && apt install -y git
```
