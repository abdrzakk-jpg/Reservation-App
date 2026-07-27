from pathlib import Path
from dotenv import load_dotenv
import os, sys



# load .env file
if getattr(sys, "frozen", False):
    env_path = Path(sys.executable).parent / "_internal" / ".env"
else:
    env_path = Path(__file__).resolve().parents[2] / ".env"

print("env_path =", env_path)

load_dotenv(str(env_path))
# load EnvVars
ip: str = os.getenv("gateaway_ip")
check_interval_in_hours: int = int(os.getenv("check_interval_in_hours"))
