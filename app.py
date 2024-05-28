from flask import Flask, request, render_template, redirect, url_for, session
import altair as alt
from vega_datasets import data
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

        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
            y='Births:Q',
            tooltip=['Year', 'Births']
        ).properties(
            width=1000,
            height=400,
        ).interactive(bind_x=True, bind_y=True)

        # heatmap viz
        df['Decade'] = (df['Year'] // 10) * 10
        df['YearWithinDecade'] = df['Year'] % 10

        min_births = df['Births'].min()
        max_births = df['Births'].max()
        threshold = df['Births'].quantile(0.85)

        select_checkbox = alt.param(
            bind=alt.binding_checkbox(name="Show grid and text"),
        )

        heatmap = alt.Chart(df).mark_rect().encode(
            alt.X('YearWithinDecade:O', title='Year Within Decade',
                  axis=alt.Axis(labelAngle=0)),
            alt.Y('Decade:O', title='Decade'),
            alt.Color('Births:Q', scale=alt.Scale(
                scheme='greenblue'), title='Number of Births', legend=alt.Legend(title="Number of Births", values=[min_births, max_births])),
            tooltip=['Year:O', 'Births:Q'],
            stroke=alt.condition(
                select_checkbox, alt.value('black'), alt.value(None))
        ).properties(
            width=400,
            height=300,
            title='Heatmap of Births by Year Within Each Decade'
        )

        text = alt.Chart(df).mark_text(align='center').encode(
            x='YearWithinDecade:O',
            y='Decade:O',
            text=alt.condition(select_checkbox, 'Births:Q',
                               alt.value(''), format=','),
            # change text color to be more readable against darker background colors
            color=alt.condition(alt.datum.Births >= threshold,
                                alt.value("white"),
                                alt.value("black"))
        ).add_params(
            select_checkbox
        )

        chart2 = heatmap + text

        chart_json = chart.to_json()
        chart_json2 = chart2.to_json()

        return render_template('interactive_chart.html', chart_json=chart_json, chart_json2=chart_json2)

    return render_template('interactive_chart.html', chart_json="{}")


@app.route('/random_name', methods=['GET', 'POST'])
def random_name():
    """
    Route to generate random names.

    Output: 
    - Rendered 'generate_form.html' template with a list of generated names when POST method is used.
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

        cur_text = names.name_information(name, gender)

        return render_template('name_info.html', texts=cur_text)
    return render_template('name_info.html')


if __name__ == "__main__":
    app.run(debug=True)
