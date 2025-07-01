from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from db import get_available_slots, save_booking
from utils import parse_date, parse_time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# In-memory context (for demo purposes)
user_context = {}

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    response = handle_message(from_number, incoming_msg)
    msg.body(response)

    return str(resp)


def handle_message(phone, text):
    context = user_context.get(phone, {})
    last_date = context.get('last_date')

    if 'hi' in text or 'hello' in text:
        return "👋 Welcome to QuickCar Wash!\nPlease provide your preferred date (YYYY-MM-DD) for booking."

    date = parse_date(text)
    if date:
        slots = get_available_slots(date)
        if slots:
            user_context[phone] = {'last_date': date}
            return f"🗓 Available time slots on {date}:\n" + "\n".join(slots) +                    "\n\nPlease reply with your preferred time (e.g., 10:00)."
        else:
            return f"❌ No slots available on {date}. Please choose another date."

    time = parse_time(text)
    if time:
        if not last_date:
            return "⚠️ Please provide a date first before selecting a time."

        success = save_booking(last_date, time, phone)
        if success:
            user_context.pop(phone, None)
            return f"✅ Your appointment is confirmed for {last_date} at {time}.\nThank you! 🚗💦"
        else:
            return f"❌ Sorry, {time} on {last_date} is already booked. Try another time."

    return "❓ I didn't understand. Please provide a date (YYYY-MM-DD) or a time (e.g., 10:00)."

if __name__ == "__main__":
    app.run(port=5000, debug=True)