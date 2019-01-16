import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
from sqlalchemy import create_engine


engine = create_engine("mysql+mysqlconnector://root:123456@localhost/titanic?host=localhost?port=3306")
conn = engine.connect()

results1 = conn.execute('select * from titanic').fetchall()
dfTitanic= pd.DataFrame(results1)
dfTitanic.columns = results1[0].keys()


results2 = conn.execute('select * from titanicoutcalc').fetchall()
dfOutCalc= pd.DataFrame(results2)
dfOutCalc.columns = results2[0].keys()



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
                                                            id='ddlnamatable',
                                                            options=[{'label': 'Titanic', 'value': 'titanic'},
                                                                    {'label': 'Titanic Outlier Calculation', 'value': 'titanicoutcalc'},
                                                                    ],
                                                            value='titanic'
                                                        ) 
                                            ],style={'width': '350px'})
                                    ])
                            ]),
                    html.H1(id='judultabel',children='',style={'text-align':'center', 'color': '#008080'}),
                    html.P(id='jumlahrow',children=''),
                    dcc.Graph(
                        id='isitable',
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
                                    id='ddl-jenis-plot-category',
                                    options=[{'label': 'Bar', 'value': 'bar'},
                                            {'label': 'Violin', 'value': 'violin'},
                                            {'label': 'Box', 'value': 'box'}],
                                    value='bar'
                                )
                            ]),
                            html.Td([
                                html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='ddl-x-plot-category',
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
            ])######################################  TAB1 ##############################################3
        ])
  ],style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})

@app.callback(
    Output('judultabel', 'children'),
    [Input('ddlnamatable','value')]
)
def update_judultable(namatable) :
    if namatable=='titanic':
        return 'Table Titanic'
    else : 
        return 'Table Titanicoutcalc'
    
@app.callback(
    Output('jumlahrow', 'children'),
    [Input('isitable','figure')]
)
def update_jumlahrow(namatable) :
    return 'JUMLAH ROW '+str(len(output_data_table))

@app.callback(
    Output('isitable', 'figure'),
    [Input('ddlnamatable','value')]
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
                                align = 'center'
                                
                                ),
                    cells=dict(values=[output_data_table[col] for col in output_data_table.columns],
                               fill = dict(color='#F5F8FF'),
                               align = 'center',
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
[Input('ddl-jenis-plot-category', 'value'),
Input('ddl-x-plot-category', 'value')])
    
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
            'data': getPlot(ddljeniscategory,ddlxcategory),
            'layout': go.Layout(
                xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'FARE(US$) AGE(YEAR)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    }
                    
if __name__ == '__main__':    
    app.run_server(debug=True,port=1995)