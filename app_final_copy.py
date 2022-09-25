from turtle import bgcolor
import dash
from dash import dcc,html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash_table import DataTable
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table

# Dataset Processing

# importing data
data = pd.read_csv("archive/Demo.csv")


df=data.copy()
# variables for the analysis
skill_player = ["Memory", "Accuracy", "Latency", "Size","Debit"]
info_player = [
    "Model",
    "Accuracy",
    "Latency",
    "Size",
    "Debit",
]
labels_table = ["Model", "Accuracy (%)", "Latency (ms)", "Number of parmaters (k)", "Speed (img/s)"]

"""
skills1 = [
    "skill_curve",
    "skill_dribbling",
    "skill_fk_accuracy",
    "skill_ball_control",
    "skill_long_passing",
]
"""
model1 = "Hyt-NAS-bl"
model2 = "MobileViT-S"


###################################################   Interactive Components   #########################################
# choice of the players

players_options_over_25 = []
for i in df.index:
    players_options_over_25.append(
        {"label": df["Model"][i], "value": df["Model"][i]}
    )

players_options_under_25 = []
for i in df.index:
    players_options_under_25.append(
        {"label": df["Model"][i], "value": df["Model"][i]}
    )

dropdown_player_over_25 = dcc.Dropdown(
    id="model1",
    options=players_options_over_25,
    value="Hyt-NAS-bl",
    style = {"background-color":"white","color":"black"}
)

dropdown_player_under_25 = dcc.Dropdown(
    id="model2", options=players_options_under_25, value="MobileViT-S",style = {"background-color":"white","color":"black"}
)

dashtable_1 = dash_table.DataTable(
    id="table1",
    columns=[
        {"name": col, "id": info_player[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=df[df["Model"] ==model1].to_dict("records"),
    style_cell={'whiteSpace': 'normal','height': 'auto','minWidth': '120px', 'width': '120px', 'maxWidth': '120px','overflow': 'hidden',
        'textOverflow': 'ellipsis',"textAlign": "center", "font_size": "14px","backgroundColor": "rgb(17, 17, 17)","padding":"Opx" },
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(17, 17, 17)", "fontWeight": "bold","font_size":"14px"}
)


dashtable_2 = dash_table.DataTable(
    id="table2",
    # columns=[{"name": i, "id": i} for i in info_player[::-1]],
    columns=[
        {"name": col, "id": info_player[idx]}
        for (idx, col) in enumerate(labels_table)
    ],
    data=df[df["Model"] == model2].to_dict("records"),
    style_cell={'whiteSpace': 'normal','height': 'auto','minWidth': '120px', 'width': '120px', 'maxWidth': '120px','overflow': 'hidden',
        'textOverflow': 'ellipsis',"textAlign": "center", "font_size": "14px","backgroundColor": "rgb(17, 17, 17)","padding":"Opx" },
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(17, 17, 17)", "fontWeight": "bold","font_size":"14px"}
)



################Components##############################################

options = [
    {"label": "Accuracy", "value": "Accuracy"},
    {"label": "Speed(FPS)", "value": "Debit"},
    {"label": "Value", "value": "value_eur"},
    {"label": "Wage", "value": "wage_eur"},
    {"label": "Height", "value": "height_cm"},
    {"label": "Weight", "value": "weight_kg"},
    {"label": "Pace", "value": "pace"},
    {"label": "Shooting", "value": "shooting"},
    {"label": "Passing", "value": "passing"},
    {"label": "Dribbling", "value": "dribbling"},
    {"label": "Defending", "value": "defending"},
    {"label": "Physic", "value": "physic"},
]

value_x = options




########Dash App Layout##########################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    #dbc.Col(
                        #html.Img(
                         #   src=app.get_asset_url("logo.png"), height="200px"
                        #),
                        #width=3,
                    #),
                    dbc.Col(
                        [
                            html.Label("Model comparaison", id="label1"),
                            html.Label(
                                "Explore the differences between Models in terms of performance measures",
                                className="label2",
                            ),
                            html.Br(),
                            html.Label(
                                "",
                                className="label2",
                                style={"margin-bottom": ".34rem"},
                            ),
                        ],
                        width=8,
                    ),
                ],
                align="between"
                # no_gutters=True,
            ),
        ),
    ],
)

controls_player_1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose a first Model:"),
                html.Br(),
                dropdown_player_over_25,
            ],className="main"
        ),
    ],
    
    body=True,
    className="controls_players",
)

controls_player_2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose a second model to compare to:"),
                html.Br(),
                dropdown_player_under_25,
            ],className="main"
        ),
    ],
    body=True,
    className="controls_players",
)

cards_1 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Size Ratio", className="card-title1"),
                    html.Div(id="P_position1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Latency Ratio", className="card-title1"),
                    html.Div(id="P_value1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Mem Ratio", className="card-title1"),
                    html.Div(id="P_skill1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Accuracy Diff", className="card-title1"),
                    html.Div(id="P_foot1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)
cards_2 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Accuracy Diff", className="card-title2"),
                    html.Div(id="P_foot2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Mem_ratio", className="card-title2"),
                    html.Div(id="P_skill2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Latency Ratio", className="card-title2"),
                    html.Div(id="P_value2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Size Ratio", className="card-title2"),
                    html.Div(id="P_position2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)
cards_3 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Speed(FPS)", className="card-title1"),
                    dcc.Graph(id="graph_example_1"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)


cards_4 = dbc.CardDeck(
    [
        
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Speed(FPS)", className="card-title2"),
                    dcc.Graph(id="graph_example_2"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)


tab1_content = (
    html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Model Comparison",className="main",),
                        html.Hr(className="main",),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_1),
                                        dbc.Row(
                                            html.Img(
                                                src=app.get_asset_url("player_1.png"),
                                                className="playerImg",
                                            )
                                        ),
                                    ],
                                    sm=4,
                                ),
                                dbc.Col(
                                    dcc.Graph(id="graph_example"), sm=4, align="center"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_2),
                                        dbc.Row(
                                            html.Img(
                                                src=app.get_asset_url("player_1.png"),
                                                className="playerImg",
                                            )
                                        ),
                                    ],
                                    className="main",
                                    sm=4,
                                ),
                            ],
                            justify="between",
                            className="main",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dashtable_1,
                                        html.Br(),
                                        cards_1,
                                        html.Br(),
                                        cards_3,
                                    ],
                                    sm=5,align="left"
                                ),
                                dbc.Col(html.Progress(id="progress_bar"),align="center",sm=2,style={"visibility" : 'hidden'}),
                                dbc.Col(
                                    [
                                        dashtable_2,
                                        html.Br(),
                                        cards_2,
                                        html.Br(),
                                        cards_4,
                                    ],
                                    sm=5,align="right"
                                ),
                            ],
                            className="main",
                        ),
                    ]
                
                ,),className="main"
            )
        ]
    ,className="main"),
)




app.layout = dbc.Container(
    [
        # html.H1("Fifa Players Analysis"),
        navbar,
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Models Comparison")
            ],className="main",
        ),
    ],
    fluid=True,
)


# ----------------Callbacks for 1st tab, clubs analysis----------------#

"""
       
        Output("graph_example_1", "figure"),
        Output("graph_example_3", "figure"),
        
        Output("graph_example_4", "figure"),
        Output("P_position1", "children"),
        Output("P_value1", "children"),
        Output("P_skill1", "children"),
        Output("P_foot1", "children"),
        Output("P_position2", "children"),
        Output("P_value2", "children"),
        Output("P_skill2", "children"),
        Output("P_foot2", "children"),
"""

@app.callback(
    [
        Output("graph_example", "figure"),
        Output("table1", "data"),
        Output("graph_example_1", "figure"),
        Output("table2", "data"),
        Output("graph_example_2", "figure"),
        Output("P_position1", "children"),
        Output("P_value1", "children"),
        Output("P_skill1", "children"),
        Output("P_foot1", "children"),
        Output("P_position2", "children"),
        Output("P_value2", "children"),
        Output("P_skill2", "children"),
        Output("P_foot2", "children"),

    ],
    [Input("model1", "value"), Input("model2", "value")],
)

###############################################   radar plot   #####################################################


def tab_1_function(model1, model2):

    # scatterpolar
    min_df=np.array([0,70,0,0,0])
    max_df=np.array([10000,100,200,3000,60])
    df1_for_plot = pd.DataFrame(df[df["Model"] == model1][skill_player].iloc[0])
    df1_for_plot.columns = ["score"]
    df2_for_plot = pd.DataFrame(df[df["Model"] == model2][skill_player].iloc[0])
    df2_for_plot.columns = ["score"]
    list_scores = [
        df1_for_plot.index[i].capitalize() + " = " + str(df1_for_plot["score"][i])
        for i in range(len(df1_for_plot))
    ]
    text_scores_1 = model1
    for i in list_scores:
        text_scores_1 += "<br>" + i

    list_scores = [
        df2_for_plot.index[i].capitalize() + " = " + str(df2_for_plot["score"][i])
        for i in range(len(df2_for_plot))
    ]
    text_scores_2 = model2
    for i in list_scores:
        text_scores_2 += "<br>" + i

    #Norm_score1=(df1_for_plot-min_df)/(max_df-min_df)
    df1_for_plot = pd.DataFrame((0.1+0.9*((df[df["Model"] == model1][skill_player]-min_df)/(max_df-min_df))).iloc[0])
    df1_for_plot.columns = ["score"]
    print(df1_for_plot)
    df2_for_plot = pd.DataFrame((0.1+0.9*((df[df["Model"] == model2][skill_player]-min_df)/(max_df-min_df))).iloc[0])
    df2_for_plot.columns = ["score"]
    
    fig = go.Figure(
        data=go.Scatterpolar(
            r=df1_for_plot["score"],
            theta=df1_for_plot.index,
            fill="toself",
            marker_color="rgb(255,0,0)",
            opacity=1,
            hoverinfo="text",
            name=text_scores_1,
            text=[
                df1_for_plot.index[i] + " = " + str(df1_for_plot["score"][i])
                for i in range(len(df1_for_plot))
            ],
        )
    )
    fig.update_traces(mode = "lines",fill='toself', marker = dict(size = 6))
    fig.update_polars(angularaxis_tickfont=dict(family="Courier",size=16),angularaxis_color="white",radialaxis_tickmode="array",radialaxis_gridcolor="darkgray",radialaxis_nticks=5)
    fig.add_trace(
        go.Scatterpolar(
            r=df2_for_plot["score"],
            theta=df2_for_plot.index,
            fill="toself",
            marker_color="rgb(0,0,255)",
            hoverinfo="text",
            name=text_scores_2,
            text=[
                df2_for_plot.index[i] + " = " + str(df2_for_plot["score"][i])
                for i in range(len(df2_for_plot))
            ],
        )
    )

    fig.update_layout(
        polar=dict(
            hole=0.1,
            #bgcolor="rgb(44, 43, 43);",
            radialaxis=dict(
                visible=True,
                type="linear",
                autotypenumbers="strict",
                autorange=False,
                range=[0, 1],
                angle=90,
                showline=False,
                showticklabels=False,
                ticks="",
                #gridcolor="black",
            ),
        ),
        width=550,
        height=550,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgb(44, 43, 43)",
        #paper_bgcolor="rgba(0, 0, 0, 0)",
        #font_color="black",
        #font_size=15,
    )
   

    #table 1
    table_updated1 = df[df["Model"] == model1].to_dict("records")
    
    #gauge plot 1
    df1_for_plot = pd.DataFrame(df[df["Model"] == model1]["Debit"])
    df1_for_plot["name"] = model1
    gauge1 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df1_for_plot["Debit"].iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "red"}},
        )
    )
    gauge1.update_layout(
        height=300,
        margin=dict(l=10, r=40, t=10, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="white",
        #template="plotly_dark",
        font_size=15,
    )
    # barplot 1
    """
    df1_for_plot = pd.DataFrame(
        df[df["Model"] == player1][skills1].iloc[0].reset_index()
    )
    df1_for_plot.rename(columns={df1_for_plot.columns[1]: "counts"}, inplace=True)
    df1_for_plot.rename(columns={df1_for_plot.columns[0]: "skills"}, inplace=True)
    barplot1 = px.bar(df1_for_plot, x="skills", y="counts")
    barplot1.update_traces(marker_color="#5000bf")
    barplot1.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        # yaxis={'visible': False, 'showticklabels': True},
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=10,
    )
    barplot1.update_yaxes(range=[1, 100])
 """
    # table 2
    table_updated2 = df[df["Model"] == model2].to_dict("records")

    # gauge plot 2
    df2_for_plot = pd.DataFrame(df[df["Model"] == model2]["Debit"])
    df2_for_plot["name"] = model2
    gauge2 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df2_for_plot["Debit"].iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "blue"}},
        )
    )
    gauge2.update_layout(
        height=300,
        margin=dict(l=10, r=40, t=10, b=10),
        showlegend=False,
         template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="white",
        #template="plotly_dark",
        font_size=15,
    )
  
    # bar plot 2
    """
    df2_for_plot = pd.DataFrame(
        df2[df2["Model"] == player2][skills1].iloc[0].reset_index()
    )
    df2_for_plot.rename(columns={df2_for_plot.columns[1]: "counts"}, inplace=True)
    df2_for_plot.rename(columns={df2_for_plot.columns[0]: "skills"}, inplace=True)
    barplot2 = px.bar(df2_for_plot, x="skills", y="counts")
    barplot2.update_traces(marker_color="rgb(255,171,0)")
    barplot2.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=10,
    )
    barplot2.update_yaxes(range=[1, 100])
    """

    # cards
    
    p_pos_1 = str(round((df[df["Model"] == model1]["Size"].iloc[0])/(df[df["Model"] == model2]["Size"].iloc[0]),3)) +" X"
    
    p_value_1 = (
        str(round(df[df["Model"] == model1]["Latency"].iloc[0] /df[df["Model"] == model2]["Latency"].iloc[0],3))
        + " X"
    )
    p_skill_1 = str(round(df[df["Model"] == model1]["Memory"].iloc[0]/df[df["Model"] == model2]["Memory"].iloc[0],3))+" X"
    p_foot_1 = str(round(df[df["Model"] == model1]["Accuracy"].iloc[0]-df[df["Model"] == model2]["Accuracy"].iloc[0],3))+ " %"
    
    p_pos_2 = str(round((df[df["Model"] == model2]["Size"].iloc[0])/(df[df["Model"] == model1]["Size"].iloc[0]),3)) +" X"
    p_value_2 =(
        str(round(df[df["Model"] == model2]["Latency"].iloc[0] /df[df["Model"] == model1]["Latency"].iloc[0],3))
        + " X"
    )
    p_skill_2 = str(round(df[df["Model"] == model2]["Memory"].iloc[0]/df[df["Model"] == model1]["Memory"].iloc[0],3))+" X"
    p_foot_2 =str(round(df[df["Model"] == model2]["Accuracy"].iloc[0]-df[df["Model"] == model1]["Accuracy"].iloc[0],3))+ " %"

    
    

    # outputs
    return (
        fig,
        table_updated1,
        gauge1,
        #None,#barplot1
        table_updated2,
        gauge2,
        #None,#barplot2,
        p_pos_1,
        p_value_1,
        p_skill_1,
        p_foot_1,
        p_pos_2,
        p_value_2,
        p_skill_2,
        p_foot_2,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
