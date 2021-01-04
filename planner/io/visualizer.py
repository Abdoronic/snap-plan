import plotly.graph_objects as go

from typing import Dict

def visualize_floor(floor_plan: Dict):
    fig = go.Figure()
    
    fig.update_xaxes(range=[0, floor_plan['width']])
    fig.update_yaxes(range=[0, floor_plan['length']])
    fig.update_layout(
        width=(50*floor_plan['width']),
        height=(50*floor_plan['length']),
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
    ducts_color = '#1A1D1A'
    modules_color = '#A5A5A5'
    corridors_color = '#F2F2F2'

    for apartment_no, apartment in enumerate(floor_plan['apartments'], 1):
        apartment_color = colors[(apartment_no - 1) % len(colors)]

        for room_no, room in enumerate(apartment['rooms'], 1):
            room_type = room['roomType']
            label = f'{room_type.name.capitalize()[:4]} #{apartment_no, room_no}'
            draw_shape(fig, room, apartment_color, label)

        for hallway in apartment['hallways']:
            label = f'H #{apartment_no}'
            draw_shape(fig, hallway, apartment_color, label, opacity=0.75)

        for duct in apartment['ducts']:
            label = f'D #{apartment_no}'
            draw_shape(fig, duct, ducts_color, label, font_color='#ffffff')

    draw_shape(fig, floor_plan['stairs'], modules_color, 'S')
    draw_shape(fig, floor_plan['elevator'], modules_color, 'E')
    for corridor in floor_plan['corridors']:
        draw_shape(fig, corridor, corridors_color, 'C')

            
    fig.show()


def draw_shape(fig, shape, color, label, opacity=1, font_color='#000000'):

    xs = shape['xs']
    xe = shape['xe']
    ys = shape['ys']
    ye = shape['ye']

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
        opacity=opacity
    )

    fig.add_annotation(
        x=(xs + xe) / 2,
        y=(ys + ye) / 2,
        text=f'<b>{label}</b>',
        showarrow=False,
        font=dict(
            color=font_color
        )
    )
