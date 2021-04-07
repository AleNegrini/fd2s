import json
from datetime import datetime

from dynamo_helper import dynamo_helper
from reader import Reader
from signal_helper import time_series_helper
from utils import Utils


def lambda_handler(event, context):

    # get a few useful environment variables
    window = int(Utils.get_environment('WINDOW', 1200))
    lower_temp = int(Utils.get_environment('LOWER_TEMP', 3200))
    upper_temp = int(Utils.get_environment('UPPER_TEMP', 4300))
    volatility_limit = int(Utils.get_environment('VOLATILITY_LIMIT', 50))
    now = datetime.now()

    # setup a few helper classes
    ts_helper = time_series_helper()
    dynamo_db = dynamo_helper()

    # Read data in
    day = json.loads(event['Records'][0]['body'])['day']
    device = json.loads(event['Records'][0]['body'])['device']
    on_wrist_1hz_df = Reader.read_csv_df('s3://empatica-model-x/'+day+'/'+device+'/on_wrist.csv',
                                         columns=['on_wrist'])
    wrist_temp_4hz_df = Reader.read_csv_df('s3://empatica-model-x/'+day+'/'+device+'/temperature.csv',
                                           columns=['w_temp'])

    # Transform the on_wrist signal from 1Hz to 4Hz
    on_wrist_4hz_array = ts_helper.signal_frequency_equalizer(4,
                                                           'on_wrist',
                                                           on_wrist_1hz_df,
                                                           wrist_temp_4hz_df)

    # Putting together on_wrist(4Hz) signal and wrist_temperature signal
    df = ts_helper.concat_two_time_series(on_wrist_4hz_array['on_wrist'],
                                          wrist_temp_4hz_df['w_temp'],
                                          'on_wrist',
                                          'w_temp')

    # We are only interested in the wrist temperature when the device is on
    df = ts_helper.get_temperature_on_wrist_only(df=df,
                                                 column_name='wrist_temperature')

    # Start evaluating a set of rolling statistics metrics
    df = ts_helper.eval_roll_stats_metrics(window, df)

    # taking the only samples beyond the limits (either upper or lower)
    beyond_samples = df[(df.discostamento > 0)]

    volatility_index = beyond_samples['discostamento'].sum() / len(beyond_samples) \
        if len(beyond_samples)!=0 else 0
    avg = df['wrist_temperature'].mean()
    max = df['wrist_temperature'].max()
    dynamo_db.put_item(table_name='empatica-temp_fd2s_history',
                       item=Utils.build_item_dynamoDB(
                           device_id=device,
                           date=day,
                           volatility_index=str(volatility_index),
                           volatility_anomaly= 'YES' if volatility_index > volatility_limit else 'NO',
                           avg=str(avg),
                           avg_anomaly='YES' if avg < lower_temp or avg > upper_temp else 'NO',
                           max=str(max),
                           max_anomaly='YES' if max > upper_temp else 'NO',
                           timestamp=now.strftime("%d/%m/%Y %H:%M:%S")
                       )
                    )
