import credentials
from acitoolkit import acitoolkit as aci

# 1. Session Setup
session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
session.login()

# 2. Re-create the parent objects (Toolkit will match them by name)
tenant = aci.Tenant('Lab-Tenant-Ahmad')
app_ptr = aci.AppProfile('Web-App', tenant)
epg = aci.EPG('Web-Servers', app_ptr)

# 3. Connect the EPG to your existing Bridge Domain
bd = aci.BridgeDomain('Lab-BD', tenant)
epg.add_bd(bd)

# 4. Push only the new AppProfile and EPG
resp = session.push_to_apic(tenant.get_url(), tenant.get_json())

if resp.ok:
    print(f"Successfully added AppProfile '{app_ptr.name}' and EPG '{epg.name}'")
else:
    print(f"Failed to push: {resp.text}")
