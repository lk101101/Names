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
        # Collect form data
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
    - Rendered 'generate_form.html' template with
    list of generated names (POST)
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
    - Rendered 'name_info.html' template with name information (POST)
    """
    template_data = {
        "texts": "",
        "world_map_json": "{}",
    }

    if request.method == 'POST':
        name = request.form.get('name', '')
        gender = request.form.get('gender', '')

        # TODO: fix formatting
        template_data["texts"] = names.name_information(name, gender)
        world_map = visualizations.create_nationalize_map(name)

        template_data["world_map_json"] = world_map.to_json()
    return render_template('name_info.html', **template_data)


if __name__ == "__main__":
    app.run(debug=True)
