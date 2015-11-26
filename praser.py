#!/usr/bin/python
# coding=utf-8

import httplib
import urllib2
import json

class StaticFlowPusher(object):
 
    def __init__(self, server):
        self.server = server
 
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
 
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
 
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
 
    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret


def simple_json_get(url):
	print 'connecting...'
	return json.loads(urllib2.urlopen(url).read())


def praser_reactive_flow_and_inseart():
	# with open("/home/wy/all_flow.json", "r") as f:
	# 	d = json.load(f)
	d = simple_json_get('http://localhost:8080/wm/core/switch/all/flow/json')
	print 'length:',len(d)
	# print d.keys()
	pusher = StaticFlowPusher('localhost')
	reactive_flow_prefix = "reactive-flow-"
	i = 0
	for sw in d.iterkeys():
		print sw
		for r_flow in d.get(sw).get("flows"):
			print 'packetCount:', f_flow.get("packetCount")
			print 'byteCount:', r_flow.get("byteCount")
			print 'in_port:', r_flow.get("match").get("in_port")
			print 'ipv4_src:', r_flow.get("match").get("ipv4_src")
			print 'ipv4_dst:', r_flow.get("match").get("ipv4_dst")
			print 'actions:', r_flow.get("actions").get("actions")
			print '====================================='
			if r_flow.get("instructions").get("instruction_apply_actions").get("actions") == "output=controller":
				continue
			if r_flow.get("match").get("eth_type") == "0x0x800" and r_flow.get("flags") == "0": # ip protocl && reactive flow
				i += 1
				flow_name = reactive_flow_prefix + str(i)
				flow = {
					'switch':sw,
					"name":flow_name,
					"active":"true",				
					#"cookie":r_flow.get("cookie"),
					"cookie":0, 
					"priority":r_flow.get("priority"),
					# # "table":r_flow.get("tableId"), 
					"idle_timeout":r_flow.get("idleTimeoutSec"),
					"hard_timeout":r_flow.get("hardTimeoutSec"),
					"in_port":r_flow.get("match").get("in_port"),
					"eth_type":"0x0800",
					"ipv4_src":r_flow.get("match").get("ipv4_src"),
					"ipv4_dst":r_flow.get("match").get("ipv4_dst"),
	    			"actions":r_flow.get("instructions").get("instruction_apply_actions").get("actions")
				}
				# print flow
				# pusher.set(flow)	


praser_reactive_flow_and_inseart()

def print_target_links():
	d = simple_json_get('http://localhost:8080/wm/lfa/targetlinks/json') # list
	print 'target links:'
	print '******************************************'
	for link in d:
		print json.dumps(link, sort_keys=False, indent=4, separators=(',', ': '))
	print '******************************************'

# print_target_links()


def praser_all_flow():
	d = simple_json_get('http://localhost:8080/wm/core/switch/all/flow/json')


def praser_static_flow():
	d = simple_json_get('http://localhost:8080/wm/staticflowpusher/list/all/json')



class Device(object):
	"""docstring for device"""
	def __init__(self, ipv4, dpid, port):
		self.ipv4 = ipv4
		self.dpid = dpid
		self.port = port

class Match(object):
	"""docstring for Match"""
	def __init__(self, ipv4_src, ipv4_dst, in_port):
		self.ipv4_src = ipv4_src
		self.ipv4_dst = ipv4_dst
		self.in_port = in_port
		
class StaticFlow(object):
	"""docstring for StaticFlow"""
	def __init__(self, switch, match, actions):
		self.switch = switch
		self.match = match
		self.actions = actions

class ReactiveFlow(object):
	"""docstring for ReactiveFlow"""
	def __init__(self, switch, match, actions):
		self.switch = switch
		self.match = match
		self.actions = actions
		
class Link(object):
	"""docstring for Link"""
	def __init__(self, src_sw, src_port, dst_sw, dst_port, direction):
		self.src_sw = src_sw
		self.dst_sw = dst_sw
		self.src_port = src_port
		self.dst_port = dst_port
		self.direction = direction
		
		
# considering the priority of flow.......
# return ordered flows
def order_flows_by_priority():
	pass

def get_path():
	path = []
	paths = []

	dvs = simple_json_get('http://localhost:8080/wm/device/') # list
	all_sw_flows = simple_json_get('http://localhost:8080/wm/core/switch/all/flow/json') # dict
	links = simple_json_get('http://localhost:8080/wm/topology/links/json') # list
	external_links = simple_json_get('http://localhost:8080/wm/topology/external-links/json') # list

	for d in dvs:
		ipv4 = d.get("ipv4")[0]
		switchDPID = d.get("attachmentPoint")[0].get("switchDPID")
		port = d.get("attachmentPoint")[0].get("port")
		path.append(ipv4)
		path.append(switchDPID)
		device = Device(ipv4, switchDPID, port)
		flows = all_sw_flows.get(switchDPID).get("flows") # list

		# supposing that the static_flows was ordered by priority
		# supposing that the each static_flow only has a output action
		for flow in flows:
			if flow.get("flags") == "0":
				print 'this is a reactive flow'
			elif flow.get("flags") == "1":
				print 'this is a static flow'
			if  sf.get("match").get("in_port") == device.port:
				ipv4_dst = sf.get("match").get("ipv4_dst")
				actions = sf.get("instructions").get("instruction_apply_actions").get("actions") # list
				for action in actions:
					if str(action).startswith("output="):
						output = str(action).split['='][1]
						print 'output=',output






		


	
	





