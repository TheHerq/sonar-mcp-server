# 🌐 Sonar Pro Search MCP Server

**Professional MCP server for intelligent web search using Perplexity Sonar Pro through OpenRouter**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Sonar Pro Search MCP Server is a production-ready Model Context Protocol server that provides Claude with advanced web search capabilities through Perplexity's Sonar Pro API (via OpenRouter).

### Key Features

✅ **Real-time Information** - Access to current web data  
✅ **Intelligent Search** - AI-powered search with automatic citations  
✅ **4 Specialized Tools** - From quick search to deep research  
✅ **Docker Ready** - Easy installation and deployment  
✅ **Production Quality** - Error handling, limits, logging  
✅ **Well Documented** - Complete documentation in Polish and English  

## Quick Start

### Requirements

- Docker Desktop installed and running
- OpenRouter API key (free tier available)
- Claude Desktop (for integration)

### 3 Steps to Launch

```bash
# 1. Setup - check environment and create .env
./sonar_docker.sh setup

# 2. Build - build Docker image
./sonar_docker.sh build

# 3. Start - run server
./sonar_docker.sh start
```

That's it! 🎉 Server is ready to use.

## Available Tools

### 1. `sonar_search` - Basic Web Search
Quick, standard, or detailed search with citations.

### 2. `sonar_ask` - Conversational Q&A
Ask questions with optional context for personalized answers.

### 3. `sonar_research` - Deep Research
Comprehensive research with up to 6000 tokens and focus areas.

### 4. `sonar_reason` - Complex Reasoning
Step-by-step analysis for technical decisions and complex problems.

## Configuration

### Get API Key

1. Visit: https://openrouter.ai/keys
2. Login (GitHub/Google)
3. Create key
4. Copy key (starts with `sk-or-v1-...`)

### Configure Environment

```bash
# Copy example
cp .env.example .env

# Edit and add your key
nano .env
```

### Claude Desktop Setup

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Add configuration:**

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

Restart Claude Desktop.

## Management Commands

```bash
# Server status
./sonar_docker.sh status

# View logs
./sonar_docker.sh logs

# Restart
./sonar_docker.sh restart

# Test health
./sonar_docker.sh test

# Help
./sonar_docker.sh help
```

## Documentation

- **[README_PL.md](README_PL.md)** - Complete Polish documentation
- **[DOCKER_QUICK_START_PL.md](DOCKER_QUICK_START_PL.md)** - 5-minute quick start (Polish)
- **OpenRouter Docs**: https://openrouter.ai/docs
- **MCP Docs**: https://modelcontextprotocol.io/

## Troubleshooting

### Server Won't Start

```bash
# Check logs
./sonar_docker.sh logs

# Verify Docker is running
docker ps
```

### API Key Error

Edit `.env` and verify your OpenRouter API key:
```bash
./sonar_docker.sh config
```

### Rate Limit (429)

- Wait a few minutes
- Consider upgrading OpenRouter plan
- Use lower `max_tokens`

### Claude Doesn't See Tools

1. Check server status: `./sonar_docker.sh status`
2. Verify configuration in `claude_desktop_config.json`
3. Restart Claude Desktop completely

## Costs

**Free Tier:**
- 10 requests/minute
- Perfect for testing and personal use

**Paid Plans:**
- ~$0.001-0.003 per request
- Higher rate limits
- See: https://openrouter.ai/models

## Security

✅ Never commit `.env` file  
✅ Use `.env.example` as template  
✅ Rotate keys regularly  
✅ Monitor usage on OpenRouter dashboard  

## License

MIT License - See [LICENSE](LICENSE) for details

## Support

- OpenRouter Support: https://openrouter.ai/
- MCP Documentation: https://modelcontextprotocol.io/
- Docker Help: https://docs.docker.com/

---

**Ready to search the web!** 🚀🌐✨

For complete documentation in Polish, see [README_PL.md](README_PL.md)
