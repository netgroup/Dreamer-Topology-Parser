![Alt text](repo_data/dreamer-logo.png "Optional title")

Dreamer-Topology-Parser
=====================================

Topology Parser For Dreamer Project (GÉANT Open Call)

Using this tools you can parse and validate the topologies created with
[Dreamer-Topology-Designer](https://github.com/netgroup/Dreamer-Topology-Designer).

License
=======

This sofware is licensed under the Apache License, Version 2.0.

Information can be found here:
 [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Tips
==============


Usage
=====

Example of usage TopoParser

#####TopoParser

		if __name__ == '__main__':

				parser = TopoParser("../Dreamer-Mininet-Extensions/topo/topo_vll.json", verbose = False)
				ppsubnets = parser.getsubnets()
				print "*** Nodes:"
				for cr, cr_property in zip(parser.cr_oshis, parser.cr_oshis_properties):
				        print "*** CR: %s - Property: %s" %(cr, cr_property)
				for pe, pe_property in zip(parser.pe_oshis, parser.pe_oshis_properties):
				        print "*** PE: %s - Property: %s" %(pe, pe_property)
				for cer, cer_property in zip(parser.cers, parser.cers_properties):
				        print "*** CER: %s - Property: %s" %(cer, cer_property)
				for ctrl, ctrl_property in zip(parser.ctrls, parser.ctrls_properties):
				        print "*** CTRL: %s - Property: %s" %(ctrl, ctrl_property)
				print "*** Networks Point To Point"
				for ppsubnet in ppsubnets:
				                links = ppsubnet.links
				                print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
				print "*** VLLs",parser.getVLLs()
				print "*** PWs", parser.getPWs()
				print "*** VSs", parser.getVSs()
				print "*** Tunneling", parser.tunneling
				print "*** Testbed", parser.testbed
				print "*** Mapped", parser.mapped
				print "*** Generated", parser.generated
				print "*** VLAN", parser.vlan		
