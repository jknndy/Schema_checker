# app.py

from flask import Flask, render_template, request, redirect, url_for
import csv
import requests
from recipe_scrapers import scrape_me
from recipe_scrapers._exceptions import WebsiteNotImplementedError

app = Flask(__name__)

def check_url_in_csv(url):
    # Check if the given URL or its variation is in the existing-urls.csv file.
    with open('existing-urls.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if url in row:
                return True
    return False

def write_url_to_csv(url):
    # Write the URL to the existing-urls.csv file.
    with open('existing-urls.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    url = request.form.get('url')

    try:
        # Fetch content from the URL with a custom user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                # Use recipe-scrapers to fetch recipe data
                scraper = scrape_me(url)

                # Check if scraper has the 'title' attribute to determine schema presence
                has_schema = hasattr(scraper, 'title')

                # Check if the URL is already in the existing-urls.csv file
                url_exists = check_url_in_csv(url)

                # Check if the URL exists and has schema, then redirect to the results page
                if has_schema and not url_exists:
                    return redirect(url_for('show_results', url=url))

                # Prepare the data to display in the template
                result_data = {
                    'url': url,
                    'has_schema': has_schema,
                    'url_exists': url_exists,
                    'scraper': scraper,
                }
                return render_template('index.html', **result_data)

            except WebsiteNotImplementedError as e:
                content = f"Error: Website ({url}) is not supported."
                result_data = {
                    'url': url,
                    'error_message': content,
                }
                return render_template('index.html', **result_data)

        else:
            content = f"Failed to fetch content from {url} (Status Code: {response.status_code})"
            result_data = {
                'url': url,
                'error_message': content,
            }
            return render_template('index.html', **result_data)

    except requests.exceptions.RequestException as e:
        content = str(e)
        result_data = {
            'url': url,
            'error_message': content,
        }
        return render_template('index.html', **result_data)

    return render_template('index.html', url=url, error_message="Failed to fetch content from the URL.")


@app.route('/results')
def show_results():
    url = request.args.get('url')

    try:
        # Use recipe-scrapers to fetch recipe data with a custom user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Use recipe-scrapers to fetch recipe data
            scraper = scrape_me(url)

            # Check if scraper has the 'title' attribute to determine schema presence
            has_schema = hasattr(scraper, 'title')

            # Check if the URL is already in the existing-urls.csv file
            url_exists = check_url_in_csv(url)

            # Prepare the data to display in the template
            result_data = {
                'url': url,
                'has_schema': has_schema,
                'url_exists': url_exists,
                'scraper': scraper,
            }

            # Check if the URL exists and has schema, then render the results template
            if has_schema and not url_exists:
                return render_template('results.html', **result_data)

            # If the URL exists in the CSV file, display a message with a hyperlink to the results page
            if url_exists:
                return render_template('index.html', **result_data, existing_url_message=True)

    except requests.exceptions.RequestException as e:
        content = str(e)
        result_data = {
            'url': url,
            'error_message': content,
        }

        return render_template('index.html', **result_data)

    except AttributeError as e:
        content = "Error: Recipe data not available for this URL."
        result_data = {
            'url': url,
            'error_message': content,
        }

        return render_template('index.html', **result_data)

    return render_template('index.html', url=url, error_message="Failed to fetch content from the URL.")

if __name__ == '__main__':
    app.run(debug=True)
