from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def hello_world():
    name='NGP'
    return render_template('index.html',name=name)
@app.route('/i')
def invite():
    return render_template('Task1.html')
if __name__ == '__main__':
    app.run(debug=True)
