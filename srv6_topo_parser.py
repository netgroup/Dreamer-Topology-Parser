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

# !/usr/bin/python

import os
import json
import sys
from topo_parser_utils import Subnet
import re
from topo_parser import TopoParser


class Srv6TopoParser(TopoParser):
    path = ""

    # Init Function, load json_data from path_json
    def __init__(self, path_json, verbose=False, version=2):
        self.verbose = verbose
        self.version = int(version)
        self.server = []
        self.server_properties = []
        self.router = []
        self.router_properties = []
        self.edge_links = []
        self.edge_links_properties = []
        self.core_links = []
        self.core_links_properties = []
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

    # Parse Function, first retrieves the vertices from json data,
    # second retrieves the links from json data
    def parse_data(self):
        self.load_advanced()
        self.load_vertex()
        self.load_edge_links()
        self.load_core_links()
        self.parsed = True

    # Function used for retrieve routers from json data
    def getRouters(self):
        if self.parsed == False:
            self.parse_data()
        return self.router

    # Function used for retrieve servers from json data
    def getServers(self):
        if self.parsed == False:
            self.parse_data()
        return self.server

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

    # Function used for retrieve vnf number for each vertices
    def getVnf(self,id):
        if self.parsed == False:
            self.parse_data()
        vertices = self.json_data['vertices']
        for vertex in vertices:
            if vertex['id'] == id:
                return vertex['info']['property']['vnf']

    # Parses topology advanced options
    def load_advanced(self):
        if self.verbose:
            print "*** Retrieve Advanced Option"
        advanced_options = self.json_data['graph_parameters'] if 'graph_parameters' in self.json_data else []
        if 'testbed' not in advanced_options:
            print "Error No Testbed Data"
            sys.exit(-2)
        testbed = advanced_options['testbed']
        if testbed != "MININET":
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
                self.server.append('Server%s' % number[0])
                self.server_properties.append(curvproperty)
            elif 'Router' in curvtype:
                number = map(int, re.findall(r'\d+', vertex))
                self.router.append('Router%s' % number[0])
                self.router_properties.append(curvproperty)
        if self.verbose:
            print "*** Server:", self.server
            print "*** Router:", self.router

    def load_vertex_v2(self):
        if self.verbose:
            print "*** Retrieve Vertex"
        vertices = self.json_data['vertices']
        for vertex in vertices:
            curvtype = vertex['info']['type']
            curvproperty = vertex['info']['property']
            if 'Server' in curvtype:
                self.server.append(str(vertex['id']))
                self.server_properties.append(curvproperty)
            elif 'Router' in curvtype:
                self.router.append(str(vertex['id']))
                self.router_properties.append(curvproperty)
        if self.verbose:
            print "*** Server:", self.server
            print "*** Router:", self.router

    # Parses edge_links from json_data
    def load_edge_links(self):
        if self.verbose:
            print "*** Retrieve Edge Links"
        edges = self.json_data['edges']
        for edge in edges:
            if edge['source'] in self.server or edge['target'] in self.server:
                    self.edge_links.append((str(edge['source']), str(edge['target'])))
        for edge_link in self.edge_links:
            if edge_link[0] not in self.router and edge_link[1] not in self.server:
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
            if edge['source'] in self.router and edge['target'] in self.router:
                self.core_links.append((str(edge['source']), str(edge['target'])))
        if self.verbose:
            print "*** Corelinks:", self.core_links


if __name__ == '__main__':

    parser = Srv6TopoParser("example_srv6_topology.json", verbose=True, version=2)
    parser.parse_data()

