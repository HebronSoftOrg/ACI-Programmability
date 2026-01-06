import credentials
from acitoolkit import acitoolkit as aci

session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
session.login()

# Get the EPG from the APIC
tenant = aci.Tenant('Lab-Tenant-Ahmad')
app = aci.AppProfile('Web-App', tenant)
epg = aci.EPG('Web-Servers', app)

# Fetch all children of the EPG to find the L2Interface (Static Path)
children = aci.EPG.get_children(epg) # This might vary by toolkit version
# Alternative: epg.get(session) 

print(f"Checking bindings for {epg.name}...")
# In a real scenario, you can iterate through children to find L2Interface objects
