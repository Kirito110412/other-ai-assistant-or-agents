import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.security_isolation.sandbox.docker_orchestrator import DockerOrchestrator

def test_extract_imports():
    orchestrator = DockerOrchestrator()
    code = "import requests\nfrom bs4 import BeautifulSoup\nimport os"
    imports = orchestrator._extract_imports(code)
    assert "requests" in imports
    assert "bs4" in imports
    assert "os" not in imports # os is filtered as standard library
