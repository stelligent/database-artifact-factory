from publisher.publisher import Publisher
import boto3

def test_happy_path():
    rds_client = boto3.client('rds')
    error_detail = Publisher('tests/config_files/happy.ini', rds_client).publish()
    assert error_detail
