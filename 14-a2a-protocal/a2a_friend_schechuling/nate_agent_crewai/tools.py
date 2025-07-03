from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Type
from crewai.tools import BaseTool
from utils import generate_calander


NATE_CALENDAR = generate_calander()

class AvailabilityToolInput(BaseModel): 
  """Input schema for AvailabilityTool."""
  date_range: str = Field(
    ..., 
    description="The date or date range to check for availability, e.g., '2024-07-28' or '2024-07-28 to 2024-07-30'."
  )

class AvailabilityTool(BaseTool): 
  name: str = "Calendar Availability Checker"
  description: str = (
    "Checks my availability for a given date or date range. "
    "Use this to find out when I am free."
  )
  args_schema: Type[BaseModel] = AvailabilityToolInput

  def _run(self, date_range: str) -> str:
    """Checks my availability for a given date range."""
    dates_to_check = [d.strip() for d in date_range.split("to")]
    start = dates_to_check[0]
    end = dates_to_check[-1]
    try:
      start = datetime.strptime(start, "%Y-%m-%d").date()
      end = datetime.strptime(end, "%Y-%m-%d").date()

      if start > end:
        return (
            "Invalid date range. The start date cannot be after the end date."
        )

      results = []
      delta = end - start
      for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        available_slots = NATE_CALENDAR.get(date_str, [])
        if available_slots:
            availability = f"On {date_str}, I am available at: {', '.join(available_slots)}."
            results.append(availability)
        else:
            results.append(f"I am not available on {date_str}.")

      return "\n".join(results)

    except ValueError:
      return (
        "I couldn't understand the date. "
        "Please ask to check availability for a date like 'YYYY-MM-DD'."
      )