from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import io

app = Flask(_name_)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plot' , methods = ["POST"])
def plot():
    # Generate the plot
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

if _name_ == '_main_':
    app.run(debug=True)