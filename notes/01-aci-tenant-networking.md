| Traditional Concept          | ACI Equivalent            | Purpose                                                                                |
| :--------------------------- | :------------------------ | :------------------------------------------------------------------------------------- |
| Routing Table / VRF          | **VRF** (or Context)      | Provides Layer 3 isolation. A separate routing domain.                                 |
| VLAN                         | **Bridge Domain (BD)**    | Provides a Layer 2 broadcast domain. A container for MAC addresses.                    |
| IP Subnet / SVI              | **Subnet**                | Defines an IP address range and provides the default gateway for endpoints.            |
| Access Control List (ACL)    | **Contract** & **Filter** | Defines which groups are allowed to talk to each other and over which ports/protocols. |
| A group of servers in a VLAN | **End-Point Group (EPG)** | A group of endpoints that share the same policy requirements.                          |



#Visualizing the Hierarchy from Your Notes
   hierarchical model of the MIT. This shows how the objects are nested within each other.
This covers the Networking Objects

Tenant
└─── VRF (Context)
     │
     └─── Bridge Domain (BD)
          │   │
          │   └─── Subnet 1 (Gateway IP)
          │   │
          │   └─── Subnet 2 (Gateway IP)
          │   │
          │   └─── Subnet 3 (Gateway IP)
          │
          └─── Bridge Domain (BD)
              │
              └─── Subnet 4 (Gateway IP)



#Now let's layer in the Policy Objects.
The policy objects live in parallel to the networking objects but are associated with them.


Tenant
├─── Networking Objects
│    └─── VRF
│         └─── Bridge Domain
│              └─── Subnet
│
└─── Policy Objects
     └─── Application Profile (ap)
          │
          └─── End-Point Group (EPG)  <--- (Associated with one Bridge Domain)
          │    │
          │    └─── Endpoint (a VM/server)
          │    │
          │    └─── Endpoint
          │
          └─── End-Point Group (EPG)
               │
               └─── Endpoint

     └─── Contracts
          └─── Contract
               └─── Subject
                    └─── Filter (e.g., TCP Port 443)
