# Syslog-ng

This document briefly covers how syslog-ng is used in our system.  We will go over why we used it, where we have it deployed and what we have it doing, what the configs we have used mean, and potential future steps.  

## Why Syslog-ng

Syslog-ng is client side log shipper with strong parsing abilities, fast log handling for C processing, abritrary python scripting for filtering, and elasticsearch integration, and at the time had better documentation and support than other client side log shippers.  It is also extendable with specific modules we developed, though this ended up being harder to do than initially expected (this part of syslog-ng was not well documented).  

Since we are using the other two components of the ELK stack (Elasticsearch, Kibana), we feel we should elaborate on why we did not use Logstash, with dumb shippers sending all logs to logstash for processing.  Primarily, we did not want to pay for processing all of our logs in an additional logstash cluster; processing and filtering client side would be cheaper in bandwidth (we aren't shipping all of the logs just to drop them) and processing wise (C is cheaper than Java).  Secondly, we were already creating transducer control infastructure on our virtue nodes, and having the log processing done client side allows us to use that tooling, rather than creating more to interact with Logstash. 

## Where and how we use it

We currently deploy syslog-ng on our virtue nodes and valor nodes. We use it with the Elasticsearch module, for forwarding our logs on to elasticsearch, and with our transducer-module for managing which logs get shipped.  

Syslog-ng has changed it's documentation links repeatedly during this project, so we won't post a documentation link here; you're looking for "syslog-ng Open Source Edition - Administration Guide", though.  This will describe the configuration in more detail than we will go into.

Note:  Updates to elasticsearch will require updates to the elasticsearch-module used by syslog-ng.  

### Virtue Nodes

On our virtue nodes, we have syslog-ng deployed with the elasticsearch module and our transducer module (documentation on this module, both how to dev and install, can be found in the README in galahad/transducers/transducer-module).

The current configuration for this node can be found in galahad/assembler/payload/syslog-ng-virtue-node.conf.template.  We will elaborate on less obvious sections here. 

At the bottom of the config file, we define our log paths.  Each log entry defines a log path; we have differing ones for either different parsing rules or sources.  The first log path deals with our LSM/kernel and crossover logs, the second path handles app armor logs, and the final one handles auditd logs.  The different parsing rules cover differences in the format of the LSM, apparmor, and audit logs.  

Note the call
	
	parser(transducer_controller);

This passes our log streams through our transducer_controller module, which filters the incoming logs based on enabled and disable log types.  

This config may need to be changed should the format of any logs be changed, or additional log sources want to be included in our system.  Otherwise, it should be mostly stable.  

Note:  The transducer-module communicates with merlin to handle transducer changes via a unix domain socket.  Modifying the socket location or user/groups in the service files for syslog-ng or merlin can break this connection (Unix domain sockets are finicky).  

#### Deployment

The syslog-ng for the virtue nodes is set up and deployed in the assembler.  

### Valor Nodes

Our valor nodes are much simplier.  The syslog-ng deployment there does not include our transducer-module, and exists to send only our introspection logs to elasticsearch.  It's config can be found in galahad/valor/syslog-ng/syslog-ng-valor-node.conf.template.  

#### Deployment

The syslog-ng for valor nodes is set up in excalibur starting (the syslog-ng.conf is fully created then), and installed and deployed in the create valor step.  


##  Syslog-ng setup

This covers how to manually set up syslog-ng (not using the scripting found elsewhere in the project). 

### Intall syslog-ng

To install using apt, first add 

	wget -qO - http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04/Release.key | sudo apt-key add -	
	deb http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04 ./

To your sources.list to access the latest module.  This setup has been tested on version 3.11 and version 3.13.  

To install:
	
	sudo apt install syslog-ng-core=3.14.1-3

### Set up Modules

Install the following:
	
	sudo apt install syslog-ng-mod-java=3.14.1-3  syslog-ng-mod-elastic=3.14.1-3 openjdk-8-jdk
	
* Add libjvm.so to path 

Navigate to /etc/ld.so.conf.d/ and add this to a file (java.conf, say)

	/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/

and run 

	ldconfig 

* Incorrect class loading

We have found that syslog-ng does not actually load all of the syslog-ng java modules.  A hack to get around this is make sure those are in your 'client-lib-dir' (See elasticsearch config in the syslog-ng config files).  You should copy their java modules to your current dir (apparently there have been issues with syslog-ng not parsing multiple directories in the client lib dir config correctly, so this is the recommended solution)

	cp /path/to/syslog-ng/java-modules/ /path/to/elasticsearch/jars/

Note these modules should be in /usr/lib/syslog-ng/java-modules/

Also note that syslog-ng cannot deal with sub-directories here; all jars must be a single directory.  You will need to copy jars form elasticsearch/lib/, elasticsearch/plugins/search-guard-5, and java-modules to a single directory.  


## Install Elasticsearch

This setup is currently tested on elasticsearch version 5.6.3 for both the elastic nodes and for the modules used by syslog-ng.  To install elasticsearch for syslog-ng, just grab the following and tar -zxvf it:

	curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.3.tar.gz

* Install Searchguard Plugin

Go to the elasticsearch dir and run:

	./bin/elasticsearch-plugin install --batch com.floragunn:search-guard-5:5.6.3-16

## Running syslog-ng

Syslog-ng can be run from systemctl, or you can run it manually with 
	
	syslog-ng -Fdv

## Potential Additional Work

Potential new work involving syslog-ng could include:

* Updating syslog-ng or elasticsearch
	- Updates to syslog-ng should be simple; it appears to be mostly backward compatible to prior configurations and versions.  The primary time cost will be re-building the transducer module off of the new version of syslog-ng.  See the transducer-module documentation for building details.
	- Updating elasticsearch will require an update of the elasticsearch and searchguard components of syslog-ng.  This may be as simple as changing version numbers in the setup scripts, but this hasn't be tried before so it may not be as simple. 

* Adding additional sensor elements
	- If the additional sensors fill a similar form as old ones (Adding more logging to the LSM, for example), nothing needs to be done; these should be parsed fine as is.  
	- If the additional sensors are pumping to syslog, but will have a different form than the logs we are currently parsing, an additional log path will need to be added to manage it.  Look at the offical syslog-ng documentation for how to do this; syslog-ng has powerful parsing tools, but they can involve some setup time.  Alternatively, a Python script can be used as a filter, wiht a performance penalty.  

* Extending transducer control
	- Should the transducer module need to change to accomodate some change in the transducer management framework, the code in galahad/transducers/transducer-module will need to change.  This was a somewhat difficult build process to get used to and running, nor is it signifcantly documented on syslog-ng's end.  