"""
Create interactive data visualizations using name data.
"""
import altair as alt
from vega_datasets import data
import pandas as pd
import pycountry
import names


def get_country_id(country_name):
    """
    Get the numeric country code for a given country name
    using ISO 3166-1 alpha-2 codes.

    input:
        country_name: string
    output:
        numeric country code or None: string
    """
    try:
        return pycountry.countries.get(alpha_2=country_name).numeric
    except LookupError:
        return None


def create_nationalize_map(name):
    """
    Create a world map visualization that shows the predicted countries of origin
    of a given name.

    input:
        name: string
    output:
        choropleth world map showcasing the five most probable countries of origin for a given name
    """
    predictions = names.nationalize(name)

    for prediction in predictions:
        country_id = get_country_id(prediction['country_id'])
        if country_id:
            prediction['id'] = int(country_id)

    df = pd.DataFrame([p for p in predictions if 'id' in p])

    countries_geojson = alt.topo_feature(data.world_110m.url, 'countries')

    # world map background in grey
    world_map = alt.Chart(countries_geojson).mark_geoshape(
        fill='lightgrey',
    )
    # chart for colored countries
    probability_layer = alt.Chart(countries_geojson).mark_geoshape(
        stroke='black'
    ).encode(
        color=alt.Color('probability:Q',
                        legend=alt.Legend(title="Probability", format='%')),
        tooltip=[
            alt.Tooltip('country_id:N', title='Country'),
            alt.Tooltip('probability:Q', title='Probability', format='.2%')
        ]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data=df, key='id', fields=[
                             'country_id', 'probability'])
    ).project(
        'equirectangular'
    ).properties(
        width=1000,
        height=400
    )

    return world_map + probability_layer


def simple_line_chart(df):
    """
    Create a line chart from a Pandas DataFrame that visualizes the frequency of a name over time.

    input:
        Pandas DataFrame containing years and associated number of births
        for a user-specified name
    output:
        simple line chart displaying the number of births over the range of years
    """
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Year:Q',
                axis=alt.Axis(format='d', title='Year')),
        y=alt.Y('Births:Q', title='Number of Births'),
        tooltip=['Year:Q', 'Births:Q']
    ).properties(
        width=800,
        height=400
    ).interactive(bind_x=True)
    return chart


def popularity_heatmap(df):
    """
    Create a heatmap from a Pandas DataFrame that visualizes the frequency of a name over time.

    input:
        Pandas DataFrame containing years and associated number of births
        for a user-specified name
    output:
        heatmap displaying the number of births over the range of years
        binned by decade
    """
    df['Decade'] = (df['Year'] // 10) * 10
    df['YearWithinDecade'] = df['Year'] % 10

    min_births = df['Births'].min()
    max_births = df['Births'].max()
    threshold = df['Births'].quantile(0.85)

    select_checkbox = alt.param(
        bind=alt.binding_checkbox(name="Show grid and labels"),
    )

    heatmap = alt.Chart(df).mark_rect().encode(
        alt.X('YearWithinDecade:O', title='Year Within Decade',
              axis=alt.Axis(labelAngle=0)),
        alt.Y('Decade:O', title='Decade'),
        alt.Color('Births:Q', scale=alt.Scale(
            scheme='greenblue'), title='Number of Births',
            legend=alt.Legend(title="Number of Births",
                              values=[min_births, max_births])),
        tooltip=['Year:O', 'Births:Q'],
        # add grid outlines if toggled on
        stroke=alt.condition(
            select_checkbox, alt.value('black'), alt.value(None))
    ).properties(
        width=500,
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

    heatmap += text
    return heatmap
