from publisher.parameter_generator import ParameterGenerator
import configparser
from unittest.mock import patch


def test_explicit_network():
    ini_file_string = """
    [source_db]
    source_db_cluster_id = fred
    liquibase_changelog_url = wilma

    [target_db]
    subnet_ids = subnet-1, subnet-2, subnet-3
    vpc_id = vpc-1234
    instance_type = wilma
    """
    config = configparser.ConfigParser()
    config.read_string(ini_file_string)

    parameter_file = ParameterGenerator(None).generate(config)
    actual_yaml = open(parameter_file.name, 'r').read()
    print(actual_yaml)
    expected_yaml = """parameters:
  DbInstanceClass: wilma
  SourceCluster: fred
  SubnetIds: subnet-1, subnet-2, subnet-3
  VpcId: vpc-1234
template_path: create.yml
"""
    assert actual_yaml == expected_yaml

@patch.object(
    ParameterGenerator, 
    '_discover_network', 
    autospec=True,
    return_value=(['subnet-12', 'subnet-34'],'vpc-555')
)
def test_sourcet_network(discover_network_method):
    ini_file_string = """
    [source_db]
    source_db_cluster_id = fred
    liquibase_changelog_url = wilma

    [target_db]
    subnet_ids = source
    vpc_id = source
    instance_type = wilma
    """
    config = configparser.ConfigParser()
    config.read_string(ini_file_string)

    parameter_file = ParameterGenerator(None).generate(config)
    actual_yaml = open(parameter_file.name, 'r').read()
    print(actual_yaml)
    expected_yaml = """parameters:
  DbInstanceClass: wilma
  SourceCluster: fred
  SubnetIds: subnet-12, subnet-34
  VpcId: vpc-555
template_path: create.yml
"""