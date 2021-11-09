"""
Simple "Hello, World" application using Flask
"""

from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/nearest', methods = ['POST'])
def return_station():
    if request.method == "POST":
        location =  request.form["location"]
        data = mbta_helper.find_stop_near(location)

        if data[0] == "There was an error":
            return render_template("error.html")
        return render_template("mbta.html", station_name=data[0], wheelchair_accessible=data[1])

    

@app.route('/square/')
@app.route('/square/<number>')
def square(number=None):
    if number:
        sqrnum = float(number) ** 2
        return f'<h1>{number} squared is {sqrnum}</h1>'
    return 'Add a number to the end of the url to square it!'

if __name__=='__main__':
    app.run(debug=True)
