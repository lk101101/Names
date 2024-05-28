from flask import Flask, request, render_template, redirect, url_for, session
import altair as alt
import names
import visualizations

app = Flask(__name__)


@app.route('/')
def home():
    """
    Serve the home page. 
    """
    return render_template('index.html')


@app.route('/interactive_chart', methods=['GET', 'POST'])
def interactive_chart():
    """ 
    TODO: add docstring
    """

    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        gender = request.form.get('gender', default='').lower()
        start_year = int(request.form.get('start_year'))
        end_year = int(request.form.get('end_year'))

        df = names.popularity(name, gender, start_year, end_year)

        chart = visualizations.simple_line_chart(df)
        chart2 = visualizations.popularity_heatmap(df)

        chart_json = chart.to_json()
        chart_json2 = chart2.to_json()

        return render_template('interactive_chart.html', chart_json=chart_json, chart_json2=chart_json2)

    return render_template('interactive_chart.html', chart_json="{}")


@app.route('/random_name', methods=['GET', 'POST'])
def random_name():
    """
    Route to generate random names.

    Output: 
    - Rendered 'generate_form.html' template with list of generated names when POST method is used.
    - Rendered 'generate_form.html' template with form when GET method is used.
    """
    if request.method == 'POST':
        gender = request.form.get('gender', default='')
        num_names = int(request.form.get('num_names', default=1))
        include_surname = request.form.get('surname') == 'yes'
        cur_names = [names.random_name(gender, include_surname)
                     for _ in range(num_names)]
        return render_template('generate_form.html', names=cur_names)
    return render_template('generate_form.html')


@app.route('/name_information', methods=['GET', 'POST'])
def name_information():
    """
    Route to retrieve information about a name. 

    Output:
    - Rendered 'name_info.html' template with name information when POST method is used.
    - Rendered 'name_info.html' template with form when GET method is used.
    """
    if request.method == 'POST':
        name = request.form.get('name', '')
        gender = request.form.get('gender', '')

        # TODO: fix formatting
        cur_text = names.name_information(name, gender)

        return render_template('name_info.html', texts=cur_text)
    return render_template('name_info.html')


if __name__ == "__main__":
    app.run(debug=True)
