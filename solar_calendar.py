import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from ics import Calendar, Event

# --- CONFIGURATION ---
LATITUDE = 45.487
LONGITUDE = -122.804
TIMEZONE = "America/Los_Angeles"
LOCATION_NAME = "Beaverton"
DAYS_AHEAD = 1826  # 5-year rolling window

def generate_solar_calendar():
    loc = LocationInfo(LOCATION_NAME, "", TIMEZONE, LATITUDE, LONGITUDE)
    tz = pytz.timezone(TIMEZONE)
    cal = Calendar()
    
    today = datetime.date.today()
    print(f"Generating 5-year solar calendar (with Zenith) for {LOCATION_NAME}...")
    
    for i in range(DAYS_AHEAD):
        current_day = today + datetime.timedelta(days=i)
        
        try:
            s = sun(loc.observer, date=current_day, tzinfo=tz)
            sunrise = s['sunrise']
            solar_noon = s['noon']  # Added: Exact solar transit / zenith moment
            sunset = s['sunset']
        except Exception:
            continue
            
        # 1. Sunrise Event (15-minute block)
        e_sunrise = Event(
            name="🌅 Sunrise",
            begin=sunrise,
            end=sunrise + datetime.timedelta(minutes=15),
            description=f"Sunrise in {LOCATION_NAME}: {sunrise.strftime('%I:%M %p')}"
        )
        cal.events.add(e_sunrise)
        
        # 2. Solar Noon / Zenith Event (15-minute block)
        e_noon = Event(
            name="☀️ Solar Noon",
            begin=solar_noon,
            end=solar_noon + datetime.timedelta(minutes=15),
            description=f"Solar Zenith (Highest point) in {LOCATION_NAME}: {solar_noon.strftime('%I:%M %p')}"
        )
        cal.events.add(e_noon)
        
        # 3. Sunset Event (15-minute block)
        e_sunset = Event(
            name="🌇 Sunset",
            begin=sunset,
            end=sunset + datetime.timedelta(minutes=15),
            description=f"Sunset in {LOCATION_NAME}: {sunset.strftime('%I:%M %p')}"
        )
        cal.events.add(e_sunset)
        
    filename = "sunrise_sunset.ics"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(cal.serialize_iter())
    print(f"Successfully saved {filename} with 5 years of solar data including Zenith.")

if __name__ == "__main__":
    generate_solar_calendar()
