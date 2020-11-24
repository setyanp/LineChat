'''
FOR VISUALIZING DATA
'''

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class DrawFigure:
    def vertical_bar_graph(self,list_data,name_1,name_2,graph_title,color_1,color_2):
        try:
            label_width = [0.5,0.5]
            label = [name_1,name_2]
            fig = go.Figure(
                            data=[go.Bar(x=label, y=list_data, width = label_width, text = list_data, textposition='outside', marker=dict(color=[
                                    color_1,color_2]))],
                            layout=go.Layout(template="simple_white",
                                        title=go.layout.Title(text=graph_title, y= 0.9, x = 0.5, xanchor="center"),
                                        yaxis = dict(title = graph_title.lower(),range=[0,list_data[1]+(15/100*list_data[1])]),
                                        xaxis = dict(range=[-0.5,1.5]),
                                        width=500,
                                        height=500,
                            ))
            filename = graph_title.replace(' ', '-').lower()
            folder = 'images/'
            filename = folder+filename + '.png'
            fig.write_image(filename)
        except Exception as e:
            print(e)

    def horizontal_bar_labels(self, tuple_value_data, graph_title, bar_color):
        try:
            desc_data_list = sorted(tuple_value_data, reverse = True, key = lambda t : t[1] )

            data_sorted = []
            rating_sorted = []

            for i in desc_data_list:
                data_sorted += [i[0].capitalize()]
                rating_sorted += [i[1]]

            values_string = []
            sum_data = sum(rating_sorted)
            for j in rating_sorted:
                percentage_value = (j/sum_data) * 100
                percentage_value = str(round(percentage_value, 2))
                values_string += [percentage_value + '% (' + str(j) + ')']

            subplots = make_subplots(
                rows = len(data_sorted),
                cols=1,
                subplot_titles = data_sorted,
                shared_xaxes=True,
                print_grid=False,
                vertical_spacing = (0.45/ len(data_sorted)),
            )

            subplots['layout'].update(
                plot_bgcolor='#fff',
            )

            # add bars for the categories
            for k, x in enumerate(data_sorted):
                bar_color2 = bar_color
                subplots.add_trace(dict(
                    type='bar',
                    orientation='h',
                    y = [data_sorted[k]],
                    x = [rating_sorted[k]],
                    text=[values_string[k]],
                    hoverinfo='text',
                    textposition='auto',
                    textangle=0,
                    marker=dict(
                        color=bar_color2,
                    ),
                ),k+1, 1)

            # update the layout
            subplots['layout'].update(
                showlegend = False,
                title_text= graph_title.capitalize()
            )

            for x in subplots["layout"]['annotations']:
                x['x'] = 0
                x['xanchor'] = 'left'
                x['align'] = 'left'
                x['font'] = dict(
                size=12,
                )

            for axis in subplots['layout']:
                if axis.startswith('yaxis') or axis.startswith('xaxis'):
                    subplots['layout'][axis]['visible'] = False

            # update the margins and size
            subplots['layout']['margin'] = {
                'l': 0,
                'r': 0,
                't': 50,
                'b': 2,
            }
            height_calc = 70 * len(data_sorted)
            # height_calc = max([height_calc, 300])
            subplots['layout']['height'] = height_calc
            subplots['layout']['width'] = 500

            filename = graph_title.replace(' ', '-').lower()
            folder = 'images/'
            filename = folder+filename + '.png'
            subplots.write_image(filename)
        except Exception as e:
            print(e)

    def stacked_bar(self,df,name_1,name_2,title,color_1,color_2):
        try:
            fig = go.Figure(data=[
                go.Bar(name = name_1, x = df['chat_time'], y = df['total_name1'],marker_color=color_1),
                go.Bar(name = name_2, x = df['chat_time'], y = df['total_name2'],marker_color=color_2)
            ])

            fig.update_layout(barmode='stack',
                            title=go.layout.Title(text=title, y= 0.9, x = 0.5, xanchor="center"))

            filename = title.replace(' ', '-').lower()
            folder = 'images/'
            filename = folder+filename + '.png'
            fig.write_image(filename)
        except Exception as e:
            print(e)