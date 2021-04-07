import json
from datetime import datetime

from dynamo_helper import dynamo_helper
from reader import Reader
from ts_signal_helper import time_series_helper
from ppg_utils import Utils


def lambda_handler(event, context):

    # get useful env variables
    now = datetime.now()
    max_ppg_inf = int(Utils.get_environment('MAX_PPG_INF', 19000))
    max_ppg_sup = int(Utils.get_environment('MAX_PPG_SUP', 21000))
    min_ppg_inf = int(Utils.get_environment('MIN_PPG_INF', 1000))
    min_ppg_sup = int(Utils.get_environment('MIN_PPG_SUP', 6000))
    avg_ppg_inf = int(Utils.get_environment('AVG_PPG_INF', 5000))
    avg_ppg_sup = int(Utils.get_environment('AVG_PPG_SUP', 11000))

    # setup a few helper classes
    ts_helper = time_series_helper()
    dynamo_db = dynamo_helper()

    # Read data in
    day = json.loads(event['Records'][0]['body'])['day']
    device = json.loads(event['Records'][0]['body'])['device']
    on_wrist_1hz_df = Reader.read_csv_df('s3://empatica-model-x/'+day+'/'+device+'/on_wrist.csv',
                                         columns=['on_wrist'])
    ppg_64hz_df = Reader.read_csv_df('s3://empatica-model-x/'+day+'/'+device+'/ppg_green.csv',
                                           columns=['ppg'])

    # Sampling the 64Hz signal from PPG to 4Hz
    ppg_4hz_array = ts_helper.sample_signal('ppg',
                                            ppg_64hz_df)

    # Transform the on_wrist signal from 1Hz to 4Hz
    on_wrist_4hz_array = ts_helper.signal_frequency_equalizer(4,
                                                              'on_wrist',
                                                              on_wrist_1hz_df)

    # Putting together on_wrist(4Hz) signal and wrist_temperature signal
    df = ts_helper.concat_two_series(on_wrist_4hz_array['on_wrist'],
                                     ppg_4hz_array['ppg'],
                                     'on_wrist',
                                     'ppg')
    # We are only interested in the wrist temperature when the device is on
    df = ts_helper.get_ppg_on_wrist_only(df=df,
                                         column_name='ppg_calc')

    min = df['ppg_calc'][1000:].min()
    max = df['ppg_calc'].max()
    avg = df['ppg_calc'].mean()
    dynamo_db.put_item(table_name='empatica-ppg_fd2s_history',
                       item=Utils.build_item_dynamoDB(
                           device_id=device,
                           date=day,
                           min=str(min),
                           min_anomaly='YES' if min < min_ppg_inf or min > min_ppg_sup else 'NO',
                           avg=str(avg),
                           avg_anomaly='YES' if avg < avg_ppg_inf or avg > avg_ppg_sup else 'NO',
                           max=str(max),
                           max_anomaly='YES' if max < max_ppg_inf or max > max_ppg_sup else 'NO',
                           timestamp=now.strftime("%d/%m/%Y %H:%M:%S")
                       )
                       )
