# Car Wash Booking WhatsApp Bot (Twilio + Flask + Firebase)

## 🚀 How to Run

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Add your Firebase `serviceAccountKey.json` in the root directory.

3. Update `.env` with Twilio credentials.

4. Run the app:

```
python app.py
```

5. Use ngrok to expose:

```
ngrok http 5000
```

6. Set the webhook URL in Twilio Console:

```
https://<ngrok-subdomain>.ngrok.io/webhook
```

## ✅ Features

- Book car wash by date and time.
- Dynamic time slot availability.
- Stores bookings in Firebase Firestore.

---

## 🏗️ Improvements

- Add payments (Stripe/PayPal).
- Add appointment reminders.
- Build admin dashboard.