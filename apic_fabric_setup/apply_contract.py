import credentials
import requests

# 1. Login and get Token
login_url = f"{credentials.URL}/api/aaaLogin.json"
login_payload = {"aaaUser": {"attributes": {"name": credentials.USER, "pwd": credentials.PASSWORD}}}
requests.packages.urllib3.disable_warnings()
s = requests.Session()
token = s.post(login_url, json=login_payload, verify=False).json()['imdata'][0]['aaaLogin']['attributes']['token']

# 2. Define the Contract and Filter URL (Tenant level)
tenant_url = f"{credentials.URL}/api/node/mo/uni/tn-Lab-Tenant-Ahmad.json"

# 3. Payload to create a 'Permit-All' Filter and Contract
contract_payload = {
    "fvTenant": {
        "attributes": {"dn": "uni/tn-Lab-Tenant-Ahmad"},
        "children": [
            {
                "vzFilter": {
                    "attributes": {"name": "Allow-IP-Filter"},
                    "children": [{"vzEntry": {"attributes": {"name": "Any-IP", "etherT": "ip"}}}]
                }
            },
            {
                "vzBrCP": {
                    "attributes": {"name": "Web-Contract"},
                    "children": [{"vzSubj": {"attributes": {"name": "Subject"},
                                 "children": [{"vzRsSubjFiltAtt": {"attributes": {"tnVzFilterName": "Allow-IP-Filter"}}}]}}]
                }
            }
        ]
    }
}

# 4. Push Contract and then link it to the EPG
s.post(tenant_url, json=contract_payload, cookies={"APIC-Cookie": token}, verify=False)

# Link to EPG as both Provider and Consumer (common for testing)
epg_url = f"{credentials.URL}/api/node/mo/uni/tn-Lab-Tenant-Ahmad/ap-Web-App/epg-Web-Servers.json"
link_payload = {
    "fvAEPg": {
        "attributes": {"dn": "uni/tn-Lab-Tenant-Ahmad/ap-Web-App/epg-Web-Servers"},
        "children": [
            {"fvRsProv": {"attributes": {"tnVzBrCPName": "Web-Contract"}}},
            {"fvRsCons": {"attributes": {"tnVzBrCPName": "Web-Contract"}}}
        ]
    }
}

resp = s.post(epg_url, json=link_payload, cookies={"APIC-Cookie": token}, verify=False)

if resp.ok:
    print("🚀 SUCCESS: 'Web-Contract' created and applied to 'Web-Servers'!")
else:
    print(f"❌ Error: {resp.text}")
