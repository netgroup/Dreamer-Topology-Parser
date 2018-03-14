#!/usr/bin/python

##############################################################################################
# Copyright (C) 2017 Pier Luigi Ventre - (University of Rome "Tor Vergata")
# Copyright (C) 2017 Stefano Salsano - (CNIT and University of Rome "Tor Vergata")
# Copyright (C) 2017 Alessandro Masci - (University of Rome "Tor Vergata")
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
# Topology Parser for Segment Routing IPv6
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
# @author Alessandro Masci <mascialessandro89@gmail.com>
#

import os
import json
import sys
from topo_parser_utils import Subnet
import re
from topo_parser import TopoParser


class SRv6TopoParser(TopoParser):
    path = ""

    # Init Function, load json_data from path_json
    def __init__(self, path_json, openbaton_path_json, verbose=False, version=2):
        self.verbose = verbose
        self.version = int(version)
        self.servers = []
        self.servers_properties = []
        self.routers = []
        self.routers_properties = []
        self.routers_dict = {}
        self.edge_links = []
        self.edge_links_properties = []
        self.core_links = []
        self.core_links_properties = []

        self.vnf_term_dict = {}

        self.ip_addr_map = {}

        self.vims = []
        #self.vm_testbed_map = {}
   
        self.parsed = False

        if self.verbose:
            print "*** __init__: version topology format:", self.version
        path_json = self.path + path_json
        if os.path.exists(path_json) == False:
            print "Error Topo File %s Not Found" % path_json
            sys.exit(-2)
        json_file = open(path_json)
        self.json_data = json.load(json_file)
        json_file.close()
        if self.verbose:
            print "*** JSON Data Loaded:"
            # print json.dumps(self.json_data, sort_keys=True, indent=4)

        self.ob_json_data = {}
        openbaton_path_json = self.path + openbaton_path_json
        if os.path.exists(path_json) == False:
            print "Openbaton Json File %s Not Found" % openbaton_path_json
        
        else:
            ob_json_file = open(openbaton_path_json)
            self.ob_json_data = json.load(ob_json_file)
            ob_json_file.close()


    # Parse Function, first retrieves the vertices from json data,
    # second retrieves the links from json data
    def parse_data(self):
        self.load_advanced()
        self.load_vertex()
        self.load_edge_links()
        self.load_core_links()
        self.load_vnfs_and_terms()
        self.load_vm_testbeds()

        self.load_openbaton()

        self.parsed = True

    # Function used for retrieve routers from json data
    def getRouters(self):
        if self.parsed == False:
            self.parse_data()
        return self.routers

    # Function used for retrieve servers from json data
    def getServers(self):
        if self.parsed == False:
            self.parse_data()
        return self.servers

    # Function used for retrieve edge links from json data
    def getEdge(self):
        if self.parsed == False:
            self.parse_data()
        return self.edge_links

    # Function used for retrieve core links from json data
    def getCore(self):
        if self.parsed == False:
            self.parse_data()
        return self.core_links

    # Function used for retrieve vnf and term dictionary for each vertex
    def getVNFandTERMdict(self, id):
        if self.parsed == False:
            self.parse_data()

        return self.routers_dict[id]['vnfs_and_terms']


    # Function used for retrieve vnf number for each vertex
    # deprecated
    # def getVNF(self, id):
    #     if self.parsed == False:
    #         self.parse_data()
    #     vertices = self.json_data['vertices']
    #     for vertex in vertices:
    #         if vertex['id'] == id:
    #             return vertex['info']['property']['vnf']

    # # Function used for retrieve vnf number for each vertices
    # def getTER(self, id):
    #     if self.parsed == False:
    #         self.parse_data()
    #     vertices = self.json_data['vertices']
    #     for vertex in vertices:
    #         if vertex['id'] == id:
    #             return vertex['info']['property']['ter']

    # Parses topology advanced options
    def load_advanced(self):
        if self.verbose:
            print "*** Retrieve Advanced Option"
        advanced_options = self.json_data['graph_parameters'] if 'graph_parameters' in self.json_data else []
        if 'tunneling' not in advanced_options:
            print "Error No Tunneling Data"
            sys.exit(-2)
        self.tunneling = advanced_options['tunneling']
        if self.tunneling == "":
            self.tunneling = "VXLAN"
        if 'testbed' not in advanced_options:
            print "Error No Testbed Data"
            sys.exit(-2)
        testbeds_types = ["MININET", "SOFTFIRE"]
        testbed = advanced_options['testbed']
        if testbed not in testbeds_types:
            print "%s Not Supported" % testbed
            sys.exit(-2)
        self.testbed = testbed

    # Parses vertex from json_data, renames the node in 'vertices' and in 'edges',
    # and divides them in: Server and Router
    def load_vertex(self):
        if self.version == 2:
            return self.load_vertex_v2()
        if self.verbose:
            print "*** Retrieve Vertex"
        vertices = self.json_data['vertices']
        for vertex in vertices:
            curvtype = vertices[vertex]['info']['type']
            curvproperty = vertices[vertex]['info']['property']
            if 'Server' in curvtype:
                number = map(int, re.findall(r'\d+', vertex))
                self.servers.append('Server%s' % number[0])
                self.servers_properties.append(curvproperty)
            elif 'Router' in curvtype:
                number = map(int, re.findall(r'\d+', vertex))
                self.routers.append('Router%s' % number[0])
                self.routers_properties.append(curvproperty)
        if self.verbose:
            print "*** Servers:", self.servers
            print "*** Routers:", self.routers

    def load_vertex_v2(self):
        if self.verbose:
            print "*** Retrieve Vertex"
        vertices = self.json_data['vertices']
        for vertex in vertices:
            curvtype = vertex['info']['type']
            #curvproperty = vertex['info']['property']
            curvproperty = vertex['info'].get('property', {})
            if 'Server' in curvtype:
                self.servers.append(str(vertex['id']))
                self.servers_properties.append(curvproperty)
            elif 'VM' in curvtype:
                self.routers.append(str(vertex['id']))
                self.routers_properties.append(curvproperty)
                self.routers_dict[str(vertex['id'])]=curvproperty
            elif 'Testbed' in curvtype:
                self.vims.append(str(vertex['id']))
            elif 'ovnf_netns' in curvtype:
                self.vnf_term_dict[str(vertex['id'])]=curvproperty
                self.vnf_term_dict[str(vertex['id'])]['type']='ovnf_netns'
            elif 'ovnf_lxdcont' in curvtype:
                self.vnf_term_dict[str(vertex['id'])]=curvproperty
                self.vnf_term_dict[str(vertex['id'])]['type']='ovnf_lxdcont'
            elif 'term_netns' in curvtype:
                self.vnf_term_dict[str(vertex['id'])]=curvproperty
                self.vnf_term_dict[str(vertex['id'])]['type']='term_netns'
            elif 'term_lxdcont' in curvtype:
                self.vnf_term_dict[str(vertex['id'])]=curvproperty
                self.vnf_term_dict[str(vertex['id'])]['type']='term_lxdcont'
        if self.verbose:
            print "*** Servers:", self.servers
            print "*** Routers:", self.routers
            print "*** Routers dict:", self.routers_dict
            print "*** vnf_term_dict:", self.vnf_term_dict

    # Parses edge_links from json_data
    def load_edge_links(self):
        if self.verbose:
            print "*** Retrieve Edge Links"
        edges = self.json_data['edges']
        for edge in edges:
            if edge['source'] in self.servers or edge['target'] in self.servers:
                    self.edge_links.append((str(edge['source']), str(edge['target'])))
        for edge_link in self.edge_links:
            if edge_link[0] not in self.routers and edge_link[1] not in self.servers:
                print "Error: malformed topology"
                sys.exit(-2)
        if self.verbose:
            print "*** Edgelinks:", self.edge_links

    # Parses core_links from json_data
    def load_core_links(self):
        if self.verbose:
            print "*** Retrieve Core Links"
        edges = self.json_data['edges']
        for edge in edges:
            if edge['source'] in self.routers and edge['target'] in self.routers:
                self.core_links.append((str(edge['source']), str(edge['target'])))
        if self.verbose:
            print "*** Corelinks:", self.core_links

    """Parses vnfs and terms from json_data
    needs to be called after load_vertex

    the routers_dict[myrouter]['vnfs_and_terms'] has the following structure:
    {'vnf1': {'type': TYPE, 'key1':'value1'}}
    """
    def load_vnfs_and_terms(self):
        if self.verbose:
            print "*** Retrieve Vnfs and Terms"
        edges = self.json_data['edges']
        for edge in edges:
            myrouter = ""
            myvnf_ter = ""
            if (edge['source'] in self.routers and edge['target'] in self.vnf_term_dict):
                myrouter = str(edge['source'])
                myvnf_ter = str(edge['target'])
            if (edge['target'] in self.routers and edge['source'] in self.vnf_term_dict) :
                myrouter = str(edge['target'])
                myvnf_ter = str(edge['source'])
            if myrouter != "" :  
                if 'vnfs_and_terms' in self.routers_dict[myrouter] :
                    self.routers_dict[myrouter]['vnfs_and_terms'][myvnf_ter]=self.vnf_term_dict[myvnf_ter]
                else :
                    self.routers_dict[myrouter].update({'vnfs_and_terms':{myvnf_ter:self.vnf_term_dict[myvnf_ter]}})
        if self.verbose:
            print "*** Routers dict updated:", self.routers_dict

    def load_openbaton(self):
        if self.ob_json_data != {} :
            for myvnf in self.ob_json_data ['payload']['vnfr']:
                #print "\n**********"
                #print myvnf['name']
                #print myvnf['vdu'][0]['vnfc_instance'][0]['ips'][0]['ip']
                #print myvnf['vdu'][0]['vnfc_instance'][0]['floatingIps'][0]['ip']
                ip_dict = {}
                ip_dict.update({'internal_ip':str(myvnf['vdu'][0]['vnfc_instance'][0]['ips'][0]['ip'])})
                ip_dict.update({'floating_ip':str(myvnf['vdu'][0]['vnfc_instance'][0]['floatingIps'][0]['ip'])})
                self.ip_addr_map[str(myvnf['name'])]=ip_dict
        if self.verbose:
            print "*** IP address map: \n", self.ip_addr_map


    def load_vm_testbeds(self):
        if self.verbose:
            print "*** Retrieve VM to tesbed map"
        edges = self.json_data['edges']
        for edge in edges:
            myrouter = ""
            mytestbed = ""
            if (edge['source'] in self.routers and edge['target'] in self.vims):
                myrouter = str(edge['source'])
                mytestbed = str(edge['target'])
            if (edge['target'] in self.routers and edge['source'] in self.vims) :
                myrouter = str(edge['target'])
                mytestbed = str(edge['source'])
            if myrouter != "" :  
                self.routers_dict[myrouter].update({'vim':mytestbed})
        if self.verbose:
            print "*** VM to tesbed map:", self.routers_dict

        
if __name__ == '__main__':

    #parser = SRv6TopoParser("example_srv6_topology.json", verbose=True, version=2)
    #parser = SRv6TopoParser("example_lombardo.json", "openbaton_notification.json", verbose=True, version=2)
    parser = SRv6TopoParser("rdcl4nodesok.json", "openbaton_notification.json", verbose=True, version=2)
    parser.parse_data()
    print "*** Nodes:"
    for router, router_property in zip(parser.routers, parser.routers_properties):
        print "*** Router: %s - Property: %s" % (router, router_property)
    for server, server_property in zip(parser.servers, parser.servers_properties):
        print "*** Server: %s - Property: %s" % (server, server_property)
    print "*** Core Links"
    for core_link in parser.core_links:
        print "*** Core Link:", core_link
    print "*** Edge Links"
    for edge_link in parser.edge_links:
        print "*** Edge Link:", edge_link
    print "*** Tunneling", parser.tunneling
    print "*** Testbed", parser.testbed

