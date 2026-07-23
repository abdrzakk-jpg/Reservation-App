from pathlib import Path
from dotenv import load_dotenv
import os



# load .env file
env_path = Path(__file__).cwd() / "_internal" / ".env"
if not os.path.exists(env_path):
    env_path = Path(__file__).cwd() / ".env"  


load_dotenv(str(env_path))

# load EnvVars
ip: str = os.getenv("gateaway_ip")
check_interval_in_hours: int = int(os.getenv("check_interval_in_hours"))