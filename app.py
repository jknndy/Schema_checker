from flask import Flask, request, jsonify, render_template
from recipe_scrapers import scrape_me

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/list')
def list_page():
    return render_template('list.html')

@app.route('/generate_test', methods=['POST'])
def generate_test():
    data = request.get_json()
    test_template = """
    def test_host(self):
        self.assertEqual("{host}", self.harvester_class.host())
    def test_author(self):
        self.assertEqual("{author}", self.harvester_class.author())
    """
    formatted_test = test_template.format(**data)
    return render_template('test.html', test=formatted_test)

@app.route('/schema', methods=['GET', 'POST'])
def index():
    url = request.form.get('url') if request.method == 'POST' else None

    def get_attribute(attribute_func):
        try:
            return attribute_func()
        except:
            return "not available"
    if url:
        try:
            scraper = scrape_me(url, wild_mode=True)
            result = {
                'success': True,
                'title': get_attribute(scraper.title),
                'host': get_attribute(scraper.host),
                'total_time': get_attribute(scraper.total_time),
                'image': get_attribute(scraper.image),
                'ingredients': get_attribute(scraper.ingredients),
                'instructions': get_attribute(scraper.instructions),
                'instructions_list': get_attribute(scraper.instructions_list),
                'yields': get_attribute(scraper.yields),
                'nutrients': get_attribute(scraper.nutrients),
                'category': get_attribute(scraper.category),
                'cuisine': get_attribute(scraper.cuisine),
                'ratings': get_attribute(scraper.ratings),
                'description': get_attribute(scraper.description),
                'author': get_attribute(scraper.author)
            }
        except Exception as e:
            result = {'success': False, 'error_message': str(e)}
    else:
        result = {'success': False, 'error_message': 'Please provide a valid URL.'}

    if request.method == 'POST':
        response = jsonify(result)
        response.headers.add('Content-Type', 'text/plain')  # Set response content type to plain text
        response_data = "\n".join(f"{key}: {value}" for key, value in result.items())
        response.set_data(response_data)
        return response
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
