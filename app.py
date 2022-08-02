import dash
import dash_auth
from dash import dcc
from dash import html
import plotly.graph_objects as go

# Store array data with numpy
import numpy as np

title = 'Main Source for News'
labels = ['Television', 'Newspaper', 'Internet', 'Radio']
colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

x_data = np.vstack((np.arange(2001, 2014),)*4)

y_data = np.array([
    [74, 82, 80, 74, 73, 72, 74, 70, 70, 66, 66, 69],
    [45, 42, 50, 46, 36, 36, 34, 35, 32, 31, 31, 28],
    [13, 14, 20, 24, 20, 24, 24, 40, 35, 41, 43, 50],
    [18, 21, 18, 21, 16, 14, 13, 18, 17, 16, 19, 23],
])

fig = go.Figure()


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Mickey': 'Mouse', 'Donald': 'Duck', 'Carlos': 'Santana'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Authorization Application'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('Welcome, if you are authorized!'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [1, 2, 3, 4]],
        value=1
    ),
    dcc.Graph(id='graph'),
    html.A('Code on Github', href='https://github.com/ksebastian/208-authentication-example'),
    html.Br(),
    html.A("Data Source", href='https://dash.plotly.com/authentication'),
], className='container')


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown_value):
    fig.data = []
    annotations = []

    fig.add_trace(go.Scatter(x=x_data[dropdown_value-1], y=y_data[dropdown_value-1], mode='lines',
                             name=labels[dropdown_value-1],
                             line=dict(color=colors[dropdown_value-1], width=line_size[dropdown_value-1]),
                             connectgaps=True,
                             ))

    fig.add_trace(go.Scatter(
        x=[x_data[dropdown_value-1][0], x_data[dropdown_value-1][-1]],
        y=[y_data[dropdown_value-1][0], y_data[dropdown_value-1][-1]],
        mode='markers',
        marker=dict(color=colors[dropdown_value-1], size=mode_size[dropdown_value-1])
    ))

    annotations.append(dict(xref='paper', x=0.05, y=y_data[0],
                            xanchor='right', yanchor='middle',
                            text=labels[dropdown_value-1],
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
