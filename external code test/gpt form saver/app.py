from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

# Database Models
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship('Comment', remote_side=[id])
    replies = db.relationship('Comment')

# Routes
@app.route('/')
def index():
    with app.app_context():
        comments = Comment.query.filter_by(parent_id=None).all()
    return render_template('index.html', comments=comments)

@app.route('/save_comment', methods=['POST'])
def save_comment():
    with app.app_context():
        body = request.form['body']
        comment = Comment(body=body)
        db.session.add(comment)
        db.session.commit()
    return redirect('/')

@app.route('/save_reply', methods=['POST'])
def save_reply():
    with app.app_context():
        body = request.form['body']
        parent_id = request.form['parent_id']
        parent = Comment.query.get(parent_id)
        reply = Comment(body=body, parent=parent)
        db.session.add(reply)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
