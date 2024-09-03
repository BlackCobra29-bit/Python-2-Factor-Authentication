import pyotp
import qrcode
from twilio.rest import Client

# Twilio setup
TWILIO_ACCOUNT_SID = 'YOUR_ACCOUNT_SSID'
TWILIO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_ACCOUNT_PHONE_NUMBER'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_secret():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    return totp.secret

def generate_qr_code(secret, user_email):
    totp = pyotp.TOTP(secret, interval=60)
    provisioning_uri = totp.provisioning_uri(name=user_email, issuer_name="YourAppName")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save("qrcode.png")
    print("QR Code saved as 'qrcode.png'.")

def send_sms(phone_number, otp):
    message = client.messages.create(
        body=f'Your OTP code is {otp}. It is valid for 1 minute.',
        from_=TWILIO_PHONE_NUMBER,
        to="RECEIVER_PHONE_NUMBER" #replace this with the actual receiver phone number
    )
    print(f'SMS sent to {phone_number}: {message.sid}')


def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret, interval=60)
    return totp.verify(otp)

if __name__ == "__main__":
    user_email = "user@example.com"
    user_phone_number = "+1234567890"  # Replace with the user's phone number
    
    # Generate and display the secret key
    secret = generate_secret()
    print(f"Secret: {secret}")
    
    # Generate and display the QR code
    generate_qr_code(secret, user_email)
    
    # Generate an OTP and send it via SMS
    totp = pyotp.TOTP(secret, interval=60)
    otp = totp.now()
    send_sms(user_phone_number, otp)
    
    # Example OTP verification
    otp_input = input("Enter the OTP from your SMS: ")
    if verify_otp(secret, otp_input):
        print("OTP is valid!")
    else:
        print("Invalid OTP.")