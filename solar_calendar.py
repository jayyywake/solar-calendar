import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from ics import Calendar, Event

# --- CONFIGURATION ---
# Replace these with your exact target coordinates and timezone
LATITUDE = 45.487
LONGITUDE = -122.804
TIMEZONE = "America/Los_Angeles"
LOCATION_NAME = "Beaverton"
DAYS_AHEAD = 365  # A 1-year rolling window keeps the sync incredibly fast

def generate_solar_calendar():
    loc = LocationInfo(LOCATION_NAME, "", TIMEZONE, LATITUDE, LONGITUDE)
    tz = pytz.timezone(TIMEZONE)
    cal = Calendar()
    
    today = datetime.date.today()
    print(f"Generating sunrise/sunset calendar for {LOCATION_NAME}...")
    
    for i in range(DAYS_AHEAD):
        current_day = today + datetime.timedelta(days=i)
        
        try:
            # Calculate solar events for the day
            s = sun(loc.observer, date=current_day, tzinfo=tz)
            sunrise = s['sunrise']
            sunset = s['sunset']
        except Exception:
            # Handles edge cases for extreme polar regions where the sun doesn't rise/set
            continue
            
        # 1. Create Sunrise Event (15-minute visual block on your grid)
        e_sunrise = Event(
            name="☀️⬆️ Sunrise",
            begin=sunrise,
            end=sunrise + datetime.timedelta(minutes=15),
            description=f"Sunrise in {LOCATION_NAME}: {sunrise.strftime('%I:%M %p')}"
        )
        cal.events.add(e_sunrise)
        
        # 2. Create Sunset Event (15-minute visual block on your grid)
        e_sunset = Event(
            name="☀️⬇️ Sunset",
            begin=sunset,
            end=sunset + datetime.timedelta(minutes=15),
            description=f"Sunset in {LOCATION_NAME}: {sunset.strftime('%I:%M %p')}"
        )
        cal.events.add(e_sunset)
        
    # Write the compiled data out to the ICS file
    filename = "sunrise_sunset.ics"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(cal.serialize_iter())
    print(f"Successfully saved {filename}")

if __name__ == "__main__":
    generate_solar_calendar()
