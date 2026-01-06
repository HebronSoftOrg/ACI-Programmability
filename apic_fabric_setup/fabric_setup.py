import credentials
from acitoolkit import acitoolkit as aci

# 1. Start Session
session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
if not session.login().ok:
    print("Login Failed")
    exit()

# 2. Create the Objects (The ACI Logical Tree)
tenant = aci.Tenant('Lab-Tenant-Ahmad')
vrf    = aci.Context('Lab-VRF', tenant)
bd     = aci.BridgeDomain('Lab-BD', tenant)
bd.add_context(vrf)  # Link BD to VRF

# 3. Push the configuration to the APIC
resp = session.push_to_apic(tenant.get_url(), tenant.get_json())

if resp.ok:
    print(f"Successfully created Tenant: {tenant.name}")
else:
    print(f"Error: {resp.status_code}")
