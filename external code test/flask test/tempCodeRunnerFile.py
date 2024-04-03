from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(f"{request.form['']}")
        return render_template('result.html')
    return render_template('result.html')

@app.route('/',)
def home():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
