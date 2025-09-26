from datetime import datetime, timedelta
class CalendarTool:
    def book_meeting(self, user_id: str, duration_min: int = 30):
        when = (datetime.utcnow() + timedelta(days=1, hours=1)).strftime("%Y-%m-%d %H:%M UTC")
        return {"when": when, "link": "https://meet.example.com/nestwell-demo"}
