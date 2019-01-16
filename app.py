import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np



dfTitanic=pd.read_csv('Titanic.csv')

dfOutCalc=pd.read_csv('TitanicOutCalc.csv')

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}


def getPlot(jenis, xCategory) :
    return [listGOFunc[jenis](
                x=dfTitanic[xCategory],
                y=dfTitanic['fare'],
                text=output_data_table['deck'],
                opacity=0.7,
                name='FARE',
                marker=dict(color='blue'),
                legendgroup='FARE'
            ),
            listGOFunc[jenis](
                x=dfTitanic[xCategory],
                y=dfTitanic['age'],
                text=output_data_table['deck'],
                opacity=0.7,
                name='AGE',
                marker=dict(color='orange'),
                legendgroup='AGE'
            )]

app = dash.Dash()
app.title = 'Ujian Titanic Dashboard'
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1', 
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        }, 
        children=[
            dcc.Tab(label='Tips Data Set', value='tab-1', children=[
                html.Div([
                    html.Table([
                            html.Tr([
                                    html.Td([
                                            html.P('Table :')
                                            ],style={'width': '150px'}),
                                    html.Td([
                                            dcc.Dropdown(
                                                            id='namaTable',
                                                            options=[{'label': 'Titanic', 'value': 'titanic'},
                                                                    {'label': 'Titanic Outlier Calculation', 'value': 'titanicoutcalc'},
                                                                    ],
                                                            value='titanic'
                                                        ) 
                                            ],style={'width': '350px'})
                                    ])
                            ]),
                    html.H1(id='judultabel',children='',style={'text-align':'center', 'color': '#008080'}),
                    html.P(id='row',children=''),
                    dcc.Graph(
                        id='isitab',
                        figure={
                            'data': []
                        }
                    )
                ],style={
                            'maxWidth': '1200px',
                            'margin': '0 auto',
                            'align':'center'
                        })
            ]),
        dcc.Tab(label='Categorical Plot', value='tab-2', children=[
                html.Div([
                    html.H1(['Categorical Plot Ujian Titanic'],style={'text-align':'center', 'color': '#008080'}),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Jenis : '),
                                dcc.Dropdown(
                                    id='jenisPlotCat',
                                    options=[{'label': 'Bar', 'value': 'bar'},
                                            {'label': 'Violin', 'value': 'violin'},
                                            {'label': 'Box', 'value': 'box'}],
                                    value='bar'
                                )
                            ]),
                            html.Td([
                                html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='plotCat',
                                    options=[{'label': 'SURVIVED', 'value': 'survived'},
                                            {'label': 'SEX', 'value': 'sex'},
                                            {'label': 'TICKET CLASS', 'value': 'class'},
                                            {'label': 'EMBARK TOWN', 'value': 'embark_town'},
                                            {'label': 'WHO', 'value': 'who'},
                                            {'label': 'OUTLIER', 'value': 'outlier'}
                                            ],
                                    value='survived'
                                )
                            ])
                        ])
                    ], style={ 'width' : '700px', 'margin': '0 auto'}),
                    dcc.Graph(
                        id='categoricalPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ])
        ])
  ],style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})

@app.callback(
    Output('judultabel', 'children'),
    [Input('namaTable','value')]
)
def update_judultable(namatable) :
    if namatable=='titanic':
        return 'Table Titanic'
    else : 
        return 'Table Titanic Out Calculation'
    
@app.callback(
    Output('row', 'children'),
    [Input('isitab','figure')]
)
def update_jumlahrow(namatable) :
    return 'Total Row : '+str(len(output_data_table))

@app.callback(
    Output('isitab', 'figure'),
    [Input('namaTable','value')]
)
def update_isitable(namatable) :
    global output_data_table
    if namatable=='titanic' : 
        output_data_table=dfTitanic
        widthtable=1000
    else : 
        output_data_table=dfOutCalc
        widthtable=600
    return {
        'data': [
            go.Table(
                    header=dict(values=['<b>'+col.upper()+'</b>' for col in output_data_table.columns],
                                fill = dict(color='#C2D4FF'),
                                align = ['left'] * 5
                                
                                ),
                    cells=dict(values=[output_data_table[col] for col in output_data_table.columns],
                               fill = dict(color='#F5F8FF'),
                               align = ['left'] * 5,
                               font = dict(color = 'black', size = 11)
                               )
                               
                            )
        ],
        'layout': go.Layout(
           margin={'l': 0, 'b': 10, 't': 10, 'r': 0},
            height=600, 
            width=widthtable
        )
    }

@app.callback(
Output('categoricalPlot', 'figure'),
[Input('jenisPlotCat', 'value'),
Input('plotCat', 'value')])
    
def update_category_graph(jenisCat, pCat):
    return {
            'data': getPlot(jenisCat,pCat),
            'layout': go.Layout(
                xaxis={'title': pCat.capitalize()}, yaxis={'title': 'FARE(US$) AGE(YEAR)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                
            )
    }
                    
if __name__ == '__main__':    
    app.run_server(debug=True,port=1995)

