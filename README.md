## Background

A "database artifact" is a bundle of metadata and code/automation for creating or
recreating another database.

In the case of creating a database, it includes: * specifications for the location of the new database - networking, etc.
* specifications for the hardware of the cluster instances - cpu, memory etc
* specifications for the maintenance of the cluster - backup windows, etc
* the schema for a relational database

In the case of re-creating a database, it includes:
* a locator for the source database
* specifications for the location of the new database - networking, etc.
* specifications for the hardware of the cluster instances - cpu, memory etc
* specifications for the maintenance of the cluster - backup windows, etc

In both cases, a new cluster is created and automation either does the copy or the create.

In the case of Aurora RDS - the copy can be a "copy-on-write" which means even a massive 
production database can be "copied" in a matter of minutes.  The commonality is shared between
the source and target, while deltas to the target are recorded separately.

The "database artifact" produced by this module is a Docker image.  The image
contains all the necessary metadata and automation to do the necessary.  A Docker image
was used because the automation (originally) contains a fairly diverse mix of software components.

## Installing the Database Artifact Factory

### Prerequisites
You will need a Docker engine installed locally.  For more information on how to do this, please
see: https://docs.docker.com/engine/install/

You will need a python 3.7 or greater environment with pip installed.  For more information on installing
python, please see: https://www.python.org/about/gettingstarted/

### Install via pip
```
pip install db-artifact-factory
```


## Build the Database Artifact

### Configuration
In order to build the artifact, a configuration INI file needs to be created with all the necessary
information for the source and target databases.

An example INI file follows:

```
[source_db]
source_db_cluster_id = dbartifact-prod-create-cluster-1k326eivoq3i0

[target_db]
subnet_ids = source
instance_type = db.r4.large
```
                
The singular published artifact contains all the information to do both the create or the clone.  
This makes for a mix of arguments in the source/target sections - some values are only necessary
for create, and some are only necessary for clone.

* *source_db_cluster_id*
  This is the Aurora RDS database cluster id to clone.  Even when creating a fresh database cluster,
  there should be a "source" database that it is re-creating - just without data.
* *subnet_ids*
  This can be a comma-delimited list of two or more subnet ids to create the target db in, e.g. subnet-1234, subnet-456
  or it can be "source" and discover the subnet-ids from the source db cluster.

  Make sure these subnet_ids are in different AZ.

* *instance_type*
  The instance type of the DB instance created in the cluster, e.g. db.r4.xlarge
* *database_name*
  In the create case, the name of a database to create and apply the liquibase changelog to.  This can be dontcare
  if you only want the artifact to be able to clone.


### Building
To invoke the build process, first make sure there are ambient AWS credentials.

Then run `db-artifact-builder` against the created INI file:
```
db-artifact-builder artifact-config.ini
```

If the build process is successful, the build process will appear in stdout and a Docker image will be created
with the tag `db-artifact`

### Publishing
Once the db-artifact is in the local registry, from here it can be "published" to DockerHub or the internal registry
of choice (e.g. GitHub, Artifactory, etc.).  It is up to the operator to publish the image (and this tool doesn't 
do anything special to support that).

## Converging a Database Artifact
If running locally after a "build", then "convergence" (i.e creating or cloning) is just a matter of running the Docker image with a few execution settings.  If the Docker image has been published in a registry, then a docker pull will be necessary to
make the image accessible.

Ultimately `docker run` is being executed but there is a wrapper CLI script `db-artifact-converge` installed as part of database-artifact-factory that provides a nicer user experience (no fussing with the filesystem mounts and environment variables)

To clarify - installing database-artifact-factory contains both the tools to build and to converge, but an operator v. an end-user
might use only one or the other.

### Clone an Existing Database
The following is the minimal command to clone an existing database.  It presumes a few things:
* that AWS credentials are stored in ~/.aws/credentials
* AWS profile is "default".
* the Docker image db-artifact:latest contains the artifact to converge

BEWARE - you must specify the password, but the username follows from the source cluster
```
db-artifact-converge --db_password thisisafakepassw0rd
```

If any of those defaults are inappropriate, please invoke the `db-artifact-converge -h` to see the other options.

## Future Direction
* Parameterize support for mysql v postgresql
* Add support for other operational configuration items for the RDS cluster
* better progress reporting and troubleshooting mechanisms
* control over stack names
