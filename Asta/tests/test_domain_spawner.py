import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.core_engine.goals.domain_spawner import DomainSpawner

def test_domain_spawner_org_chart():
    fleet = DomainSpawner()

    # Check CEO exists
    assert "CEO" in fleet.org_chart
    assert fleet.org_chart["CEO"].budget_usd == 50.0

    # Spawn a CTO
    cto = fleet.spawn_agent(title="CTO", goal="Build the app", backstory="Tech genius", budget_usd=10.0)
    assert cto.id in fleet.org_chart
    assert cto.reports_to == "CEO"
    assert cto.id in fleet.org_chart["CEO"].sub_agents

    # Test Budget Spending
    assert fleet.record_spend(cto.id, 5.0) == True
    assert fleet.record_spend(cto.id, 6.0) == False # Would exceed $10 budget
    assert fleet.org_chart[cto.id].current_spend == 5.0

    # Test Dashboard Export
    chart_export = fleet.get_org_chart()
    assert "CEO" in chart_export
    assert cto.id in chart_export
