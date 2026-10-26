import pandas as pd
import plotly.express as px
import plotly.offline as opy

COLORS = ['#6d5efc', '#958aff', '#b4acff', '#22b5ad', '#67ccc6', '#a0e0db', '#f3b75f', '#f6ce92', '#b0bbc9', '#d0d6df']

def manufacturer_counts(df):
    counts = df['manufacturer'].value_counts().rename_axis('Manufacturer').reset_index(name='Count')
    return counts

def frequency_table(df):
    return manufacturer_counts(df).to_html(classes='table table-bordered table-striped table-sm',
                                           index=False, float_format='%.2f', justify='left', border=0)

def charts(df):
    counts = manufacturer_counts(df)
    bar = px.bar(counts, x='Manufacturer', y='Count', color='Manufacturer', color_discrete_sequence=COLORS)
    bar.update_traces(marker_line_width=0, width=0.55, hovertemplate='%{x}<br>%{y} vehicles<extra></extra>')
    bar.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Vehicles', bargap=0.4)
    donut = px.pie(df, names='fuel_type', hole=0.73, color='fuel_type',
                   color_discrete_map={'Gasoline': '#6d5efc', 'Diesel': '#22b5ad', 'Hybrid': '#f3b75f', 'Electric': '#b4acff'})
    donut.update_traces(textinfo='none', marker_line_color='white', marker_line_width=4,
                        hovertemplate='%{label}: %{value} (%{percent})<extra></extra>')
    donut.update_layout(legend=dict(orientation='h', y=-0.05, x=0.5, xanchor='center'),
                        annotations=[dict(text=f'<b>{len(df):,}</b><br>vehicles', x=0.5, y=0.5, showarrow=False, font_size=20)])
    result = []
    for figure in [bar, donut]:
        figure.update_layout(template='plotly_white', font=dict(family='Arial, sans-serif', color='#7c8395', size=12),
                             margin=dict(l=40, r=15, t=15, b=45), height=310, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        figure.update_xaxes(showgrid=False, zeroline=False)
        figure.update_yaxes(gridcolor='#f0f1f6', zeroline=False)
        result.append(opy.plot(figure, output_type='div', include_plotlyjs=False,
                               config={'displayModeBar': False, 'responsive': True}))
    return result
