# Dash Example Dashboard
# ----------------------
# ----------------------

# Import Packages
# ---------------

import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Load Data
# ---------

df = pd.read_csv("../diabetes.csv")


# Generate HTML-Table for Dash
# ----------------------------

# Build a Dash-HTML table based on the structure of the Data Frame

def generate_table(dataframe, max_rows=50):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Build Dashboard
# ---------------


app = dash.Dash()  # Initialize dash application

# Reference externally hosted CSS file
my_css_url = "https://codepen.io/madjazz/pen/awxxQK.css"
app.css.append_css({
    "external_url": my_css_url
})

# Define layout
app.layout = html.Div(children=[
    html.H1(children="Simple Dashboard Example", style={"height": "100px", "text-align": "center"}),

    html.H2(children="Plots", style={"text-align": "center"}),

    # From core components use the dropdown component
    dcc.Dropdown(
        id="dropdown-graph",
        options=[
            {"label": "Insulin vs BMI", "value": "insulin_bmi"},
            {"label": "Glucose vs BMI", "value": "glucose_bmi"},
            {"label": "Age vs BMI", "value": "age_bmi"}
        ],
        value="insulin_bmi"
    ),

    # Set position of plot
    dcc.Graph(id="display-graph", style={"padding-bottom": "50px"}),

    # Set position where table should be generated
    html.Div(children=[
            html.H2(children="Pima Indians Diabetes Data", style={"text-align": "center"}),
            generate_table(df, max_rows=100)
            ], style={"height": "400px", "overflow-y": "scroll", "padding": "0 0 50px 0"})
])

# Generate plot in backend based on selected dropdown value


@app.callback(Output("display-graph", "figure"),  # The id of the plot indicates where the output is sent to
              [Input("dropdown-graph", "value")])  # The dropdown value is the the specific input to the backend
def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "insulin_bmi":
        return {"data": [
                go.Scatter(
                    x=df["Insulin"],
                    y=df["BMI"],
                    mode="markers",
                    opacity=0.7
                )],
                "layout": go.Layout(
                    title="Insulin vs BMI",
                    xaxis={"title": "Insulin"},
                    yaxis={"title": "BMI"})
            }

    elif selected_dropdown_value == "glucose_bmi":
        return {"data": [
            go.Scatter(
                x=df["Glucose"],
                y=df["BMI"],
                mode="markers",
                opacity=0.7
            )],
            "layout": go.Layout(
                title="Glucose vs BMI",
                xaxis={"title": "Glucose"},
                yaxis={"title": "BMI"})
        }

    else:
        return {"data": [
            go.Scatter(
                x=df["Age"],
                y=df["BMI"],
                mode="markers",
                opacity=0.7
            )],
            "layout": go.Layout(
                title="Age vs BMI",
                xaxis={"title": "Age"},
                yaxis={"title": "BMI"})
        }


app.run_server(debug=True)
