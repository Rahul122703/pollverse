            hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256',salt_length=8)
