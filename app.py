from flask import Flask, request, jsonify, render_template
from recipe_scrapers import scrape_me

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = request.form.get('url') if request.method == 'POST' else None

    if url:
        try:
            scraper = scrape_me(url, wild_mode=True)
            result = {
                'success': True,
                'title': scraper.title(),
                'host': scraper.host(),
                'total_time': scraper.total_time(),
                'image': scraper.image(),
                'ingredients': scraper.ingredients(),
                'instructions': scraper.instructions(),
                'instructions_list': scraper.instructions_list(),
                'yields': scraper.yields(),
                'nutrients': scraper.nutrients()
            }
        except Exception as e:
            result = {'success': False, 'error_message': str(e)}
    else:
        result = {'success': False, 'error_message': 'Please provide a valid URL.'}

    if request.method == 'POST':
        return jsonify(result)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
