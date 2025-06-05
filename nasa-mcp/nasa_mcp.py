from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os
import sys
from datetime import datetime, timedelta

print("Starting NASA MCP Server...", file=sys.stderr)

load_dotenv(
    "ops/.env"
)

print("Environment loaded", file=sys.stderr)

# Initialize MCP server
mcp = FastMCP("NASA-MCP-Server")

print("MCP server initialized", file=sys.stderr)

# NASA API configuration
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")  # Use DEMO_KEY for testing
BASE_URL = "https://api.nasa.gov"

@mcp.tool()
def get_astronomy_picture_of_the_day() -> dict:
    """Get NASA's Astronomy Picture of the Day (APOD)"""
    try:
        response = requests.get(
            f"{BASE_URL}/planetary/apod",
            params={"api_key": NASA_API_KEY}
        )
        response.raise_for_status()
        return {
            "title": response.json()["title"],
            "url": response.json()["url"],
            "explanation": response.json()["explanation"]
        }
    except Exception as e:
        return {"error": f"Failed to fetch APOD: {str(e)}"}

@mcp.tool()
def get_cme_data(start_date: str = None, end_date: str = None) -> list:
    """Get Coronal Mass Ejection (CME) data from NASA's DONKI API.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date (str): End date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        response = requests.get(
            f"{BASE_URL}/DONKI/CME",
            params={
                "startDate": start_date,
                "endDate": end_date,
                "api_key": NASA_API_KEY
            }
        )
        response.raise_for_status()
        
        cme_data = response.json()
        return [{
            "activity_id": cme["activityID"],
            "start_time": cme["startTime"],
            "source_location": cme["sourceLocation"],
            "note": cme["note"],
            "speed": cme["cmeAnalyses"][0]["speed"] if cme["cmeAnalyses"] else None,
            "latitude": cme["cmeAnalyses"][0]["latitude"] if cme["cmeAnalyses"] else None,
            "longitude": cme["cmeAnalyses"][0]["longitude"] if cme["cmeAnalyses"] else None,
            "half_angle": cme["cmeAnalyses"][0]["halfAngle"] if cme["cmeAnalyses"] else None
        } for cme in cme_data]
    except Exception as e:
        return [{"error": f"Failed to fetch CME data: {str(e)}"}]

@mcp.tool()
def get_near_earth_objects(start_date: str = None, end_date: str = None) -> list:
    """Get information about Near Earth Objects (asteroids and comets) that approach Earth.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format. Defaults to today.
        end_date (str): End date in YYYY-MM-DD format. Defaults to 7 days from today.
    """
    try:
        # Set default dates if not provided
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = requests.get(
            f"{BASE_URL}/neo/rest/v1/feed",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "api_key": NASA_API_KEY
            }
        )
        response.raise_for_status()
        
        neo_data = response.json()
        results = []
        
        for date, objects in neo_data["near_earth_objects"].items():
            for obj in objects:
                results.append({
                    "id": obj["id"],
                    "name": obj["name"],
                    "nasa_jpl_url": obj["nasa_jpl_url"],
                    "absolute_magnitude_h": obj["absolute_magnitude_h"],
                    "estimated_diameter": {
                        "meters": {
                            "min": obj["estimated_diameter"]["meters"]["estimated_diameter_min"],
                            "max": obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
                        }
                    },
                    "is_potentially_hazardous": obj["is_potentially_hazardous_asteroid"],
                    "close_approach_date": date,
                    "relative_velocity": obj["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"],
                    "miss_distance": obj["close_approach_data"][0]["miss_distance"]["kilometers"]
                })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to fetch NEO data: {str(e)}"}]

@mcp.tool()
def get_solar_flares(start_date: str = None, end_date: str = None) -> list:
    """Get Solar Flare data from NASA's DONKI API.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date (str): End date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        response = requests.get(
            f"{BASE_URL}/DONKI/FLR",
            params={
                "startDate": start_date,
                "endDate": end_date,
                "api_key": NASA_API_KEY
            }
        )
        response.raise_for_status()
        
        flare_data = response.json()
        return [{
            "flare_id": flare["flrID"],
            "begin_time": flare["beginTime"],
            "peak_time": flare["peakTime"],
            "end_time": flare["endTime"],
            "class_type": flare["classType"],
            "source_location": flare["sourceLocation"],
            "active_region": flare["activeRegionNum"],
            "instruments": [inst["displayName"] for inst in flare["instruments"]],
            "note": flare["note"],
            "linked_events": [event["activityID"] for event in flare["linkedEvents"]] if flare["linkedEvents"] else []
        } for flare in flare_data]
    except Exception as e:
        return [{"error": f"Failed to fetch solar flare data: {str(e)}"}]

if __name__ == "__main__":
    print("Attempting to run MCP server...", file=sys.stderr)
    try:
        mcp.run(
            transport="stdio"
        )
    except Exception as e:
        print(f"Error running MCP server: {str(e)}", file=sys.stderr)
        raise
