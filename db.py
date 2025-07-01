import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

WORKING_HOURS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]

def get_bookings_for_date(date):
    bookings_ref = db.collection("bookings").document(date)
    doc = bookings_ref.get()
    if doc.exists:
        return doc.to_dict().get("times", [])
    return []

def get_available_slots(date):
    booked = get_bookings_for_date(date)
    available = [slot for slot in WORKING_HOURS if slot not in booked]
    return available

def save_booking(date, time, phone):
    bookings_ref = db.collection("bookings").document(date)
    doc = bookings_ref.get()

    if doc.exists:
        current = doc.to_dict().get("times", [])
        if time in current:
            return False  # Slot already booked
        current.append(time)
        bookings_ref.set({"times": current}, merge=True)
    else:
        bookings_ref.set({"times": [time]})

    db.collection("customers").add({
        "date": date,
        "time": time,
        "phone": phone,
        "created_at": datetime.utcnow()
    })

    return True