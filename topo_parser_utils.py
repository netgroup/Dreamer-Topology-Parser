#!/usr/bin/python

##############################################################################################
# Copyright (C) 2014 Pier Luigi Ventre - (Consortium GARR and University of Rome "Tor Vergata")
# Copyright (C) 2014 Giuseppe Siracusano, Stefano Salsano - (CNIT and University of Rome "Tor Vergata")
# www.garr.it - www.uniroma2.it/netgroup - www.cnit.it
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Topology Parser Utils.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
#
#
# Utility Class Store The Set Of Links and Nodes In a Subnet
class Subnet: 
	def __init__(self, Type=None):
		self.nodes = []
		self.links = []

	def appendLink(self, link):
		#if link[0] not in self.nodes:
			self.nodes.append(link[0])
		#if link[1] not in self.nodes:
			self.nodes.append(link[1])
		#if link not in self.links:
			self.links.append(link)

	# Provides the links in a proper order (if the network is "Access"; this order is very important for now in Mininet)
	# the links are ordered, executing a deep-first search on L2Subnet, starting from the AOSHIS,
	# XXX At the end of visit, the links are removed
	def getOrderedLinks(self):
		links = self.links
		return links

	# Retrieves all the AOS
	def getAOS(self):
		ret_aos = []
		for node in self.nodes:
			if 'aos' in node and node not in ret_aos:
				ret_aos.append(node)
		return ret_aos


# Cemetery of code

	"""# Executes a deep-first search on L2Subnet
	def deep_first_search(self):
		if self.verbose:
			print "*** Explore Subnet - Type %s: Nodes %s - Links %s" % (self.type, self.nodes, self.links)
		nodes = self.getAOS()
		ret_links = []
		links = []
		while len(nodes) > 0:
			links_to_remove = []
			node = nodes[0]
			(tmpnodes, tmplinks) = self.getOrderedNextLinksAndNodes(node)
			for tmpnode in tmpnodes:
				if tmpnode not in nodes:
					nodes.append(tmpnode)
			for tmplink in tmplinks:
				if tmplink not in links:
					links.append(tmplink)
			for link in links:
				if node in link[0] or node in link[1]:
					ret_links.append(link)
					links_to_remove.append(link)
			nodes.remove(node)
			for toremove in links_to_remove:
				links.remove(toremove)
		return ret_links

	# get Next Hop and links towards the next hop, and pop the node and
	# links from nodes and links before to return
	def getOrderedNextLinksAndNodes(self, node):
		ret_node = []
		ret_link = []
		for link in self.links:
			if node in link[0]:
				ret_node.append(link[1])
				ret_link.append(link)
			elif node in link[1]:
				ret_node.append(link[0])
				ret_link.append(link)
		for link in ret_link:
			self.links.remove(link)
		self.nodes.remove(node)
		return (ret_node, ret_link)"""
