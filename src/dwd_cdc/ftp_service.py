import collections
import ftplib
import io
from zipfile import ZipFile

import pandas as pd

Station = collections.namedtuple('Station', 'name id')
elsenz = Station(name='Eppingen-Elsenz', id=str(1255).zfill(5))

Data = collections.namedtuple('Data', 'type ty')
precip = Data(type='precipitation', ty='rr')
temper = Data(type='air_temperature', ty='tu')


def retrieve_df(station=elsenz, data=precip):
    ftp = ftplib.FTP('ftp-cdc.dwd.de')
    ftp.login()
    ftp.cwd('/pub/CDC/observations_germany/climate/hourly/{type}/recent'.format(type=data.type))

    with io.BytesIO() as f:
        try:
            ftp.retrbinary('RETR stundenwerte_{ty}_{id}_akt.zip'.format(id=station.id, ty=data.ty.upper()), f.write)
            zipfile = ZipFile(f)
            filename = _find_filename(zipfile, filename_prefix='produkt_{}_stunde'.format(data.ty))
            csv_file = zipfile.open(filename)
            df = pd.read_csv(csv_file, sep=';', converters={'MESS_DATUM': _convert_date})

            df.rename(columns=lambda x: x.strip(), inplace=True)
            df['STATIONS_NAME'] = station.name
            df['MESS_DATUM_DAY'] = df['MESS_DATUM'].apply(lambda x: x.date())
            df = _cumsum(df, col='R1', groupby='MESS_DATUM_DAY')

            return df

        except ftplib.Error as e:
            print(e)


def _find_filename(zipfile, filename_prefix):
    filenames = zipfile.namelist()
    matching_filenames = [f for f in filenames if str(f).startswith(filename_prefix)]
    assert len(matching_filenames) == 1, "Filename with prefix {} not among filenames {} of zip-file, or not unique" \
        .format(filename_prefix, filenames)
    return matching_filenames[0]


def _convert_date(mess_datum):
    year = int(mess_datum[0:4])
    month = int(mess_datum[4:6])
    day = int(mess_datum[6:8])
    hour = int(mess_datum[8:10])
    return pd.datetime(year, month, day, hour)


def _cumsum(df, col, groupby):
    if col in df.columns:
        df['{}_cumsum'.format(col)] = df.groupby(by=groupby)[col].cumsum()
    return df
