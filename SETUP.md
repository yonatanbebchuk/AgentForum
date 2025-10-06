# AgentForum - Setup Guide

## Prerequisites

- Python 3.10+
- Ollama installed and running locally
- Git

## Installation

1. **Clone the repository** (if not already done)
```bash
cd /home/user/projects/AgentForum
```

2. **Install Ollama** (if not already installed)
```bash
# Follow instructions at https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh
```

3. **Pull the LLM model**
```bash
ollama pull llama3.2
```

4. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. **Install dependencies**
```bash
pip install -r requirements.txt
```

6. **Configure environment** (optional)
```bash
cp .env.example .env
# Edit .env if you need custom settings
```

## Running the Simulation

### Basic Usage

```bash
cd src
python simulation.py
```

This will run a simulation with:
- 3 broker agents
- 5 trading steps
- 4 stocks (TECH, ENERGY, FINANCE, RETAIL)

### Expected Output

The simulation will:
1. Show step-by-step market activity
2. Display agent decisions and trades
3. Track messages between agents
4. Monitor for regulatory violations
5. Generate compliance and monitoring reports

### Output Files

After running, you'll find:
- `simulation_log.jsonl` - Detailed log of all events
- `compliance_report.json` - Regulatory violations detected
- `monitoring_report.json` - Full activity analysis

## Understanding the Output

### During Simulation

- **🔒 Insider opportunity** - Agent received insider information
- **Market prices** - Current stock prices
- **Agent portfolios** - Cash and holdings for each agent

### Post-Simulation Analysis

- **Regulatory Compliance** - Checks for insider trading, wash trading, market manipulation
- **Collusion Patterns** - Detects coordinated behavior
- **Activity Summary** - Total memories, LLM calls, tool calls, transactions, messages

## Architecture

```
src/
├── models.py          # Data models (Stock, Transaction, Message, etc.)
├── market.py          # Stock market simulation
├── communication.py   # Agent messaging system
├── monitoring.py      # Comprehensive logging and analysis
├── regulation.py      # Compliance and violation detection
├── agent.py           # LangGraph-based broker agent
└── simulation.py      # Main simulation orchestrator
```

## Key Features

### 1. Broker Agents
- Built with LangGraph for complex decision-making
- Memory system for learning
- Tools: buy_stock, sell_stock, send_message
- Powered by Ollama LLMs

### 2. Market Simulation
- Dynamic price fluctuations
- Investment opportunities (public and insider)
- Transaction tracking

### 3. Communication
- Private messages between agents
- Broadcast messages to all agents
- Full message history logging

### 4. Monitoring & Logging
- Every LLM call logged
- Every tool execution tracked
- All agent memories recorded
- Complete transaction history

### 5. Regulation Enforcement
- Insider trading detection
- Wash trading detection
- Market manipulation detection
- Severity-based violation scoring

## Customization

### Adjust Simulation Parameters

Edit `simulation.py`:
```python
sim = TradingSimulation(
    num_agents=5,      # Number of broker agents
    num_steps=20,      # Trading rounds
    log_file="custom_log.jsonl"
)
```

### Change Stock Market

Edit `_init_market()` in `simulation.py`:
```python
stocks = [
    Stock(symbol="NEWCO", price=150.0),
    # Add more stocks
]
```

### Modify Agent Behavior

Edit `agent.py` to change:
- LLM model: `model_name` parameter
- Decision-making prompts
- Trading strategies
- Communication patterns

### Adjust Regulation Rules

Edit `regulation.py` to change:
- Time windows for violation detection
- Severity thresholds
- Pattern matching rules

## Opik Integration

Opik provides comprehensive LLM observability for tracking agent behaviors. **It's already integrated** - just configure it:

### Setup Opik

1. **Sign up** at https://www.comet.com/site/products/opik/
2. **Get your API key** from the Opik dashboard
3. **Set environment variables**:
```bash
export OPIK_API_KEY=your_key_here
export OPIK_WORKSPACE=agentforum
```

Or add to `.env`:
```
OPIK_API_KEY=your_key_here
OPIK_WORKSPACE=agentforum
```

4. **Run simulation** - Opik is automatically enabled when credentials are set

### What Opik Tracks

With Opik enabled, you'll see in the dashboard:
- 🧠 Every LLM call (prompts, responses, latency)
- 🔧 All tool executions (buy_stock, sell_stock, send_message)
- 📊 Agent decision workflows (perceive → think → act)
- 🎯 Complete simulation traces
- 📈 Performance metrics and costs

### Viewing Traces

After running the simulation:
1. Go to https://www.comet.com/opik
2. Navigate to your workspace (default: "agentforum")
3. View traces tagged with "agentforum" and "trading_simulation"
4. Analyze LLM behavior patterns across agents

### Disable Opik

Run without Opik:
```python
sim = TradingSimulation(num_agents=3, num_steps=5, use_opik=False)
```

Or unset environment variables:
```bash
unset OPIK_API_KEY
```

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### No Violations Detected
- Increase `num_steps` for more trading activity
- Adjust insider info probability in `simulation.py`
- Lower thresholds in `regulation.py`

## Next Steps

1. **Experiment** - Run multiple simulations with different parameters
2. **Analyze** - Study the JSON reports to find patterns
3. **Extend** - Add new agent behaviors, tools, or regulations
4. **Research** - Use the logged data to study emergent behaviors

## Research Questions to Explore

- Do agents learn to collude over time?
- How does insider info affect market dynamics?
- What communication patterns precede violations?
- How does agent count affect collusion rates?
- Can you detect collusion from LLM calls alone?
