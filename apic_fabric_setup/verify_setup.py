import credentials
from acitoolkit import acitoolkit as aci

session = aci.Session(credentials.URL, credentials.USER, credentials.PASSWORD)
session.login()

# Search for the specific tenant you created
tenants = aci.Tenant.get(session)

for t in tenants:
    if t.name == 'Lab-Tenant-Ahmad':
        print(f"✅ Verified: {t.name} exists on the APIC.")
        
        # Check for VRFs inside this tenant
        vrfs = aci.Context.get(session, t)
        for v in vrfs:
            print(f"   -> VRF found: {v.name}")
            
        # Check for Bridge Domains inside this tenant
        bds = aci.BridgeDomain.get(session, t)
        for b in bds:
            print(f"   -> BD found: {b.name}")
