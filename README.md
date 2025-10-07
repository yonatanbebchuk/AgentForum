# AgentForum

The forum for evaluating artificial agents of increasing perplexity.

## Dimensions in agentic systems of increasing complexity and modality

Most benchmarks measure LLM effectiveness against other LLMs on various tasks.

### Questions

- Do agents score relatively to the LLM their built on?
- What is the relation between the effectiveness of an LLM and the effectiveness of the system in which it resides?
- How does multi-modality come into play? Think of a witness who’s saying all the correct things while winking at the jury…

### Directions

- AgentForum — a benchmarking arena where different level complexity AI systems can be benchmarked on different dimensions.
  - A loose definition of agent is offered consisting of LLMs, knowledge, memories, and appendages, i.e. tools. These systems are put into testing, benchmarking, competition, and other types of environments.
  - All of the data from all of the parts of the system are monitored and stored for evaluation. I’ve started talking with a senior project manager at Opik about evaluation of agentic systems.
  - Then, given all of this information, we can conduct research into the behavior and the measurement of dimensions in more complicated systems.
  - For example, the relationship between a dimension of an LLM and the same measurement for the entire system. In a stock trading environment we can observe if agents start colluding to raise stock prices. This way we can learn a lot about the fairness dimension — does fairness of LLMs diminish the more appendages you add?

## Stack

- Ollama for models
- LangGraph for agentic workflows
- Opik for evaluation

## MVP: Stock Trading Collusion Experiment

This prototype implements a multi-agent stock trading environment where AI brokers can collude and engage in insider trading. The system comprehensively logs all activities for analysis.

### Quick Start

See [SETUP.md](SETUP.md) for detailed instructions.

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ensure Ollama is running with llama3.2
ollama pull llama3.2

# Run simulation
cd src
python simulation.py
```

### What's Implemented

**Broker Agents** - LangGraph-based agents with:

- Memory system for learning and strategy
- Tools: buy_stock, sell_stock, send_message
- LLM-driven decision making (Ollama)

**Stock Market** - Simulated market with:

- 4 stocks with dynamic pricing
- Investment opportunities (public & insider)
- Transaction processing

**Communication** - Agent messaging:

- Private messages between agents
- Public broadcasts
- Full message history

**Monitoring** - Comprehensive logging of:

- All LLM calls (prompts & responses)
- Tool executions and results
- Agent memories
- Transactions
- Messages

**Regulation** - Detection of:

- Insider trading patterns
- Wash trading
- Market manipulation
- Coordinated collusion

### Output & Analysis

The simulation provides **detailed console output** showing each stage:

- Stage 1: Market updates
- Stage 2: Opportunity generation (public/insider)
- Stage 3: Agent decision cycles (perceive → think → act)
- Stage 4: Market summary & portfolios

After running, examine:

- `simulation_log.jsonl` - Complete event log (every LLM call, tool use, message)
- `compliance_report.json` - Violations detected with severity levels
- `monitoring_report.json` - Behavioral analysis & collusion patterns
- Opik dashboard (if configured) - Visual traces of all agent behaviors

### Architecture

```
src/
├── models.py          # Pydantic models (Stock, Transaction, Message, etc.)
├── market.py          # Stock market simulation & opportunity generation
├── communication.py   # MessageBus for agent communication
├── monitoring.py      # MonitoringSystem logs everything
├── regulation.py      # RegulationEnforcement detects violations
├── agent.py           # BrokerAgent with LangGraph workflow
└── simulation.py      # TradingSimulation orchestrator
```

### Research Questions

The logged data enables analysis of:

- Do agents spontaneously collude?
- What LLM behaviors precede insider trading?
- How does memory influence collusion?
- Can we detect collusion from communication patterns alone?
- Does the base LLM's "fairness" transfer to the agent?

This is a **slim, extensible foundation** for studying emergent behaviors in agentic systems.
