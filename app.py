from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Add a route to handle form submission
@app.route('/run_script', methods=['POST'])
def run_script():
    url = request.form.get('url')

    # Implement your Python script logic here.
    # You can use libraries like requests to fetch the URL content and process it.

    # Sample response for testing purposes
    result = f"Running script with URL: {url}"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
