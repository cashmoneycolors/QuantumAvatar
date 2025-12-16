#!/usr/bin/env python3
"""
PARALLEL TRAINING ORCHESTRATOR - Quantum Avatar Massive Training
Train all available quantum components simultaneously in parallel
"""

import asyncio
import argparse
import json
import os
from pathlib import Path
import time
from datetime import datetime

class ParallelTrainer:
    def __init__(self, *, concurrency: int = 4, timeout_seconds: int = 300, targets: list[str] | None = None):
        self.training_processes = []
        self.training_logs = {}
        self.concurrency = max(1, int(concurrency))
        self.timeout_seconds = max(1, int(timeout_seconds))
        self.training_targets = targets or [
            # QuantumAvatar Core Training
            "python quantum_training_loop.py",
            "python auto_training_executor.py",
            "python live_api_integration.py",

            # Performance Managers
            "python JOULE_PERFORMANCE_PC_MANAGER.py",
            "python TERMINAL_QUANTUM_EMPIRE_APP.py",

            # Final Systems
            "python FINAL_QUANTUM_AVATAR_BUSINESS_EMPIRE_APP.py",

            # External Repositories
            r'cd /d "C:\Users\nazmi\-MEGA-ULTRA-ROBOTER-KI" && install.bat',
            r'cd /d "C:\Users\nazmi\-MEGA-ULTRA-ROBOTER-KI-1" && install.bat',
            r'cd /d "C:\Users\nazmi\modules" && python app_generator.py',
            r'cd /d "C:\Users\nazmi\desktop-tutorial" && install.bat'
        ]

    def _derive_process_name(self, command: str) -> str:
        cmd = command.strip()
        if "&&" in cmd:
            cmd = cmd.split("&&")[-1].strip()

        parts = cmd.split()
        if not parts:
            return "process"

        first = parts[0].lower()
        if first in {"python", "python3", "py"} and len(parts) > 1:
            target = parts[1]
        else:
            target = parts[0]

        target = target.strip('"').strip("'")

        if target == "-c":
            return "python-c"
        return Path(target).stem

    async def execute_training_process(self, command, name):
        """Execute a single training process with monitoring"""
        start_time = time.time()
        print(f"\n[STARTING] {name}")
        print(f"Command: {command}")
        print("-" * 80)

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd()
            )

            self.training_processes.append((name, process))

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout_seconds
                )

                end_time = time.time()
                duration = end_time - start_time

                result = {
                    "name": name,
                    "command": command,
                    "duration": duration,
                    "success": process.returncode == 0,
                    "return_code": process.returncode,
                    "stdout": stdout.decode()[:1000] if stdout else "",  # First 1000 chars
                    "stderr": stderr.decode()[:1000] if stderr else "",
                    "timestamp": datetime.now().isoformat()
                }

                self.training_logs[name] = result

                status = "[SUCCESS]" if result["success"] else "[FAILED]"
                print(f"\n{status}: {name} completed in {duration:.1f}s")
                print(f"Return code: {process.returncode}")

                if stderr and len(stderr.decode()) > 0:
                    print(f"STDERR: {stderr.decode()[:500]}...")

            except asyncio.TimeoutError:
                process.terminate()
                await process.wait()
                result = {
                    "name": name,
                    "command": command,
                    "duration": self.timeout_seconds,
                    "success": False,
                    "return_code": -1,
                    "stdout": "",
                    "stderr": "TIMEOUT EXCEEDED",
                    "timestamp": datetime.now().isoformat()
                }
                self.training_logs[name] = result
                print(f"\n[TIMEOUT]: {name} exceeded {self.timeout_seconds}s limit")

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            result = {
                "name": name,
                "command": command,
                "duration": duration,
                "success": False,
                "return_code": -2,
                "stdout": "",
                "stderr": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.training_logs[name] = result
            print(f"\n[EXCEPTION]: {name} failed with error: {e}")

    async def run_parallel_training(self):
        """Run all training processes in parallel with controlled concurrency"""
        print("=" * 100)
        print("[QUANTUM AVATAR] - MASSIVE PARALLEL TRAINING ORCHESTRATOR")
        print("[ALL COMPONENTS] TRAINING SIMULTANEOUSLY")
        print("=" * 100)
        print(f"Found {len(self.training_targets)} training components to execute")
        print("May the quantum coherence be with us... [Quantum Physics Loading]")
        print("Target Cohrence >= 2.0 | Performance Boost >= 500% | Autonomous Level MAX")
        print("=" * 100)

        start_master = time.time()

        # Execute all training processes in parallel (limited to 4 concurrent)
        semaphore = asyncio.Semaphore(self.concurrency)  # Limit concurrent processes

        async def execute_with_semaphore(command_and_name):
            command, name = command_and_name
            async with semaphore:
                await self.execute_training_process(command, name)

        tasks = [
            execute_with_semaphore((cmd, f"{idx:02d}-{self._derive_process_name(cmd)}"))
            for idx, cmd in enumerate(self.training_targets, start=1)
        ]

        # Wait for all to complete
        await asyncio.gather(*tasks, return_exceptions=True)

        end_master = time.time()
        total_duration = end_master - start_master

        print("\n" + "=" * 100)
        print("[TRAINING ORCHESTRATION COMPLETED]")
        print("=" * 100)
        print(f"Total training time: {total_duration:.1f} seconds")
        print(f"Components trained: {len(self.training_targets)}")

        successful = sum(1 for log in self.training_logs.values() if log["success"])
        failed = len(self.training_targets) - successful

        print(f"[SUCCESSFUL]: {successful}")
        print(f"[FAILED]: {failed}")

        # Save comprehensive training log
        self.save_master_training_log()

        print("\n[MASTER LOG] SAVED: 'parallel_training_master_log.json'")

        if successful > 0:
            print("\nMASSIVE QUANTUM TRAINING COMPLETE!")
            print(f"[ENHANCED] {successful} components successfully enhanced!")
            print("[EVOLUTION] Quantum Avatar evolution achieved!")
        else:
            print("\n[WARNING] ALL TRAINING COMPONENTS FAILED - CHECK LOGS")

    def save_master_training_log(self):
        """Save comprehensive training results"""
        master_log = {
            "training_summary": {
                "total_components": len(self.training_targets),
                "successful_components": sum(1 for log in self.training_logs.values() if log["success"]),
                "failed_components": sum(1 for log in self.training_logs.values() if not log["success"]),
                "total_training_time": sum(log["duration"] for log in self.training_logs.values()),
                "average_component_time": sum(log["duration"] for log in self.training_logs.values()) / len(self.training_logs),
                "best_performing_component": max(self.training_logs.items(), key=lambda x: x[1]["duration"]) if self.training_logs else None,
                "timestamp": datetime.now().isoformat()
            },
            "component_results": self.training_logs,
            "targets_executed": self.training_targets
        }

        with open("parallel_training_master_log.json", "w") as f:
            json.dump(master_log, f, indent=2)


async def main():
    parser = argparse.ArgumentParser(description="Quantum Avatar parallel training orchestrator")
    parser.add_argument("--dry-run", action="store_true", help="Print targets and exit without running")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N targets (0 = all)")
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start at target index (1-based). Useful for running only a slice of targets.",
    )
    parser.add_argument("--concurrency", type=int, default=4, help="Max parallel processes")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per process in seconds")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run a short self-test (validates subprocess/logging without running training scripts)",
    )
    args = parser.parse_args()

    targets = None
    if args.self_test:
        targets = [
            'python -c "print(\\\"SELFTEST_OK\\\")"',
            'python -c "import time; time.sleep(1); print(\\\"SELFTEST_SLEEP_OK\\\")"',
        ]

    print("Initializing Parallel Training Orchestrator...")
    trainer = ParallelTrainer(concurrency=args.concurrency, timeout_seconds=args.timeout, targets=targets)

    start_idx = max(1, int(args.start)) - 1
    if start_idx:
        trainer.training_targets = trainer.training_targets[start_idx:]

    if args.limit and args.limit > 0:
        trainer.training_targets = trainer.training_targets[: args.limit]

    if args.dry_run:
        print("[DRY-RUN] Targets to execute:")
        for idx, cmd in enumerate(trainer.training_targets, start=1):
            print(f"{idx:02d}. {cmd}")
        return

    await trainer.run_parallel_training()


if __name__ == "__main__":
    asyncio.run(main())
