import plotly.graph_objects as go


def visualize_floor(floor, solver):
    fig = go.Figure()

    fig.update_xaxes(range=[0, floor.width])
    fig.update_yaxes(range=[0, floor.length])
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        )
    )

    for apartment_no, apartment in enumerate(floor.apartments, 1):
        for room_no, room in enumerate(apartment.rooms, 1):
            room_type = room.room_type
            xs = solver.Value(room.variables[0])
            xe = solver.Value(room.variables[1])
            ys = solver.Value(room.variables[2])
            ye = solver.Value(room.variables[3])

            room_fill_color, room_border_color = get_room_colors(room_type)

            fig.add_shape(
                type="rect",
                x0=xs, y0=ys,
                x1=xe, y1=ye,
                line=dict(
                    color=room_border_color,
                    width=3,
                ),
                fillcolor=room_fill_color,
            )

            fig.add_annotation(
                x=(xs + xe) / 2,
                y=(ys + ye) / 2,
                text=f'{room_type.name.capitalize()} (A{apartment_no})',
                showarrow=False
            )

    fig.show()

def get_room_colors(room_type):
    return 'PaleTurquoise', 'LightSeaGreen'