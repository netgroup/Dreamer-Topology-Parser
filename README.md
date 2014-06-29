![Alt text](repo_data/dreamer-logo.png "Optional title")

Dreamer-Topology-Parser-and-Validator
=====================================

Topology Parser and Validator For Dreamer Project (GÉANT Open Call)

Using this tools you can parse and validate the topologies created with
Dreamer-Topology-Designer.

License
=======

This sofware is licensed under the Apache License, Version 2.0.

Information can be found here:
 [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Tips
==============

Set "path" in TopoParser, it is the base path for the store of the
topologies.

Usage
=====

Example of using TopoParser and Validator

#####TopoParser

		if __name__ == '__main__':
			parser = TopoParser("topo3.json", verbose = False)
			(ppsubnets, l2subnets) = parser.getsubnets()
			print "*** Networks Point To Point"
			for ppsubnet in ppsubnets:
					links = ppsubnet.getOrderedLinks()
					print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
			print "*** Switched Networks"
			for l2subnet in l2subnets:
					links = l2subnet.getOrderedLinks()
					print "*** Subnet: Node %s - Links %s" %(l2subnet.nodes, links)
			print "*** VLLs",parser.getVLLs()
			print "*** Tunneling", parser.tunneling

TODO
======

Validator implementation

