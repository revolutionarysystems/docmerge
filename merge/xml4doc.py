import xmltodict
import iso8601
import json
import datetime
#from .testData import xml0, xml1
from .gd_resource_utils import folder_file,file_content_as
from .resource_utils import strip_xml_dec,get_xml_content
import lxml.etree as etree
import re

xml = '''
'''

def parse_as_datetime(str_value):

    try:
        return iso8601.parse_date(str_value)
    except:        
        try:
            str_value=str_value.replace(" ","+")
            return iso8601.parse_date(str_value)
        except:        
            return None

def parse_as_boolean(str):
    try:
        if (str.lower()=="true"):
            return True
        if (str.lower()=="false"):
            return False
        return None
    except:
        return None


def parse_special_values(this_value):
    if not isinstance(this_value, str):
        return this_value
    dt_regex = "\d{4}-[01]\d-[0-3]\d[T\s][0-2]\d:[0-5]\d:[0-5]\d.*" 
    p = re.compile(dt_regex)
    m=p.match(this_value)
    if (m==None):
        return this_value 
    else:
        sv = parse_as_datetime(this_value)
        if sv != None:
            return sv
#    sv = parse_as_boolean(str)  # suppress for now
#        return sv



def force_lists(doc):
    for key in doc.keys():
        node = doc[key]
        force_list = False
        if isinstance(node, dict):
            if "#text" in node.keys():
                doc[key]=node["#text"]
                node = node["#text"]
            elif "@xsi:nil" in node.keys() and node["@xsi:nil"] == "true":
                doc[key]=None
                node = None
            else:
                if ('@list' in node.keys()) and (node['@list']=='true'):
                    force_list = True
                force_lists(node)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict):
                    force_lists(item)
        else:
            sv=parse_special_values(node)
            if not(sv==None):
                doc[key]=sv
                node = sv
        if (key.find("_list"))>=0 or force_list: # force a list if the tag contains _list
            node_name = list(node.keys())[-1] #xmldict will force a single node with a common name -which is ugly
            sublist = node[node_name]
            goodlist = []
            if not node_name=="@list": #exclude the @list attribute
                if isinstance(sublist, list):
                    for item in sublist:
                        goodlist.append(item)
                else:
                    goodlist.append(sublist)
                    #node[node_name]=[sublist,]
            doc[key]=goodlist
    return doc

def alternate_values(doc):
    newValues = {}
    for key in doc.keys():
        node = doc[key]
        if isinstance(node, dict):
            alternate_values(node)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict):
                    alternate_values(item)
        else:
            if key.find("UserId")>=0:
                value = doc[key].replace("-","")
                key_stripped = key+"_stripped"
                newValues[key_stripped]=value
            looks_like_boolean = parse_as_boolean(doc[key])
            if looks_like_boolean != None:
                key_bool = key+"_bool"
                newValues[key_bool]=looks_like_boolean
    for newKey in newValues.keys():
        doc[newKey]=newValues[newKey]
    return doc


def xform_xml(content, local_folder, remote_folder, xform_file):
#    print(type(content))
    if type(content) is bytes:
        content = content.decode("UTF-8")
    content = strip_xml_dec(content)
    dom = etree.fromstring(content)
    xslt = etree.fromstring(get_xml_content(local_folder, remote_folder, xform_file))
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return etree.tostring(newdom, pretty_print=True).decode("utf-8")

def dictify(par_dict, node_name, node_value):
    if node_name.find(".")<0:
        par_dict[node_name]=node_value
        return par_dict
    else:
        root = node_name[:node_name.find(".")]
        remainder = node_name[node_name.find(".")+1:]
        if not (root in par_dict.keys()):
            par_dict[root]={}
        dictify(par_dict[root], remainder, node_value)


def getData(test_case = None, payload=None, payload_type="xml", params = None, data_file=None, remote_data_folder = None, local_data_folder = None, xform_folder = None, xform_file = None):
    data = None
    if payload and payload_type.lower()=="xml":
        if xform_file:
                payload = xform_xml(payload, "transforms", xform_folder, xform_file)
        data = xmltodict.parse(payload)
    elif payload and payload_type=="json":
        data = json.loads(payload)
    elif payload_type == "params" and params:
        data = {}
        for key in params.keys():
            dictify(data, key, params[key])
    elif data_file:
        doc_xml = get_xml_content(local_data_folder, remote_data_folder, data_file)
#        data_doc_id = folder_file(data_folder, data_file)["id"]
#        doc_xml = file_content_as(data_doc_id)
        if xform_file:
            doc_xml = xform_xml(doc_xml, "transforms", xform_folder, xform_file)
        data = xmltodict.parse(doc_xml) 
    if data == None: #default
        data = xmltodict.parse(xml)
    data = force_lists(data)
    data = alternate_values(data)
    return data

#print(json.dumps(getData(), indent=2))


