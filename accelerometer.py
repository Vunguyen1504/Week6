import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Output, Input

# ---------------------------------------------------
# 1. Read accelerometer CSV file
# ---------------------------------------------------
# Adjust the filename/path to your file
df = pd.read_csv("gyro_data.csv")

# Make sure timestamp is parsed correctly
# If your CSV timestamps don’t include the year, add it manually
try:
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
except Exception:
    # fallback if no year is given in timestamp, prefix with 2025
    df["timestamp"] = pd.to_datetime("2025-" + df["timestamp"], errors="coerce")

# ---------------------------------------------------
# 2. Initialize the Dash app
# ---------------------------------------------------
app = Dash(__name__)

# ---------------------------------------------------
# 3. Layout
# ---------------------------------------------------
app.layout = html.Div([
    html.H2("Accelerometer Monitoring Dashboard"),
    html.Hr(),

    # Dropdown to pick which axis to view
    dcc.Dropdown(
        id="axis-choice",
        options=["x", "y", "z"],
        value="x",
        clearable=False
    ),

    # Table of recent data
    dash_table.DataTable(
        id="accel-table",
        data=df.tail(10).to_dict("records"),
        page_size=5
    ),

    # Graph of chosen axis
    dcc.Graph(id="accel-graph")
])

# ---------------------------------------------------
# 4. Callbacks
# ---------------------------------------------------
@app.callback(
    Output("accel-graph", "figure"),
    Output("accel-table", "data"),
    Input("axis-choice", "value")
)
def update_graph(selected_axis):
    # Build line graph of the chosen axis
    fig = px.line(df, x="timestamp", y=selected_axis,
                  title=f"{selected_axis} over Time",
                  markers=True)

    # Update table with latest 10 rows
    table_data = df.tail(10).to_dict("records")

    return fig, table_data

# ---------------------------------------------------
# 5. Run the app (use port 8051 to avoid conflicts)
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8051, jupyter_mode="tab")
