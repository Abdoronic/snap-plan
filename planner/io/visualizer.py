from ortools.sat.python import cp_model

import plotly.graph_objects as go

from planner.models.floor import Floor


def visualize_floor(floor: Floor, solver: cp_model.CpSolver):
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

    colors = ['#CB48B7', '#FFA9A3', '#20FC8F', '#5FBFF9', '#FFE74C', '#F24236', '#FCECC9', '#1B98E0', '#FFD2FC']
    modules_color = '#1A1D1A'

    for apartment_no, apartment in enumerate(floor.apartments, 1):
        apartment_color = colors[(apartment_no - 1) % len(colors)]

        for room_no, room in enumerate(apartment.rooms, 1):
            room_type = room.room_type
            label = f'{room_type.name.capitalize()[:4]} #{apartment_no, room_no}'
            draw_shape(fig, room.variables, apartment_color, label, solver)

        for hallway in apartment.hallways:
            label = f'H #{apartment_no}'
            draw_shape(fig, hallway.variables, apartment_color, label, solver)

        for duct in apartment.ducts:
            label = f'D #{apartment_no}'
            draw_shape(fig, duct.variables, modules_color, label, solver)

    draw_shape(fig, floor.stairs.variables, modules_color, 'S', solver)
    draw_shape(fig, floor.elevator.variables, modules_color, 'E', solver)
    for corridor in floor.corridors:
        draw_shape(fig, corridor.variables, modules_color, 'C', solver)

            
    fig.show()


def draw_shape(fig, variables, color, label, solver):

    xs = solver.Value(variables[0])
    xe = solver.Value(variables[1])
    ys = solver.Value(variables[2])
    ye = solver.Value(variables[3])

    room_fill_color = color
    room_border_color = "Black"
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
        text=label,
        showarrow=False
    )
