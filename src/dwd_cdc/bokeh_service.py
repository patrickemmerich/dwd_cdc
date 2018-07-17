from bokeh.plotting import figure, show


def dashboard(df):
    x = df['MESS_DATUM']
    y = df['R1_cumsum']

    p = figure(title="Precipitation", x_axis_type='datetime', x_axis_label='date', y_axis_label='mm')
    p.line(x, y)
    show(p)
