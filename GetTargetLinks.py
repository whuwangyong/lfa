#!/usr/bin/python
# coding=utf-8

import httplib
import urllib2
import json
import pdb


def simple_json_get(url):
	print 'connecting...'
	return json.loads(urllib2.urlopen(url).read())


DEVICES = simple_json_get('http://localhost:8080/wm/device/all/json') # list
ALL_SW_FLOWS = simple_json_get('http://localhost:8080/wm/core/switch/all/flow/json') # dict
LINKS = simple_json_get('http://localhost:8080/wm/topology/directed-links/json') # list


# considering the priority of flow.......
# return ordered flows
def order_flows_by_priority():
	pass

def getPathFromBoundarySw(start_sw):

	START_SW_FLOWS = ALL_SW_FLOWS.get(start_sw).get("flows") # list
	PATHS=[]

	for flow in START_SW_FLOWS:
		# not considering the mac-level flow
		if(flow.get("match").get("eth_type") == "0x0x806"):
			continue

		# reinitialize
		CURRENT_SW = start_sw
		CURRENT_PORT = 0
		IPV4_SRC = 0
		IPV4_DST = 0
		PATH=[]

		PATH.append(CURRENT_SW)
		IPV4_SRC = flow.get("match").get("ipv4_src")
		IPV4_DST = flow.get("match").get("ipv4_dst")


		find_next_hop = False

		action = flow.get("actions").get("actions")
		output = str(action).split('=')[1]
		CURRENT_PORT = int(output)
		# pdb.set_trace()
		for link in LINKS:
			if (link.get("src-switch")==CURRENT_SW and int(link.get("src-port"))==CURRENT_PORT ):
				CURRENT_SW = link.get("dst-switch")
				CURRENT_PORT = int(link.get("dst-port"))
				find_next_hop = True
				break
		
		while(find_next_hop):
			find_next_hop = False
			PATH.append(CURRENT_SW)
			curr_sw_flows = ALL_SW_FLOWS.get(CURRENT_SW).get("flows") # list
			for curr_sw_flow in curr_sw_flows:
				# not considering the mac-level flow
				if(curr_sw_flow.get("match").get("eth_type") == "0x0x806"):
					continue
				if (IPV4_SRC == curr_sw_flow.get("match").get("ipv4_src") \
					and IPV4_DST == curr_sw_flow.get("match").get("ipv4_dst") \
					and CURRENT_PORT == int(curr_sw_flow.get("match").get("in_port"))):
					# supposing that the each flow only has a output action
					# pdb.set_trace()
					action = curr_sw_flow.get("actions").get("actions")
					output = str(action).split('=')[1]
					CURRENT_PORT = int(output)
					for link in LINKS:
						if (link.get("src-switch")==CURRENT_SW and int(link.get("src-port"))==CURRENT_PORT ):
							# print "link",link
							CURRENT_SW = link.get("dst-switch")
							CURRENT_PORT=int(link.get("dst-port"))
							find_next_hop = True
							break
		if (len(PATH)>1):
			PATHS.append(PATH)
	return PATHS




def getBoundarySws():
	boundary_sws = set([])
	for d in DEVICES:
		if (len(d.get("attachmentPoint"))!=0):
			boundary_sws.add(d.get("attachmentPoint")[0].get("switchDPID"))
	return boundary_sws

def getPath():
	print getBoundarySws()
	for sw in getBoundarySws():
		print getPathFromBoundarySw(sw)

# getPath()


def getTagetLinks(top_K):
	linkWithTimes={}
	for sw in getBoundarySws():
		ll = getPathFromBoundarySw(sw) # [['00:00:01','00:00:02'], ['00:00:03','00:00:05','00:00:06']]
		for l in ll:
			i=0
			while(i<len(l)-1):
				key=str(l[i]+"&"+l[i+1])
				if (key in linkWithTimes):
					linkWithTimes[key] += 1
				else:
					linkWithTimes[key] = 1
				i += 1
	return sorted(linkWithTimes.items(), key=lambda d: d[1], reverse=True)[0:top_K]

print getTagetLinks(10)
