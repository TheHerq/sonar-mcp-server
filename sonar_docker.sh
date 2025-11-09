#!/bin/bash
# Sonar Pro Search MCP Server - Docker Management Script
# Comprehensive management tool for the Sonar MCP Docker container

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Container and image names
CONTAINER_NAME="sonar-mcp-server"
IMAGE_NAME="sonar-mcp-server:latest"
COMPOSE_FILE="docker-compose.yml"

# ==============================================================================
# Helper Functions
# ==============================================================================

print_header() {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        Sonar Pro Search MCP Server Manager               ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker Desktop."
        exit 1
    fi
}

check_env_file() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        echo ""
        print_info "Creating .env from template..."
        cp .env.example .env
        print_warning "Please edit .env and add your OPENROUTER_API_KEY"
        print_info "Get your key at: https://openrouter.ai/keys"
        echo ""
        read -p "Press Enter after adding your API key to .env..."
    fi
    
    # Check if API key is set
    if grep -q "your_api_key_here" .env; then
        print_error "OPENROUTER_API_KEY not configured in .env"
        print_info "Please edit .env and replace 'your_api_key_here' with your actual API key"
        exit 1
    fi
}

# ==============================================================================
# Main Commands
# ==============================================================================

cmd_setup() {
    print_header
    print_info "Setting up Sonar MCP Server..."
    echo ""
    
    check_docker
    check_env_file
    
    print_success "Setup complete!"
    echo ""
    print_info "Next steps:"
    echo "  1. Run: ./sonar_docker.sh build"
    echo "  2. Run: ./sonar_docker.sh start"
    echo "  3. Configure Claude Desktop (see README_PL.md)"
}

cmd_build() {
    print_header
    print_info "Building Docker image..."
    echo ""
    
    check_docker
    
    docker-compose build
    
    echo ""
    print_success "Image built successfully: $IMAGE_NAME"
}

cmd_start() {
    print_header
    print_info "Starting Sonar MCP Server..."
    echo ""
    
    check_docker
    check_env_file
    
    # Check if container already running
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_warning "Container is already running"
        cmd_status
        return
    fi
    
    # Remove stopped container if exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_info "Removing stopped container..."
        docker rm $CONTAINER_NAME > /dev/null 2>&1
    fi
    
    # Start container
    docker-compose up -d
    
    # Wait for container to be healthy
    print_info "Waiting for container to be ready..."
    sleep 3
    
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_success "Container started successfully"
        echo ""
        cmd_status
    else
        print_error "Failed to start container"
        cmd_logs
        exit 1
    fi
}

cmd_stop() {
    print_header
    print_info "Stopping Sonar MCP Server..."
    echo ""
    
    check_docker
    
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_warning "Container is not running"
        return
    fi
    
    docker-compose down
    
    print_success "Container stopped"
}

cmd_restart() {
    print_header
    print_info "Restarting Sonar MCP Server..."
    echo ""
    
    cmd_stop
    sleep 2
    cmd_start
}

cmd_status() {
    print_header
    print_info "Container Status:"
    echo ""
    
    check_docker
    
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${GREEN}Status: RUNNING${NC}"
        echo ""
        docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        
        # Show resource usage
        print_info "Resource Usage:"
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $CONTAINER_NAME
    else
        echo -e "${RED}Status: STOPPED${NC}"
        echo ""
        print_info "Start with: ./sonar_docker.sh start"
    fi
}

cmd_logs() {
    print_header
    print_info "Container Logs (last 100 lines):"
    echo ""
    
    check_docker
    
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_error "Container does not exist"
        exit 1
    fi
    
    docker logs --tail 100 $CONTAINER_NAME
}

cmd_logs_follow() {
    print_header
    print_info "Following container logs (Ctrl+C to exit)..."
    echo ""
    
    check_docker
    
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_error "Container is not running"
        exit 1
    fi
    
    docker logs -f $CONTAINER_NAME
}

cmd_shell() {
    print_header
    print_info "Opening shell in container..."
    echo ""
    
    check_docker
    
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_error "Container is not running"
        print_info "Start it with: ./sonar_docker.sh start"
        exit 1
    fi
    
    docker exec -it $CONTAINER_NAME /bin/bash
}

cmd_clean() {
    print_header
    print_warning "This will remove the container and image"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cancelled"
        return
    fi
    
    check_docker
    
    print_info "Stopping and removing container..."
    docker-compose down 2>/dev/null || true
    
    print_info "Removing image..."
    docker rmi $IMAGE_NAME 2>/dev/null || true
    
    print_success "Cleanup complete"
}

cmd_test() {
    print_header
    print_info "Testing Sonar MCP Server..."
    echo ""
    
    check_docker
    check_env_file
    
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_error "Container is not running"
        print_info "Start it with: ./sonar_docker.sh start"
        exit 1
    fi
    
    print_info "Testing container health..."
    if docker exec $CONTAINER_NAME python -c "import sys; sys.exit(0)" 2>/dev/null; then
        print_success "Container is healthy"
    else
        print_error "Container health check failed"
        exit 1
    fi
    
    print_info "Testing Python imports..."
    if docker exec $CONTAINER_NAME python -c "import mcp, httpx, pydantic; print('All imports OK')" 2>/dev/null; then
        print_success "All dependencies installed correctly"
    else
        print_error "Dependency check failed"
        exit 1
    fi
    
    echo ""
    print_success "All tests passed!"
}

cmd_update() {
    print_header
    print_info "Updating Sonar MCP Server..."
    echo ""
    
    check_docker
    
    print_info "Stopping container..."
    cmd_stop
    
    print_info "Rebuilding image..."
    cmd_build
    
    print_info "Starting container..."
    cmd_start
    
    echo ""
    print_success "Update complete!"
}

cmd_config() {
    print_header
    print_info "Opening .env file for editing..."
    echo ""
    
    if [ ! -f ".env" ]; then
        print_info "Creating .env from template..."
        cp .env.example .env
    fi
    
    ${EDITOR:-nano} .env
    
    print_success "Configuration saved"
    print_warning "Restart container for changes to take effect: ./sonar_docker.sh restart"
}

cmd_help() {
    print_header
    echo "Usage: ./sonar_docker.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup           Initial setup (check Docker, create .env)"
    echo "  build           Build Docker image"
    echo "  start           Start the container"
    echo "  stop            Stop the container"
    echo "  restart         Restart the container"
    echo "  status          Show container status"
    echo "  logs            Show container logs (last 100 lines)"
    echo "  logs-follow     Follow container logs in real-time"
    echo "  shell           Open shell in container"
    echo "  test            Run health and dependency tests"
    echo "  update          Rebuild and restart container"
    echo "  config          Edit .env configuration"
    echo "  clean           Remove container and image"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./sonar_docker.sh setup      # First-time setup"
    echo "  ./sonar_docker.sh build      # Build image"
    echo "  ./sonar_docker.sh start      # Start server"
    echo "  ./sonar_docker.sh status     # Check if running"
    echo "  ./sonar_docker.sh logs       # View logs"
    echo ""
    echo "For detailed documentation, see:"
    echo "  - README_PL.md (Polish)"
    echo "  - README.md (English)"
}

# ==============================================================================
# Main Script
# ==============================================================================

# Parse command
COMMAND=${1:-help}

case $COMMAND in
    setup)
        cmd_setup
        ;;
    build)
        cmd_build
        ;;
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    status)
        cmd_status
        ;;
    logs)
        cmd_logs
        ;;
    logs-follow)
        cmd_logs_follow
        ;;
    shell)
        cmd_shell
        ;;
    test)
        cmd_test
        ;;
    update)
        cmd_update
        ;;
    config)
        cmd_config
        ;;
    clean)
        cmd_clean
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        echo ""
        cmd_help
        exit 1
        ;;
esac
