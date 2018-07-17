import click
import pandas as pd
from dwd_cdc.bokeh_service import dashboard
from dwd_cdc.ftp_service import retrieve_df

pd.options.display.width = 120
pd.options.display.max_rows = 2 * 24


@click.command()
def show_dashboard():
    df = retrieve_df()
    dashboard(df)


@click.command()
def show_data():
    df = retrieve_df()
    print(df)
