import plotly.graph_objs as go

# read data from file
with open("seq_number_dropped.txt", "r") as f:
    lines = f.readlines()

# separate time and value
times = []
values = []
for line in lines:
    value,timestamp = line.strip().split(",")
    times.append((timestamp))
    values.append((value))

# create time series scatter plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=values, mode="markers"))
fig.update_layout(title="Time Series Scatter Plot", xaxis_title="Time", yaxis_title="Value")
fig.show()
