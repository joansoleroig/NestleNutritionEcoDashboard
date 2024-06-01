import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pandas.api.types import CategoricalDtype

# Load your dataset
df = pd.read_csv('nestle_es_cleaned.csv')

# Filter out 'not-applicable' and 'unknown' NutriScore and EcoScore grades
df = df[~df['off:nutriscore_grade'].isin(['not-applicable', 'unknown'])]
df = df[~df['off:ecoscore_grade'].isin(['not-applicable', 'unknown'])]

# Define the categorical order for NutriScore and EcoScore grades
nutriscore_order = CategoricalDtype(categories=['a', 'b', 'c', 'd', 'e'], ordered=True)
ecoscore_order = CategoricalDtype(categories=['a', 'b', 'c', 'd', 'e'], ordered=True)
df['off:nutriscore_grade'] = df['off:nutriscore_grade'].astype(nutriscore_order)
df['off:ecoscore_grade'] = df['off:ecoscore_grade'].astype(ecoscore_order)

# Rename columns for better hover text
df.rename(columns={
    'off:nutriscore_grade': 'Nutriscore grade',
    'salt_value': 'Salt Value [g]',
    'sugars_value': 'Sugars Value [g]',
    'fat_value': 'Fat Value [g]',
    'saturated-fat_value': 'Saturated Fat Value [g]'
}, inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='selected-grade-store', data=None),  # Store for the selected NutriScore grade
    dcc.Store(id='selected-ecoscore-store', data=None),  # Store for the selected EcoScore grade
    
    html.Div([
        html.Img(src='/assets/nestle.png', style={'width': '100px', 'float': 'right'}),
        html.Img(src='/assets/esade.png', style={'width': '100px', 'float': 'left'}),
        html.H1("Nestlé's Products Analysis Dashboard", style={'textAlign': 'center'}),
    ], style={'height': '100px', 'backgroundColor': '#f0f8ff', 'padding': '20px'}),
    
    dcc.Tabs([
        dcc.Tab(label='Nutritional Analysis', children=[
            # Scatter plot for clustering by NutriScore grade
            html.Div([
                dcc.Graph(id='clustering-scatterplot')
            ]),
            
            # Histogram for NutriScore Grade
            html.Div([
                dcc.Graph(id='nutriscore-histogram'),
            ], style={'display': 'inline-block', 'width': '48%'}),
            
            # Boxplot for fat values based on selected NutriScore Grade
            html.Div([
                dcc.Graph(id='fat-boxplot'),
            ], style={'display': 'inline-block', 'width': '48%'}),
            
            # Reset button
            html.Div([
                html.Button("Do Not Select Any", id='reset-button', n_clicks=0, 
                            style={
                                'background-color': '#4CAF50',  # Button color
                                'color': 'white',  # Text color
                                'padding': '14px 20px',  # Padding
                                'margin': '8px 0',  # Margin
                                'border': 'none',  # No border
                                'cursor': 'pointer',  # Cursor style
                                'width': '20%',  # Button width
                                'borderRadius': '12px',  # Button corners
                                'textAlign': 'center'  # Center the text
                            })
            ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'}),
        ]),
        dcc.Tab(label='Eco Analysis', children=[
            # Histogram for Eco-Score Grade
            html.Div([
                dcc.Graph(id='ecoscore-histogram'),
            ], style={'display': 'inline-block', 'width': '48%'}),
            
            # Radar chart for packaging materials and Eco-Score
            html.Div([
                dcc.Graph(id='packaging-radar'),
            ], style={'display': 'inline-block', 'width': '48%'}),
            
            # Reset button for Eco Analysis
            html.Div([
                html.Button("Do Not Select Any", id='reset-eco-button', n_clicks=0, 
                            style={
                                'background-color': '#4CAF50',  # Button color
                                'color': 'white',  # Text color
                                'padding': '14px 20px',  # Padding
                                'margin': '8px 0',  # Margin
                                'border': 'none',  # No border
                                'cursor': 'pointer',  # Cursor style
                                'width': '20%',  # Button width
                                'borderRadius': '12px',  # Button corners
                                'textAlign': 'center'  # Center the text
                            })
            ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'}),
        ])
    ])
])

@app.callback(
    Output('selected-grade-store', 'data'),
    Output('selected-ecoscore-store', 'data'),
    Input('clustering-scatterplot', 'clickData'),
    Input('nutriscore-histogram', 'clickData'),
    Input('ecoscore-histogram', 'clickData'),
    Input('reset-button', 'n_clicks'),
    Input('reset-eco-button', 'n_clicks'),
    State('selected-grade-store', 'data'),
    State('selected-ecoscore-store', 'data')
)
def update_selected_grade(scatter_clickData, histogram_clickData, ecoscore_clickData, n_clicks, n_clicks_eco, selected_grade, selected_ecoscore):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'clustering-scatterplot' and scatter_clickData:
            selected_grade = scatter_clickData['points'][0]['customdata'][0]
            selected_ecoscore = None
        elif prop_id == 'nutriscore-histogram' and histogram_clickData:
            selected_grade = histogram_clickData['points'][0]['x']
            selected_ecoscore = None
        elif prop_id == 'ecoscore-histogram' and ecoscore_clickData:
            selected_ecoscore = ecoscore_clickData['points'][0]['x']
            selected_grade = None
        elif prop_id in ['reset-button', 'reset-eco-button']:
            selected_grade = None
            selected_ecoscore = None
    
    return selected_grade, selected_ecoscore

@app.callback(
    Output('clustering-scatterplot', 'figure'),
    Output('nutriscore-histogram', 'figure'),
    Output('fat-boxplot', 'figure'),
    Output('ecoscore-histogram', 'figure'),
    Output('packaging-radar', 'figure'),
    Input('selected-grade-store', 'data'),
    Input('selected-ecoscore-store', 'data')
)
def update_graphs(selected_grade, selected_ecoscore):
    # Filter dataframe based on selected NutriScore grade
    if selected_grade:
        filtered_df = df[df['Nutriscore grade'] == selected_grade]
    else:
        filtered_df = df

    # Filter dataframe based on selected EcoScore grade
    if selected_ecoscore:
        filtered_df_eco = df[df['off:ecoscore_grade'] == selected_ecoscore]
    else:
        filtered_df_eco = df

    # Generate scatter plot for clustering
    scatter_fig = px.scatter(
        df, 
        x='Salt Value [g]', 
        y='Sugars Value [g]', 
        color='Nutriscore grade',
        title='Clustering of Food Items by NutriScore Grade',
        labels={'Nutriscore grade': 'Nutriscore Grade', 'Salt Value [g]': 'Salt Value', 'Sugars Value [g]': 'Sugars Value'},
        custom_data=['Nutriscore grade', 'product_name'],
        hover_data={'Nutriscore grade': True, 'Salt Value [g]': True, 'Sugars Value [g]': True, 'product_name': False}
    )

    scatter_fig.update_traces(hovertemplate=
        '<b>Nutriscore Grade:</b> %{customdata[0]}<br>' +
        '<b>Salt Value [g]:</b> %{x}<br>' +
        '<b>Sugars Value [g]:</b> %{y}<br>' +
        '<b>Product:</b> %{customdata[1]}<br>'
    )

    if selected_grade:
        scatter_fig.for_each_trace(lambda trace: trace.update(marker=dict(opacity=0.4)) if trace.name != selected_grade else trace.update(marker=dict(opacity=1, size=10)))

    scatter_fig.update_layout(title={'x': 0.5})
    scatter_fig.update_xaxes(title_text='Salt Value [g]')
    scatter_fig.update_yaxes(title_text='Sugars Value [g]')
    scatter_fig.update_layout(legend_title_text='NutriScore Grade')

    # Generate NutriScore histogram
    hist_fig = px.histogram(
        df, 
        x='Nutriscore grade', 
        title='NutriScore Grade Distribution', 
        color='Nutriscore grade'
    )
    
    hist_fig.update_traces(hovertemplate=
        '<b>Nutriscore Grade:</b> %{x}<br>' +
        '<b>Count:</b> %{y}<br>'
    )
    
    # Ensure that each trace is correctly named by the NutriScore grade
    nutriscore_grades = df['Nutriscore grade'].unique()
    for trace, grade in zip(hist_fig.data, nutriscore_grades):
        trace.name = grade

    if selected_grade:
        for trace in hist_fig.data:
            trace.marker.opacity = 0.2
            if trace.name == selected_grade:
                trace.marker.opacity = 1
    else:
        for trace in hist_fig.data:
            trace.marker.opacity = 1

    hist_fig.update_layout(title={'x': 0.5})
    hist_fig.update_xaxes(title_text='Nutriscore Grade', categoryorder='array', categoryarray=['a', 'b', 'c', 'd', 'e']) 
    hist_fig.update_yaxes(title_text='Count')   
    hist_fig.update_layout(legend_title_text='Nutriscore Grade')

    # Generate boxplot for fat values
    box_fig = px.box(filtered_df, y=['Fat Value [g]', 'Saturated Fat Value [g]'], 
                     title=f'Fat and Saturated Fat Values for Nutriscore Grade {selected_grade if selected_grade else "All"}')

    box_fig.update_layout(title={'x': 0.5})
    box_fig.update_xaxes(title_text='Fat Type')
    box_fig.update_yaxes(title_text='Fat Value [g]')

    # Generate Eco-Score histogram
    ecoscore_fig = px.histogram(
        df[df['off:ecoscore_grade'].notna() & ~df['off:ecoscore_grade'].isin(['not-applicable', 'unknown'])], 
        x='off:ecoscore_grade', 
        title='Eco-Score Grade Distribution', 
        color='off:ecoscore_grade'
    )
    
    ecoscore_fig.update_traces(hovertemplate=
        '<b>Eco-Score Grade:</b> %{x}<br>' +
        '<b>Count:</b> %{y}<br>'
    )
    
    # Ensure that each trace is correctly named by the Eco-Score grade
    ecoscore_grades = df['off:ecoscore_grade'].unique()
    for trace, grade in zip(ecoscore_fig.data, ecoscore_grades):
        trace.name = grade

    if selected_ecoscore:
        for trace in ecoscore_fig.data:
            trace.marker.opacity = 0.2
            if trace.name == selected_ecoscore:
                trace.marker.opacity = 1
    else:
        for trace in ecoscore_fig.data:
            trace.marker.opacity = 1

    ecoscore_fig.update_layout(title={'x': 0.5})
    ecoscore_fig.update_xaxes(title_text='Eco-Score Grade', categoryorder='array', categoryarray=['a', 'b', 'c', 'd', 'e']) 
    ecoscore_fig.update_yaxes(title_text='Count')   
    ecoscore_fig.update_layout(legend_title_text='Eco-Score Grade')

    # Generate radar chart for packaging materials and Eco-Score
    # Group by EcoScore grade and get the count of unique packaging materials starting with 'en'
    packaging_data = df[df['off:ecoscore_grade'].notna() & ~df['off:ecoscore_grade'].isin(['not-applicable', 'unknown'])]
    packaging_data = packaging_data[packaging_data['packaging_1_material'].str.startswith('en', na=False)]

    # Strip the starting 'en: ' from all the names in the packaging type
    packaging_data['packaging_1_material'] = packaging_data['packaging_1_material'].str.replace('^en:\s*', '', regex=True).str.capitalize()

    packaging_data = packaging_data.groupby(['off:ecoscore_grade', 'packaging_1_material']).size().reset_index(name='Count')

    # Define colors for EcoScore grades
    ecoscore_colors = {grade: trace.marker.color for trace, grade in zip(ecoscore_fig.data, ecoscore_grades)}

    # Create a radar chart figure
    radar_fig = go.Figure()

    # Iterate through each unique EcoScore grade and add a trace to the radar chart
    for ecoscore_grade in packaging_data['off:ecoscore_grade'].unique():
        subset = packaging_data[packaging_data['off:ecoscore_grade'] == ecoscore_grade]
        radar_fig.add_trace(go.Scatterpolar(
            r=subset['Count'],
            theta=subset['packaging_1_material'],
            fill='toself',
            name=ecoscore_grade,
            line_color=ecoscore_colors[ecoscore_grade],
            opacity=0.2 if selected_ecoscore and ecoscore_grade != selected_ecoscore else 1
        ))

    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, packaging_data['Count'].max()]
            )
        ),
        title='Packaging Materials by Eco-Score',
        showlegend=True,
        title_x=0.5
    )

    return scatter_fig, hist_fig, box_fig, ecoscore_fig, radar_fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)

