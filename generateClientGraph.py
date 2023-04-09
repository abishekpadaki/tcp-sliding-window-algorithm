# ----------------------------------------------------------------------
# Name: Graph plotting script for Client
# Purpose: CS258 - Coding Project 
# Authors: Abishek Padaki and Jatin Battu
# ----------------------------------------------------------------------

import plotly.graph_objs as go

def generate_window_size_graphs():
        # read data from file
    with open("windowsize.txt", "r") as f:
        lines = f.readlines()

    # separate time and value
    times = []
    values = []
    for line in lines:
        value, timestamp = line.strip().split(",")
        times.append(float(timestamp))
        values.append(int(value))

    # create time series line graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=values, mode="lines"))
    fig.update_layout(title="Sender Window Size by Time", xaxis_title="Time", yaxis_title="Value")
    fig.show()


generate_window_size_graphs()