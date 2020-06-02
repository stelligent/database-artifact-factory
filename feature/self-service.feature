Feature: Self-service Database Artifact
  As a data analysts/scientist/engineer
  I would like recreate a production database with a single-click
  So that I can do exploratory testing

Scenario: Create from scratch
  Given a database artifact published in a docker registry
    And AWS credentials are set as docker secrets
    And db username and password are set as docker secrets
   When I pull the image
    And I run the image with ENV var CREATE_MODE=create
   Then an empty RDS cluster is created with the credentials from secrets
    And the instances are configured with settings determined by the publisher
    And liquibase is invoked to converge the schema of the database
    And a URL is emitted to stdout for accessing the database

Scenario: Copy of Production Database
  Given a database artifact published in a docker registry
    And AWS credentials are set as docker secrets
    And db username and password are set as docker secrets
   When I pull the image
    And I run the image with ENV var CREATE_MODE=clone
   Then a copy-on-write cloned RDS cluster is created with the credentials from secrets
    And the instances are configured with settings determined by the publisher
    And a URL is emitted to stdout for accessing the database

Scenario: Missing credentials
  Given aws creds aren't in secrets or db creds
   When running
   Then an error message indicates which secrets are missing    

Scenario: Bad CREATE_MODE
  Given CREATE_MODE isn't clone|create
   When running
   Then an error message indicates legal modes

Scenario: Artifact fails to converge
  When running
   And the convergence fails for some reason
  Then the failure will emit to stderr
   And publisher contact information will be emitted to stdout    