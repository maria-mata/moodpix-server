import os
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    username = os.environ['TONE_USERNAME'],
    password = os.environ['TONE_PASSWORD'],
    version = '2017-09-21')
