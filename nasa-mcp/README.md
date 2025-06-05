# NASA MCP Server

A Model Context Protocol (MCP) server that provides access to various NASA Open APIs, allowing AI models to interact with NASA's data.

## Features

This MCP server provides access to several NASA APIs:

1. **Astronomy Picture of the Day (APOD)**
   - Get NASA's daily featured astronomical image
   - Includes title, image URL, and explanation

2. **Coronal Mass Ejection (CME) Data**
   - Track solar eruptions and their characteristics
   - Includes speed, location, and impact predictions

3. **Near Earth Objects (NEO)**
   - Monitor asteroids and comets approaching Earth
   - Get size, velocity, and closest approach data

4. **Solar Flare Data**
   - Track solar flare activity
   - Includes classification, timing, and associated events

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- NASA API key (get one at https://api.nasa.gov/)
- Claude App

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nasa_mcp
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create an environment file:
   ```bash
   mkdir ops
   touch ops/.env
   ```

5. Add your NASA API key to `ops/.env`:
   ```
   NASA_API_KEY=your_api_key_here
   ```

## Running the Server

1. Start the MCP server:
   ```bash
   python nasa_mcp.py
   ```

## Using with Claude App

1. Open Claude App
2. Open settings and go to developer and select edit config
3. Add the following to the config:
```
{
  "mcpServers": {
    "nasa-mcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/nasa_mcp.py"
      ],
      "env": {
        "NASA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```
4. Restart the claude app

## API Details

### Astronomy Picture of the Day
- Returns daily featured astronomical image
- Includes title, image URL, and explanation

### CME Data
- Tracks solar eruptions
- Provides speed, location, and impact data
- Default date range: yesterday to today

### Near Earth Objects
- Monitors asteroids and comets
- Includes size, velocity, and approach data
- Default date range: today to 7 days ahead

### Solar Flare Data
- Tracks solar flare activity
- Includes classification (X, M, C, B, A classes)
- Provides timing and location data
- Default date range: yesterday to today
