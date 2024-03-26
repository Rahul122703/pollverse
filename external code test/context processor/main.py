from flask import Flask, render_template

app = Flask(__name__)

# Context processor function
@app.context_processor
def common_variable():
    # Set the values for common variables
    logged_in = 1
    not_registering = 0
    current_user_id = 123
    otp_send = 1
    anonymous_mode = 0
    current_user_email = "example@example.com"
    user_otp = "123456"
    user_obj = {"name": "John Doe", "age": 30}
    username = "john_doe"
    user_icon = "user_icon.jpg"
    
    # Return a dictionary containing the variables
    return dict(logged_in=logged_in,
                not_registering=not_registering,
                current_user_id=current_user_id,
                otp_send=otp_send,
                anonymous_mode=anonymous_mode,
                current_user_email=current_user_email,
                user_otp=user_otp,
                user_obj=user_obj,
                username=username,
                user_icon=user_icon)

# Route
@app.route('/')
def index():
    # Render the template and pass no additional context
    return render_template('example.html')

if __name__ == '__main__':
    app.run(debug=True)
