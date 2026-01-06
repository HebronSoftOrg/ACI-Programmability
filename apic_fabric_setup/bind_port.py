import credentials
import requests
import json

# 1. Login to get a token (since toolkit methods are failing)
login_url = f"{credentials.URL}/api/aaaLogin.json"
login_payload = {
    "aaaUser": {
        "attributes": {
            "name": credentials.USER,
            "pwd": credentials.PASSWORD
        }
    }
}

requests.packages.urllib3.disable_warnings()
s = requests.Session()
login_resp = s.post(login_url, json=login_payload, verify=False)
token = login_resp.json()['imdata'][0]['aaaLogin']['attributes']['token']

# 2. Define the exact path for the Static Port
# This targets Lab-Tenant-Ahmad -> Web-App -> Web-Servers
dist_path_url = f"{credentials.URL}/api/node/mo/uni/tn-Lab-Tenant-Ahmad/ap-Web-App/epg-Web-Servers.json"

# 3. The Raw JSON payload for the Static Path
# This binds Leaf 101, Port 1/10 with VLAN 100
payload = {
    "fvRsPathAtt": {
        "attributes": {
            "dn": "uni/tn-Lab-Tenant-Ahmad/ap-Web-App/epg-Web-Servers/rspathAtt-[topology/pod-1/paths-101/pathep-[eth1/10]]",
            "encap": "vlan-100",
            "status": "created,modified"
        }
    }
}

# 4. Push to APIC
resp = s.post(dist_path_url, json=payload, cookies={"APIC-Cookie": token}, verify=False)

if resp.ok:
    print("✅ SUCCESS: Static Port 1/10 bound to EPG Web-Servers (Raw JSON Push)")
else:
    print(f"❌ Error: {resp.text}")
