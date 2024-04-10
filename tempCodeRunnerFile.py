
            current_user.password = generate_password_hash(password1,method='pbkdf2:sha256',salt_length=8)