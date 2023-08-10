import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('vgsales.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP])  # Apply Bootstrap theme

# Create options for the genre dropdown
genre_options = [{'label': genre, 'value': genre}
                 for genre in df['Genre'].unique()]

app.layout = dbc.Container([
    html.H1("Video Game Sales Analysis Dashboard", style={
        'text-align': 'center', 'color': 'blue', 'margin-bottom': '10px'
    }),

    dbc.Row([
        dbc.Col([
            html.Label("Select Genre:", style={'font-size': '18px'}),
            dcc.Dropdown(id='genre-dropdown', options=genre_options,
                         multi=False, value='Action', style={'font-size': '18px'}),
            html.Br(),
            html.Label("Select Year Range:", style={'font-size': '18px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                step=1,
                value=[df['Year'].min(), df['Year'].max()],
                marks={str(year): str(year) for year in df['Year'].unique()},
                tooltip={'placement': 'bottom', 'always_visible': True},
                updatemode='drag',  # Update values while dragging the slider
                vertical=False,  # Horizontal slider
            ),
        ]),
    ], justify="center"),  # Center align the row
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), md=12),  # Full width for bar chart
    ]),

    dbc.Row([
        # Half width for area plot and line plot
        dbc.Col(dcc.Graph(id='line-chart'), md=6),
        dbc.Col(dcc.Graph(id='area-chart'), md=6),
    ]),

    dbc.Row([
        # Half width for scatter plot and pie chart
        dbc.Col(dcc.Graph(id='scatter-plot'), md=6),
        dbc.Col(dcc.Graph(id='pie-chart'), md=6),
    ])

])


@app.callback(
    Output('bar-chart', 'figure'),
    Output('line-chart', 'figure'),
    Output('area-chart', 'figure'),
    Output('scatter-plot', 'figure'),
    Output('pie-chart', 'figure'),
    Input('genre-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_charts(selected_genre, selected_years):
    filtered_df = df[(df['Genre'] == selected_genre) & (
        df['Year'].between(selected_years[0], selected_years[1]))]

    bar_chart = px.bar(
        filtered_df,
        x='Platform',
        y='Global_Sales',
        title=f'Global Sales by Platform for {selected_genre}',
        labels={'Global_Sales': 'Sales in millions'}
    )

    area_chart = px.area(
        filtered_df.groupby('Year')['Global_Sales'].sum().reset_index(),
        x='Year',
        y='Global_Sales',
        title=f'Total Global Sales Over Years for {selected_genre}',
        labels={'Global_Sales': 'Total Sales in millions'}
    )

    line_chart = px.line(
        filtered_df.groupby('Year')['Global_Sales'].mean().reset_index(),
        x='Year',
        y='Global_Sales',
        title=f'Average Global Sales Per Year for {selected_genre}',
        labels={'Global_Sales': 'Average Sales in millions'}
    )

    scatter_plot = px.scatter(
        filtered_df,
        x='Year',
        y=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        title=f'Sales Comparison by Region for {selected_genre}',
        labels={'value': 'Sales in millions', 'variable': 'Region'}
    )

    sales_by_region = filtered_df[['NA_Sales',
                                   'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    pie_chart = px.pie(
        names=sales_by_region.index,
        values=sales_by_region.values,
        title=f'Sales Distribution by Region for {selected_genre}',
        labels={'value': 'Sales in millions'}
    )

    return bar_chart, line_chart, area_chart, scatter_plot, pie_chart


if __name__ == '__main__':
    app.run_server(debug=True)
