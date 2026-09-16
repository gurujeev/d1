def send_activation_email(email: str, token: str):

    link = (
        f"http://localhost:8000/activate.html"
        f"?token={token}"
    )

    print("\n========== ACTIVATION EMAIL ==========")
    print(f"To: {email}")
    print("Subject: Activate your College Portal account")
    print(f"Activation link: {link}")
    print("======================================\n")


def send_password_reset_email(email: str, token: str):

    link = (
        f"http://localhost:8000/reset-password.html"
        f"?token={token}"
    )

    print("\n========== PASSWORD RESET ==========")
    print(f"To: {email}")
    print("Subject: Reset your College Portal password")
    print(f"Reset link: {link}")
    print("====================================\n")