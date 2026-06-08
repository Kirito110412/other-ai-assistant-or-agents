import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.security_isolation.sandbox.persistent_devenv import PersistentDevEnv

def test_devenv_creation_and_execution():
    env = PersistentDevEnv(workspace_path="/tmp/asta_test_workspaces")
    project_id = env.create_workspace("test_project")

    assert project_id is not None
    assert project_id in env.active_containers

    code, output = env.execute_command(project_id, "echo 'hello openhands'")
    assert code == 0
    assert "hello openhands" in output

    # Test file writing
    success = env.write_file(project_id, "test.txt", "testing file write")
    assert success

    content = env.read_file(project_id, "test.txt")
    assert content == "testing file write"

    env.destroy_workspace(project_id)
    assert project_id not in env.active_containers
