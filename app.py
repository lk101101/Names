""" 
Contains routes for Flask app.

Routes:
- /: home page
- /data_visualizations: interactive data visualizations based on name popularity
- /random_name: generates random names based on user input (gender, number of names, surname)
- /name_information: provides name information and world map visualization displaying potential countries of origin

"""
from flask import Flask, request, render_template
import names
import visualizations

app = Flask(__name__)


@app.route('/')
def home():
    """
    Serve the home page.
    """
    return render_template('index.html')


@app.route('/data_visualizations', methods=['GET', 'POST'])
def data_visualizations():
    """
    Route to create data visualizations.

    Output:
    - Rendered 'data_visualizations.html' template
    displaying interactive data visualizations.
    """

    template_data = {
        "chart_json": "{}",
        "chart_json2": "{}",
    }
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender', default='').lower()
        start_year = int(request.form.get('start_year'))
        end_year = int(request.form.get('end_year'))

        df = names.popularity(name, gender, start_year, end_year)

        line_chart = visualizations.simple_line_chart(df)
        heatmap = visualizations.popularity_heatmap(df)

        template_data["chart_json"] = line_chart.to_json()
        template_data["chart_json2"] = heatmap.to_json()

    return render_template('data_visualizations.html', **template_data)


@app.route('/random_name', methods=['GET', 'POST'])
def random_name():
    """
    Route to generate random names.

    Output:
    - Rendered 'generate_form.html' template with a list of generated names (POST)
    - Rendered 'generate_form.html' template for name generation form (GET)
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
    - Rendered 'name_info.html' template with:
          - 'texts': information about the name scraped from NameBerry
          - 'world_map_json': world map visualization displaying five most probable countries of origin for the name
          - 'spotify_data': first song title matching name from Spotify API

    """
    template_data = {
        "texts": "",
        # ** Uncomment for Spotify API data
        # "spotify_data": {},
        "world_map_json": "{}",
    }

    if request.method == 'POST':
        name = request.form.get('name', '')
        gender = request.form.get('gender', '')

        # TODO: fix formatting
        template_data["texts"] = names.name_information(name, gender)
        # ** Uncomment to display song matching name from Spotify API
        # template_data["spotify_data"] = names.spotify_track(name)
        world_map = visualizations.create_nationalize_map(name)
        template_data["world_map_json"] = world_map.to_json()
    return render_template('name_info.html', **template_data)


if __name__ == "__main__":
    app.run(debug=True)
