import credentials
from acitoolkit import acitoolkit as aci

session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
session.login()

# 1. Access the existing hierarchy
tenant = aci.Tenant('Lab-Tenant-Ahmad')
app    = aci.AppProfile('Web-App', tenant)
epg    = aci.EPG('Web-Servers', app)

# 2. Define the Physical Interface
intf = aci.Interface('eth', '1', '101', '1', '10')

# 3. Create the Static Binding properly
# In acitoolkit, you create an L2Interface, attach the physical interface,
# and then add that L2Interface as a child of the EPG.
vlan_id = '100'
static_binding = aci.L2Interface('vlan' + vlan_id, 'vlan', vlan_id)
static_binding.attach(intf)

# The correct method for an EPG to hold a static path is .add_child()
epg.add_child(static_binding)
