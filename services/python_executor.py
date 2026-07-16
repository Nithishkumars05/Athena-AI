"""
Athena AI

Python Executor

Executes Python code in an isolated subprocess and
captures stdout, stderr, exit code and execution time.

Future Features
---------------
- Package whitelist
- Workspace execution
- File support
- Plot/image capture
- Sandboxed execution
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from pathlib import Path

from models.python_result import PythonResult


class PythonExecutor:

    def __init__(self):

        self.timeout = 30

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        code: str,
    ) -> PythonResult:

        start = time.perf_counter()

        temp_file = None

        try:

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8"
            ) as f:

                f.write(code)

                temp_file = Path(f.name)

            process = subprocess.run(

                [sys.executable, str(temp_file)],

                capture_output=True,

                text=True,

                timeout=self.timeout,

            )

            elapsed = (
                time.perf_counter()
                - start
            )

            return PythonResult(

                success=(
                    process.returncode == 0
                ),

                stdout=process.stdout.strip(),

                stderr=process.stderr.strip(),

                execution_time=elapsed,

                exit_code=process.returncode,

            )

        except subprocess.TimeoutExpired:

            elapsed = (
                time.perf_counter()
                - start
            )

            return PythonResult(

                success=False,

                stderr=f"Execution exceeded {self.timeout} seconds.",

                execution_time=elapsed,

                exit_code=-1,

            )

        except Exception as e:

            elapsed = (
                time.perf_counter()
                - start
            )

            return PythonResult(

                success=False,

                stderr=str(e),

                execution_time=elapsed,

                exit_code=-1,

            )

        finally:

            if temp_file and temp_file.exists():

                try:

                    temp_file.unlink()

                except Exception:

                    pass


python_executor = PythonExecutor()