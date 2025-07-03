from datetime import datetime, timedelta
from utils import generate_calander

KARLEY_CALENDAR = generate_calander()


def get_availability(start_date: str, end_date: str) -> str:
  """
  Checks Karley's availability for a given date range.

  Args:
      start_date: The start of the date range to check, in YYYY-MM-DD format.
      end_date: The end of the date range to check, in YYYY-MM-DD format.

  Returns:
      A string listing Karley's available times for that date range.
  """
   
  try:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    if start > end:
      return "Invalid date range. The start date cannot be after the end date."

    results = []
    delta = end - start
    for i in range(delta.days + 1):
      day = start + timedelta(days=i)
      date_str = day.strftime("%Y-%m-%d")
      available_slots = KARLEY_CALENDAR.get(date_str, [])
      if available_slots:
          availability = f"On {date_str}, Karley is available at: {', '.join(available_slots)}."
          results.append(availability)
      else:
          results.append(f"Karley is not available on {date_str}.")

      return "\n".join(results)

  except ValueError:
    return (
        "Invalid date format. Please use YYYY-MM-DD for both start and end dates."
    )
