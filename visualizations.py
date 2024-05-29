"""
Create interactive data visualizations using name data. 
"""
import altair as alt


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
        width=1000,
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
        bind=alt.binding_checkbox(name="Show grid and text"),
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
