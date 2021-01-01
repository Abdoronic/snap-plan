from ortools.sat.python import cp_model

import plotly.graph_objects as go

from planner.models.floor import Floor
from planner.models.room_type import RoomType

import random


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

    colors = ['#CB48B7', '#FFA9A3', '#20FC8F', '#5FBFF9',
              '#FFE74C', '#F24236', '#FCECC9', '#1B98E0', '#FFD2FC']
    others_color = '#1A1D1A'
    for apartment_no, apartment in enumerate(floor.apartments, 1):
        apartment_color = colors[(apartment_no - 1) % len(colors)]
        for room_no, room in enumerate(apartment.rooms, 1):
            room_type = room.room_type
            xs = solver.Value(room.variables[0])
            xe = solver.Value(room.variables[1])
            ys = solver.Value(room.variables[2])
            ye = solver.Value(room.variables[3])

            # room_fill_color, room_border_color = get_room_colors(room_type)
            room_fill_color = apartment_color
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
                text=f'{room_type.name.capitalize()[:4]} #{apartment.type_id, room_no}',
                showarrow=False
            )

    fig.show()


def get_room_colors(room_type: RoomType):
    return '#CB48B7', 'Black'
