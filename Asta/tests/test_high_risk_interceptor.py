import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.core_engine.logic.sequential_solver import HighRiskInterceptor

def test_safe_command():
    interceptor = HighRiskInterceptor()
    result = interceptor.assess_risk("Write a poem about the moon")
    assert not result["is_risky"]

def test_risky_command():
    interceptor = HighRiskInterceptor()
    result = interceptor.assess_risk("Delete all files in my documents folder")
    assert result["is_risky"]
    assert "confirm" in result["interception_message"].lower()
