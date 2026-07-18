"""
Recipe 50 (V2): Build Health Checks and Recovery

Problem: Automation should tell you it's alive. Heartbeat
monitoring, crash recovery, and graceful shutdown.
"""
import asyncio, time, subprocess
from pathlib import Path

HEARTBEAT = Path("/tmp/automation.alive")


def touch():
    HEARTBEAT.write_text(str(time.time()))


def is_alive(timeout=300):
    if not HEARTBEAT.exists():
        return False
    return time.time() - float(HEARTBEAT.read_text()) < timeout


async def run_with_heartbeat(script, max_restarts=3):
    for attempt in range(1, max_restarts + 1):
        print(f"Starting (attempt {attempt}/{max_restarts})")
        proc = await asyncio.create_subprocess_exec(
            "python", script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=3600)
            print("Completed successfully")
            return
        except asyncio.TimeoutError:
            proc.kill()
            print("Timed out, restarting...")
        except Exception as e:
            print(f"Crashed: {e}")

    print("Max restarts reached")


async def main():
    # Simulate a heartbeat during automation
    for i in range(5):
        touch()
        print(f"Heartbeat {i+1}: alive")
        await asyncio.sleep(1)

    # Check if still alive
    print(f"Health check: {'ALIVE' if is_alive() else 'DEAD'}")
    # Clean up
    if HEARTBEAT.exists():
        HEARTBEAT.unlink()


if __name__ == "__main__":
    asyncio.run(main())
