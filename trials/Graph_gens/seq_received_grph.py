import plotly.graph_objs as go
import time

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
fig.update_layout(title="Time Series Line Graph", xaxis_title="Time", yaxis_title="Value")
fig.show()
