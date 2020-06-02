Feature: Publish a Database Artifact
  As a DataOps engineer
  I would like to emit Docker images that can recreate production databases
  So that analysts can do self-service exploratory testing

  Additional points to consider about the implementation:
  * For schema versioning and change control, liquibase is the chosen tool
  * liquibase requires a JVM to run
  * Calling liquibase from Maven is probably the most convenient way to call it - but not the only way
  * python has the most reach within Stelligent, so anything that doesn't explicitly require Java will be developed in python
  * Docker images are the best tool to make sure a JVM, mvn and python run together with no fuss
  * GitHub Packages easiest registry to use?
  * Anything we need to worry about wrt parallel query in src/dest?
  * Given we can clone from cfn.... probably just use Sceptre to do heavy lifting?

Scenario: Minimal Publish
    Given a source database exists
      And a configuration file describes the source database
       | source_db_cluster_id     | emk-1                                            |
       | liquibase_changelog_url  | https://github.com/stelligent/foo/change_log.xml | 
      And a target database configuration file
       | subnet_ids: source         |
       | vpc_id: source             |
       | instance_type: db.r4.large |
    When publish is invoked
    Then the subnet_ids and vpc_id of the source db are discovered
     And a Cloudformation template is generated with those settings including:
       | source cluster id |
       | subnet ids |
       | vpc id |
     And a Docker image is build that includes components:
       | JVM        |
       | python 3.8 |
       | Sceptre    |
       | liquibase  |
    And the publisher repo
    And the change_log
    And the entrypoint is set to the database-artifact-factory script

Scenario: The factory script for create
 Given create_mode=fresh
  When invoked
  Then sceptre runs minimal-create.yml cfn template
  And invokes liquibase against the created db
  And emits the endpoint to the created cluster

Scenario: The factory script for clone
 Given create_mode=clone
  When invoked
  Then sceptre runs minimal-clone.yml cfn template
  And emits the endpoint to the created cluster