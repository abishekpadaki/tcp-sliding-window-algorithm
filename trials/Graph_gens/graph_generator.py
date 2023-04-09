import plotly.graph_objs as go
import time

# read data from file
with open("windowsize.txt", "r") as f:
    lines = f.readlines()

with open("receiver_window.txt", "r") as r:
    rlines = r.readlines()

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