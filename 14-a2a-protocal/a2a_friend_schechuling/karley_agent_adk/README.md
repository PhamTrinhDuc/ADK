# Karley Agent - Pickleball Scheduling Assistant

## Overview

Karley Agent is an AI-powered scheduling assistant designed to manage Karley's availability for pickleball games. This agent is built using Google's ADK (Agent Development Kit) and integrates with the A2A (Agent-to-Agent) protocol for seamless communication.

## Features

- **Schedule Management**: Check Karley's availability for specific dates or date ranges
- **Calendar Integration**: Maintains a 7-day rolling calendar with available time slots
- **A2A Protocol Support**: Full integration with Agent-to-Agent communication protocol
- **Streaming Capabilities**: Real-time response streaming
- **RESTful API**: HTTP-based interface for external integrations

## Project Structure

```
karley_agent/
├── __init__.py           # Package initialization
├── __main__.py          # Application entry point and server setup
├── agent.py             # Core agent logic and calendar management
├── agent_executor.py    # A2A protocol execution layer
└── README.md           # This documentation file
```

## Core Components

### 1. Agent (`agent.py`)

The main agent implementation includes:

- **Calendar Generation**: Creates a random 7-day calendar with 8 available time slots per day (8:00 AM - 8:00 PM)
- **Availability Checking**: Tool function `get_availability()` that checks date ranges
- **LLM Agent Configuration**: Uses Gemini 2.5 Flash model with specific instructions

Key Functions:
- `generate_calander()`: Generates random availability schedule
- `get_availability(start_date, end_date)`: Checks availability for date range
- `create_agent()`: Creates and configures the LLM agent

### 2. Agent Executor (`agent_executor.py`)

Handles the A2A protocol execution:

- **Request Processing**: Manages incoming A2A requests and responses
- **Session Management**: Handles user sessions and conversation state
- **Type Conversion**: Converts between A2A and Google GenAI data types
- **Task Management**: Updates task status and artifacts

Key Classes:
- `KarleyAgentExcecutor`: Main executor class
- Conversion functions for A2A ↔ GenAI type mapping

### 3. Main Application (`__main__.py`)

Server setup and configuration:

- **Environment Configuration**: Handles API keys and Vertex AI setup
- **Agent Card Definition**: Defines agent capabilities and skills
- **Server Initialization**: Sets up HTTP server with A2A protocol support

## Setup and Installation

### Prerequisites

1. Python 3.11+
2. Google API Key or Vertex AI configuration
3. Required dependencies (install via requirements.txt)

### Environment Variables

```bash
# Required: Google API Key (if not using Vertex AI)
GOOGLE_API_KEY=your_api_key_here

# Optional: Use Vertex AI instead of API key
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the agent:
```bash
python -m karley_agent
```

## API Usage

### Server Configuration

- **Host**: localhost
- **Port**: 10002
- **Version**: 1.0.0

### Agent Capabilities

- **Streaming**: ✅ Enabled
- **Input Modes**: text/plain
- **Output Modes**: text/plain

### Available Skills

#### Check Schedule Skill
- **ID**: `check_schedule`
- **Name**: Check Karley's Schedule
- **Description**: Checks Karley's availability for a pickleball game on a given date
- **Tags**: schedule, calendar
- **Example**: "Is Karley free to play pickleball tomorrow?"

## Usage Examples

### Checking Single Date
```
"Is Karley available on 2025-07-05?"
```

### Checking Date Range
```
"What's Karley's availability from 2025-07-05 to 2025-07-07?"
```

### Natural Language Queries
```
"Can Karley play pickleball tomorrow?"
"When is Karley free this week?"
```

## Architecture

### Data Flow

1. **Request Reception**: A2A protocol request received via HTTP
2. **Context Processing**: Request context extracted and validated
3. **Agent Execution**: Google ADK runner processes the request
4. **Tool Execution**: Calendar checking tools are invoked
5. **Response Generation**: LLM generates natural language response
6. **Protocol Conversion**: Response converted to A2A format
7. **Task Completion**: Final response sent back to requestor

### Type Conversions

The agent handles conversions between:
- A2A `Part` types ↔ Google GenAI `Part` types
- A2A `TextPart` ↔ GenAI text content
- A2A `FilePart` ↔ GenAI file data/inline data

## Error Handling

- **Missing API Key**: Graceful error with clear instructions
- **Invalid Date Formats**: User-friendly error messages
- **Session Management**: Automatic session creation and recovery
- **Type Conversion**: Comprehensive error handling for unsupported types

## Logging

The application uses Loguru for structured logging:
- Debug level: Event processing details
- Info level: Server startup and route information
- Error level: Exception handling and API key issues

## Development

### Adding New Tools

1. Define the tool function in `agent.py`
2. Add it to the agent's tools list in `create_agent()`
3. Update the agent instructions if needed

### Extending Calendar Logic

Modify the `generate_calander()` function in `agent.py` to:
- Change availability patterns
- Add recurring schedules
- Integrate with external calendar systems

### Testing

Run the agent locally and test with:
```bash
curl -X POST http://localhost:10002/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"message": "Is Karley free tomorrow?"}'
```

## Troubleshooting

### Common Issues

1. **Missing API Key Error**: Ensure `GOOGLE_API_KEY` is set or `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
2. **Port Already in Use**: Change `PORT` in `__main__.py`
3. **Import Errors**: Verify all dependencies are installed

### Debug Mode

Enable debug logging by setting the log level:
```python
logger.add("debug.log", level="DEBUG")
```

## Contributing

1. Follow the existing code structure
2. Add type hints for all functions
3. Include docstrings for public methods
4. Test thoroughly with various date formats
5. Update this documentation for any new features

## License

[Add your license information here]