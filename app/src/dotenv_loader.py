from dotenv import load_dotenv
import os

load_dotenv(".env")

ip: str | None = os.getenv("gateaway_ip")
check_interval_in_hours: int | None = os.getenv("check_interval_in_hours")