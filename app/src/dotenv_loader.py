from dotenv import load_dotenv
import os

# load .env file
load_dotenv(".env")

# load EnvVars
ip: str = os.getenv("gateaway_ip")
check_interval_in_hours: int = int(os.getenv("check_interval_in_hours"))