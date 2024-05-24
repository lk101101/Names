from flask import Flask, request, render_template
import names
app = Flask(__name__)


@app.route('/')
def home():
    """
    Serve the home page. 
    """
    return render_template('index.html')


@app.route('/vizs', methods=['GET', 'POST'])
def get_visualizations():
    """
    Route to generate visualizations. 

    Output: 
    - Rendered 'generate_form.html' template with a list of generated names when POST method is used.
    - Rendered 'generate_form.html' template with form when GET method is used.
    """
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        year = request.form['year']
        # plot_url = names.popularity(name, gender, year)
        return render_template('visualizations.html', plot_url=plot_url)
    return render_template('visualizations_form.html')


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
        print(cur_text)

        return render_template('name_info.html', texts=cur_text)
    return render_template('name_info.html')


if __name__ == '__main__':
    app.run(debug=True)
