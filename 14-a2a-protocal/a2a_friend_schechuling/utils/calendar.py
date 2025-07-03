
import random
from datetime import date, datetime, timedelta

def generate_calander() -> dict[str, list[str]]: 
  """
  Generates a random calendar for Karley for the next 7 days.
  Return: 
    dict: key ~ date, 
          value ~ frame time available
  """
  calendar = {}
  today = date.today()
  possible_times = [f"{h:02}:00" for h in range(8, 21)]

  for i in range(7): 
    current_date = today + timedelta(days=i)
    date_str = current_date.strftime("%Y-%m-%d")

    # Select 8 random unique time slots to increase availability
    available_slots = sorted(random.sample(possible_times, 8))
    calendar[date_str] = available_slots

  return calendar
  
