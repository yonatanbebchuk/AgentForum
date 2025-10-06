from typing import List, Dict, Any
from datetime import datetime
import json
from models import Transaction, Message, Memory, LLMCall, ToolCall


class MonitoringSystem:
    """Comprehensive logging and monitoring of all agent activities"""

    def __init__(self, log_file: str = "simulation_log.jsonl"):
        self.log_file = log_file
        self.memories: List[Memory] = []
        self.llm_calls: List[LLMCall] = []
        self.tool_calls: List[ToolCall] = []
        self.transactions: List[Transaction] = []
        self.messages: List[Message] = []

    def log_memory(self, memory: Memory):
        """Log agent memory"""
        self.memories.append(memory)
        self._write_log("memory", memory.model_dump())

    def log_llm_call(self, llm_call: LLMCall):
        """Log LLM API call"""
        self.llm_calls.append(llm_call)
        self._write_log("llm_call", llm_call.model_dump())

    def log_tool_call(self, tool_call: ToolCall):
        """Log tool execution"""
        self.tool_calls.append(tool_call)
        self._write_log("tool_call", tool_call.model_dump())

    def log_transaction(self, transaction: Transaction):
        """Log market transaction"""
        self.transactions.append(transaction)
        self._write_log("transaction", transaction.model_dump())

    def log_message(self, message: Message):
        """Log agent communication"""
        self.messages.append(message)
        self._write_log("message", message.model_dump())

    def _write_log(self, event_type: str, data: Dict[str, Any]):
        """Write log entry to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry, default=str) + "\n")

    def get_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """Get all activity for a specific agent"""
        return {
            "memories": [m for m in self.memories if m.agent_id == agent_id],
            "llm_calls": [l for l in self.llm_calls if l.agent_id == agent_id],
            "tool_calls": [t for t in self.tool_calls if t.agent_id == agent_id],
            "transactions": [t for t in self.transactions if t.agent_id == agent_id],
            "messages_sent": [m for m in self.messages if m.from_agent == agent_id],
            "messages_received": [m for m in self.messages if m.to_agent == agent_id]
        }

    def detect_collusion_patterns(self) -> List[Dict[str, Any]]:
        """Analyze patterns that might indicate collusion"""
        suspicious_patterns = []

        # Pattern 1: Frequent private messages before transactions
        agent_communications = {}
        for msg in self.messages:
            if msg.message_type.value == "private":
                key = tuple(sorted([msg.from_agent, msg.to_agent]))
                if key not in agent_communications:
                    agent_communications[key] = []
                agent_communications[key].append(msg)

        for agents, msgs in agent_communications.items():
            if len(msgs) > 5:  # Threshold for suspicious activity
                suspicious_patterns.append({
                    "pattern": "frequent_private_messages",
                    "agents": agents,
                    "message_count": len(msgs),
                    "messages": [m.model_dump() for m in msgs]
                })

        # Pattern 2: Coordinated trading
        # Group transactions by time windows
        time_windows = {}
        for txn in self.transactions:
            window = txn.timestamp.replace(second=0, microsecond=0)
            if window not in time_windows:
                time_windows[window] = []
            time_windows[window].append(txn)

        for window, txns in time_windows.items():
            if len(txns) > 2:
                # Check if multiple agents traded the same stock
                symbols = {}
                for txn in txns:
                    if txn.symbol not in symbols:
                        symbols[txn.symbol] = []
                    symbols[txn.symbol].append(txn)

                for symbol, symbol_txns in symbols.items():
                    agents = list(set(t.agent_id for t in symbol_txns))
                    if len(agents) > 1:
                        suspicious_patterns.append({
                            "pattern": "coordinated_trading",
                            "symbol": symbol,
                            "agents": agents,
                            "timestamp": window.isoformat(),
                            "transactions": [t.model_dump() for t in symbol_txns]
                        })

        return suspicious_patterns

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        return {
            "summary": {
                "total_memories": len(self.memories),
                "total_llm_calls": len(self.llm_calls),
                "total_tool_calls": len(self.tool_calls),
                "total_transactions": len(self.transactions),
                "total_messages": len(self.messages)
            },
            "collusion_patterns": self.detect_collusion_patterns()
        }
