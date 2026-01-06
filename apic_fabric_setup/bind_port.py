import credentials
from acitoolkit import acitoolkit as aci

session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
session.login()

# 1. Access the existing hierarchy
tenant = aci.Tenant('Lab-Tenant-Ahmad')
app    = aci.AppProfile('Web-App', tenant)
epg    = aci.EPG('Web-Servers', app)

# 2. Define the Physical Path (Leaf 101, Eth 1/10)
# Note: On the DevNet Sandbox, use '101', '1', '10'
intf = aci.Interface('eth', '1', '101', '1', '10')

# 3. Create the Static Binding with a VLAN encapsulation
vlan_id = '100'
static_binding = aci.L2Interface('binding', 'vlan', vlan_id)
static_binding.add_interface(intf)
epg.add_static_path(static_binding)

# 4. Push to APIC
resp = session.push_to_apic(tenant.get_url(), tenant.get_json())

if resp.ok:
    print(f"✅ Success: EPG 'Web-Servers' is now bound to Leaf 101, Port 1/10 on VLAN {vlan_id}")
else:
    print(f"❌ Error: {resp.text}")
