import subprocess
import os

def run_cli_command(command):
    """Helper to run CLI command and capture output"""
    return subprocess.run(command, capture_output=True, text=True)

def test_add_task():
    result = run_cli_command(["python", "cli_tool.py", "add-task", "Alice", "Submit report"])
    # Check for the task addition message (handling Unicode encoding differences)
    assert "Task 'Submit report' added to Alice." in result.stdout
    assert result.returncode == 0

def test_complete_task_with_script(tmp_path):
    """Runs everything in one subprocess so state is shared."""
    script_path = tmp_path / "script.py"
    script_content = f"""
import sys
sys.path.insert(0, r'{os.getcwd()}')

from models import Task, User

users = {{}}
user = User("Bob")
users["Bob"] = user
task = Task("Finish lab")
user.add_task(task)
task.complete()
"""
    script_path.write_text(script_content)

    result = subprocess.run(["python", str(script_path)], capture_output=True, text=True)
    # Check for the task completion message (handling Unicode encoding differences)
    assert "Task 'Finish lab' completed." in result.stdout
    assert result.returncode == 0
