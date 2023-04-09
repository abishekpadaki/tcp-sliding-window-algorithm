import plotly.graph_objs as go

def drop_packets_graph():
    # Read data from file
    x = []
    y = []
    with open("drop_time.txt", "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            x.append(parts[1])
            y.append(int(parts[0]))

    # Create plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))

    fig.update_layout(
        title="Time-Series Line Graph",
        xaxis_title="Time",
        yaxis_title="Sequence Number",
    )

    fig.show()

def rcv_seq_graph():
    # Read data from file
    x = []
    y = []
    with open("receive_time.txt", "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            x.append(parts[1])
            y.append(int(parts[0]))

    # Create plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))

    fig.update_layout(
        title="Time-Series Line Graph",
        xaxis_title="Time",
        yaxis_title="Sequence Number",
    )

    fig.show()

selection = input("Enter 1 to generate TCP Seq dropped over time \n Enter 2 to generate TCP Seq received over time \n")

match(selection):
    case '1':
        drop_packets_graph()
    case '2':
        rcv_seq_graph()
    case _:
        print("Incorrect Input") 

