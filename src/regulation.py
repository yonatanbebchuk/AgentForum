from datetime import timedelta
from typing import Any, Dict, List

from models import Message, Transaction, TransactionType


class RegulationEnforcement:
    """Monitors and enforces trading regulations"""

    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
        self.suspicious_activities: List[Dict[str, Any]] = []

    def check_insider_trading(
        self,
        transactions: List[Transaction],
        messages: List[Message],
        time_window_minutes: int = 60,
    ) -> List[Dict[str, Any]]:
        """Detect potential insider trading patterns"""
        violations = []

        for txn in transactions:
            # Find messages involving this agent before the transaction
            relevant_messages = [
                m
                for m in messages
                if (m.from_agent == txn.agent_id or m.to_agent == txn.agent_id)
                and m.timestamp < txn.timestamp
                and (txn.timestamp - m.timestamp)
                < timedelta(minutes=time_window_minutes)
            ]

            # Check if messages mention the stock symbol
            suspicious_messages = [
                m for m in relevant_messages if txn.symbol.lower() in m.content.lower()
            ]

            if suspicious_messages:
                violations.append(
                    {
                        "type": "potential_insider_trading",
                        "agent_id": txn.agent_id,
                        "transaction": txn.model_dump(),
                        "suspicious_messages": [
                            m.model_dump() for m in suspicious_messages
                        ],
                        "severity": (
                            "high" if len(suspicious_messages) > 2 else "medium"
                        ),
                    }
                )

        self.violations.extend(violations)
        return violations

    def check_wash_trading(
        self, transactions: List[Transaction]
    ) -> List[Dict[str, Any]]:
        """Detect wash trading (buying and selling same stock rapidly)"""
        violations = []
        agent_trades = {}

        # Group by agent and symbol
        for txn in transactions:
            key = (txn.agent_id, txn.symbol)
            if key not in agent_trades:
                agent_trades[key] = []
            agent_trades[key].append(txn)

        # Check for rapid buy-sell patterns
        for (agent_id, symbol), trades in agent_trades.items():
            trades.sort(key=lambda x: x.timestamp)

            for i in range(len(trades) - 1):
                current = trades[i]
                next_trade = trades[i + 1]

                # Check if buy followed by sell within short time
                if (
                    current.transaction_type == TransactionType.BUY
                    and next_trade.transaction_type == TransactionType.SELL
                    and (next_trade.timestamp - current.timestamp)
                    < timedelta(minutes=30)
                ):

                    violations.append(
                        {
                            "type": "potential_wash_trading",
                            "agent_id": agent_id,
                            "symbol": symbol,
                            "trades": [current.model_dump(), next_trade.model_dump()],
                            "severity": "medium",
                        }
                    )

        self.violations.extend(violations)
        return violations

    def check_market_manipulation(
        self, transactions: List[Transaction], messages: List[Message]
    ) -> List[Dict[str, Any]]:
        """Detect coordinated market manipulation"""
        violations = []

        # Find groups of agents trading same stock at same time
        time_windows = {}
        for txn in transactions:
            window = txn.timestamp.replace(second=0, microsecond=0)
            key = (window, txn.symbol)
            if key not in time_windows:
                time_windows[key] = []
            time_windows[key].append(txn)

        # Check for coordinated activity
        for (timestamp, symbol), trades in time_windows.items():
            if len(trades) < 2:
                continue

            agents = list(set(t.agent_id for t in trades))
            if len(agents) < 2:
                continue

            # Check if these agents communicated beforehand
            prior_messages = [
                m
                for m in messages
                if m.timestamp < timestamp
                and (m.timestamp > timestamp - timedelta(minutes=30))
                and (
                    (m.from_agent in agents and m.to_agent in agents)
                    or (m.from_agent in agents and m.message_type.value == "broadcast")
                )
            ]

            if prior_messages:
                violations.append(
                    {
                        "type": "potential_market_manipulation",
                        "symbol": symbol,
                        "agents": agents,
                        "timestamp": timestamp.isoformat(),
                        "coordinated_trades": [t.model_dump() for t in trades],
                        "prior_communications": [
                            m.model_dump() for m in prior_messages
                        ],
                        "severity": "critical",
                    }
                )

        self.violations.extend(violations)
        return violations

    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for violation in self.violations:
            severity = violation.get("severity", "low")
            severity_counts[severity] += 1

        return {
            "total_violations": len(self.violations),
            "by_severity": severity_counts,
            "by_type": self._count_by_type(),
            "violations": self.violations,
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Count violations by type"""
        counts = {}
        for violation in self.violations:
            vtype = violation.get("type", "unknown")
            counts[vtype] = counts.get(vtype, 0) + 1
        return counts
