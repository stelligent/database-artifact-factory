from publisher.publisher_config import PublisherConfig
from publisher.config_exception import ConfigException
import pytest

def test_file_not_found():
    '''Given a bogus path
    When it is parsed
    Then it raises file not found exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(FileNotFoundError) as excinfo:
        publisher_config.parse('/something/bogus')

def test_empty_file():
    '''Given an empty file
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/empty_source.ini')

def test_missing_source_db_section():
    '''Given a file without source_db
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/missing_sections.ini')
    
    actual_message = str(excinfo.value)
    expected_message = "Missing sections: {'source_db'}"

    assert actual_message == expected_message    

def test_missing_source_key():
    '''Given a file wit missing key
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/missing_key.ini')
    
    actual_message = str(excinfo.value)
    expected_message = "Missing source_db key: {'liquibase_changelog_url'}"

    assert actual_message == expected_message        

def test_missing_target_key():
    '''Given a file wit missing key
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/missing_target_key.ini')
    
    actual_message = str(excinfo.value)
    expected_message = "Missing target_db key: {'instance_type'}"

    assert actual_message == expected_message  

def test_happy_path():
    '''Given a good file
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    config = publisher_config.parse('tests/config_files/happy.ini')
    assert config['source_db']['source_db_cluster_id'] == 'fred'
    assert config['target_db']['subnet_ids'] == 'subnet-1, subnet-2, subnet-3'

def test_mangled_subnet_ids():
    '''Given a good file
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/manged_subnets.ini')

    actual_message = str(excinfo.value)
    expected_message = "target_db/subnet_ids must be set to source or a comma-delmited-list of subnets, e.g subnet-1,subnet2,subnet-3"

    assert actual_message == expected_message  

def test_source():
    '''Given a good file
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()
    config = publisher_config.parse('tests/config_files/source_subnet.ini')
    assert config['target_db']['subnet_ids'] == 'source'  

def test_mangled_vpc_id():
    '''Given a good file
    When it is parsed
    Then it raises and invalid format exception'''
    publisher_config = PublisherConfig()

    with pytest.raises(ConfigException) as excinfo:
        publisher_config.parse('tests/config_files/bad_vpc.ini')

    actual_message = str(excinfo.value)
    expected_message = "target_db/vpc_id must be set to source or a vpc id, e.g vpc-1234"

    assert actual_message == expected_message  