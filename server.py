import os
import datetime
from garminconnect import Garmin
from mcp.server.fastmcp import FastMCP

GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL")
GARMIN_PASSWORD = os.environ.get("GARMIN_PASSWORD")

mcp = FastMCP("garmin-connector")
client = None

def get_client():
    global client
    if client is None:
        client = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD)
        client.login()
    return client

@mcp.tool()
def ultima_attivita() -> str:
    """Restituisce l'ultima attività registrata su Garmin Connect."""
    c = get_client()
    activities = c.get_activities(0, 1)
    if not activities:
        return "Nessuna attività trovata."
    a = activities[0]
    return f"{a.get('activityName')} - {a.get('distance')}m - {a.get('duration')}s - {a.get('startTimeLocal')}"

@mcp.tool()
def passi_oggi() -> str:
    """Restituisce il numero di passi di oggi."""
    c = get_client()
    oggi = datetime.date.today().isoformat()
    dati = c.get_steps_data(oggi)
    return str(dati)

@mcp.tool()
def frequenza_cardiaca_oggi() -> str:
    """Restituisce i dati di frequenza cardiaca di oggi."""
    c = get_client()
    oggi = datetime.date.today().isoformat()
    dati = c.get_heart_rates(oggi)
    return str(dati)

if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http")
