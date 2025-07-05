# Makefile for running A2A Friend Scheduling Agents

.PHONY: all run-karley run-nate run-kaitlyn run-all stop install clean help

# Default target
all: help

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run individual agents
run-karley:
	@echo "Starting Karley Agent on port 10002..."
	cd karley_agent_adk && python -m __main__

run-nate:
	@echo "Starting Nate Agent on port 10003..."
	cd nate_agent_crewai && python -m __main__

run-kaitlyn:
	@echo "Starting Kaitlyn Agent on port 10004..."
	cd kaitlyn_agent_langgraph && python -m __main__

# Run all agents in background (requires GNU parallel or you can use & and wait)
run-all:
	@echo "Starting all agents..."
	@echo "Karley Agent will run on http://localhost:10002"
	@echo "Nate Agent will run on http://localhost:10003"
	@echo "Kaitlyn Agent will run on http://localhost:10004"
	@echo ""
	@echo "Starting agents in parallel..."
	@(cd karley_agent_adk && python -m __main__) & \
	(cd nate_agent_crewai && python -m __main__) & \
	(cd kaitlyn_agent_langgraph && python -m __main__) & \
	wait

# Stop all running agents (kills python processes on the specific ports)
stop:
	@echo "Stopping all agents..."
	@-pkill -f "python -m __main__" 2>/dev/null || true
	@-lsof -ti:10002 | xargs kill -9 2>/dev/null || true
	@-lsof -ti:10003 | xargs kill -9 2>/dev/null || true
	@-lsof -ti:10004 | xargs kill -9 2>/dev/null || true
	@echo "All agents stopped."

# Check which ports are in use
check-ports:
	@echo "Checking ports 10002, 10003, 10004..."
	@lsof -i :10002 || echo "Port 10002 is free"
	@lsof -i :10003 || echo "Port 10003 is free"
	@lsof -i :10004 || echo "Port 10004 is free"

# Clean up any temporary files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete."

# Development helpers
dev-karley:
	@echo "Starting Karley Agent in development mode..."
	cd karley_agent_adk && python __main__.py --reload

dev-nate:
	@echo "Starting Nate Agent in development mode..."
	cd nate_agent_crewai && python __main__.py --reload

dev-kaitlyn:
	@echo "Starting Kaitlyn Agent in development mode..."
	cd kaitlyn_agent_langgraph && python __main__.py --reload

# Test if agents are running
test:
	@echo "Testing if agents are responding..."
	@curl -s http://localhost:10002/health > /dev/null && echo "✓ Karley Agent (10002) is running" || echo "✗ Karley Agent (10002) is not responding"
	@curl -s http://localhost:10003/health > /dev/null && echo "✓ Nate Agent (10003) is running" || echo "✗ Nate Agent (10003) is not responding"
	@curl -s http://localhost:10004/health > /dev/null && echo "✓ Kaitlyn Agent (10004) is running" || echo "✗ Kaitlyn Agent (10004) is not responding"

# Show help
help:
	@echo "A2A Friend Scheduling Agents - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make run-karley   - Run Karley Agent (port 10002)"
	@echo "  make run-nate     - Run Nate Agent (port 10003)"
	@echo "  make run-kaitlyn  - Run Kaitlyn Agent (port 10004)"
	@echo "  make run-all      - Run all agents in parallel"
	@echo "  make stop         - Stop all running agents"
	@echo "  make check-ports  - Check which ports are in use"
	@echo "  make test         - Test if agents are responding"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Development commands:"
	@echo "  make dev-karley   - Run Karley Agent with reload"
	@echo "  make dev-nate     - Run Nate Agent with reload"
	@echo "  make dev-kaitlyn  - Run Kaitlyn Agent with reload"
	@echo ""
	@echo "Before running, make sure you have:"
	@echo "  - GOOGLE_API_KEY environment variable set"
	@echo "  - Required dependencies installed (make install)"
