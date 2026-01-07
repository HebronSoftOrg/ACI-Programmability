import credentials
import requests

# 1. Login to get token
login_url = f"{credentials.URL}/api/aaaLogin.json"
login_payload = {"aaaUser": {"attributes": {"name": credentials.USER, "pwd": credentials.PASSWORD}}}
requests.packages.urllib3.disable_warnings()
s = requests.Session()
login_resp = s.post(login_url, json=login_payload, verify=False)
token = login_resp.json()['imdata'][0]['aaaLogin']['attributes']['token']

# 2. Query for Static Path Bindings in your specific EPG
# We use a query filter to look for 'fvRsPathAtt' objects
url = f"{credentials.URL}/api/node/mo/uni/tn-Lab-Tenant-Ahmad/ap-Web-App/epg-Web-Servers.json?query-target=children&target-subtree-class=fvRsPathAtt"

resp = s.get(url, cookies={"APIC-Cookie": token}, verify=False)
data = resp.json()['imdata']

print(f"Inspecting EPG: Web-Servers (via Raw API)")
print("-" * 40)

if not data:
    print("❌ No static bindings found in the APIC database.")
else:
    for item in data:
        attributes = item['fvRsPathAtt']['attributes']
        path = attributes['tDn']
        vlan = attributes['encap']
        print(f"✅ Found Binding: {path}")
        print(f"   Encap: {vlan}")
