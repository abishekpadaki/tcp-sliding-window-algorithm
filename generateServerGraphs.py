# ----------------------------------------------------------------------
# Name: Graph plotting script for Server
# Purpose: CS258 - Coding Project 
# Authors: Abishek Padaki and Jatin Battu
# ----------------------------------------------------------------------

import plotly.graph_objs as go

def generate_window_size_graphs():
        # read data from file
    with open("receiver_window.txt", "r") as r:
        rlines = r.readlines()
    r_times = []
    r_values = []
    for line in rlines:
        rvalue, rtimestamp = line.strip().split(",")
        r_times.append(float(rtimestamp))
        r_values.append(int(rvalue))

    # create time series line graph
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=r_times, y=r_values, mode="lines"))
    fig2.update_layout(title="Receiver Window Size by Time", xaxis_title="Time", yaxis_title="Value")
    fig2.show()

def generate_seq_received_graph():
        # read data from file
    with open("seq_number_received.txt", "r") as f:
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
    fig.update_layout(title="Sequence Numbers received over Time", xaxis_title="Time", yaxis_title="Value")
    fig.show()

def generate_seq_dropped_graph():

    # read data from file
    with open("seq_number_dropped.txt", "r") as f:
        lines = f.readlines()

    # separate time and value
    times = []
    values = []
    for line in lines:
        value,timestamp = line.strip().split(",")
        times.append(float(timestamp))
        values.append(int(value))

    # create time series scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=values, mode="markers"))
    fig.update_layout(title="Sequence Numbers Dropped over Time", xaxis_title="Time", yaxis_title="Value")
    fig.show()


generate_seq_dropped_graph()
generate_seq_received_graph()
generate_window_size_graphs()