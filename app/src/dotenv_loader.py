from dotenv import load_dotenv
import os

load_dotenv(".env")

ip: str = os.getenv("gateaway_ip")
check_interval_in_hours: int = int(os.getenv("check_interval_in_hours"))