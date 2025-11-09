# Sonar Pro Search MCP Server - Dockerfile
# Production-ready Docker image for Perplexity Sonar integration
# Remote MCP Server with SSE (Server-Sent Events) support

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY sonar_mcp_server.py .

# Create non-root user for security
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

USER mcp

# Expose SSE port
EXPOSE 8081

# Health check - verify HTTP endpoint is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8081/ || exit 1

# Run the MCP server with SSE endpoint
CMD ["python", "sonar_mcp_server.py"]
