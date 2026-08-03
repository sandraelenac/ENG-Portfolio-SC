from air_traffic_control.opensky_api import OpenSkyApi
from datetime import datetime, timezone

api = OpenSkyApi()

def to_unix(dt: datetime) -> int:
    """Convert timezone-aware datetime to Unix timestamp (UTC seconds since epoch)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())

def from_unix(timestamp: int) -> datetime:
    """Convert Unix timestamp to timezone-aware UTC datetime."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)

def get_flights(airport: str, start: datetime, end: datetime, type: str = "arrival"):
    """
    Query OpenSky for arrival/departure flights to/from an airport.
    
    Parameters:
        airport (str): ICAO airport code (e.g., 'KLAX')
        start (datetime): Start of time window
        end (datetime): End of time window
        type (str): 'arrival', 'departure', or 'both'
    
    Returns:
        list: List of flight objects (arrivals, departures, or both)
    """
    try:
        api = OpenSkyApi()

        # Convert datetime to Unix timestamps
        start_unix = int(start.timestamp())
        end_unix = int(end.timestamp())

        flights = []

        if type == "arrival":
            flights = api.get_arrivals_by_airport(airport, start_unix, end_unix)
        elif type == "departure":
            flights = api.get_departures_by_airport(airport, start_unix, end_unix)
        elif type == "both":
            arrivals = api.get_arrivals_by_airport(airport, start_unix, end_unix)
            departures = api.get_departures_by_airport(airport, start_unix, end_unix)
            flights = (arrivals or []) + (departures or [])
        else:
            raise ValueError("Invalid flight type: choose 'arrival', 'departure', or 'both'.")

        if flights is None:
            print("⚠️ OpenSky returned None — no data or rate-limited.")
            return []
        
        return flights

    except Exception as e:
        print(f"❌ Error loading flights from OpenSky: {e}")
        return []

def get_aircraft_track_path(uid: str, timestamp: int=None):
    if timestamp is None:
        timestamp = 0
        
    track = api.get_track_by_aircraft(uid, timestamp)

    if track is None:
        raise ValueError("No track found")
    
    return track
