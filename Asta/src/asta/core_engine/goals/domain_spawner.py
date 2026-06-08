import logging
import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("DomainSpawner")

class AgentRole(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    title: str = Field(description="The formal title of this agent (e.g., 'CTO', 'Senior Researcher')")
    goal: str = Field(description="The primary objective this agent is responsible for.")
    backstory: str = Field(description="Context to give the LLM specific domain expertise.")
    budget_usd: float = Field(default=5.0, description="Max allowed API spend for this agent.")
    current_spend: float = Field(default=0.0)
    reports_to: Optional[str] = Field(default="CEO", description="ID of the managing agent.")
    sub_agents: List[str] = Field(default_factory=list)

class DomainSpawner:
    """
    Fleet Management and Org-Chart Architect.
    Bridges the gap with Paperclip/CrewAI by allowing Asta to spawn
    a highly structured hierarchy of agents with strict budgets and roles.
    """
    def __init__(self):
        # Asta itself is always the default 'CEO' orchestrating the fleet
        self.org_chart: Dict[str, AgentRole] = {
            "CEO": AgentRole(id="CEO", title="CEO (Asta Core)", goal="Manage the company and finalize deliverables", backstory="I am Asta, the orchestrator.", budget_usd=50.0)
        }

    def spawn_agent(self, title: str, goal: str, backstory: str, budget_usd: float = 2.0, reports_to: str = "CEO") -> AgentRole:
        """
        Dynamically spawns a new sub-agent and slots it into the Org-Chart.
        """
        if reports_to not in self.org_chart:
            logger.error(f"Cannot assign manager: {reports_to} does not exist in Org Chart.")
            reports_to = "CEO"

        new_agent = AgentRole(
            title=title,
            goal=goal,
            backstory=backstory,
            budget_usd=budget_usd,
            reports_to=reports_to
        )

        self.org_chart[new_agent.id] = new_agent
        self.org_chart[reports_to].sub_agents.append(new_agent.id)

        logger.info(f"Spawned new Agent: [{new_agent.title}] reporting to [{self.org_chart[reports_to].title}]")
        return new_agent

    def record_spend(self, agent_id: str, cost: float) -> bool:
        """
        Tracks LLM API usage. Returns False if budget is exceeded.
        """
        if agent_id not in self.org_chart:
            return False

        agent = self.org_chart[agent_id]
        if agent.current_spend + cost > agent.budget_usd:
            logger.warning(f"Agent {agent.title} [{agent_id}] exceeded budget! (${agent.current_spend + cost} / ${agent.budget_usd})")
            return False

        agent.current_spend += cost
        return True

    def get_org_chart(self) -> Dict:
        """
        Exports the entire fleet hierarchy for the Web Dashboard UI (Paperclip parity).
        """
        return {agent_id: agent.model_dump() for agent_id, agent in self.org_chart.items()}

# Global Singleton for the active company structure
fleet_manager = DomainSpawner()
