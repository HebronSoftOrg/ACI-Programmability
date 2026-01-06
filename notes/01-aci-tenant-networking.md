# ACI Tenant Networking Components

This document summarizes the core networking and policy objects within a Cisco ACI Tenant, translating traditional concepts to the ACI model and illustrating their hierarchy.

---

## Translation: Traditional vs. ACI Concepts

This table maps familiar networking concepts to their ACI equivalents.

| Traditional Concept | ACI Equivalent | Purpose |
| :--- | :--- | :--- |
| Routing Table / VRF | **`VRF`** (or Context) | Provides Layer 3 isolation. A separate routing domain. |
| VLAN | **`Bridge Domain` (BD)** | Provides a Layer 2 broadcast domain. A container for MAC addresses. |
| IP Subnet / SVI | **`Subnet`** | Defines an IP address range and provides the default gateway. |
| Access Control List (ACL) | **`Contract`** & **`Filter`** | Defines which groups can talk and over which ports/protocols. |
| Group of servers in a VLAN | **`End-Point Group` (EPG)** | A group of endpoints that share the same security policy. |

---

## ACI Object Hierarchy

The ACI Management Information Tree (MIT) organizes all logical components within a `Tenant`.

### 1. Networking Objects (The "Where")

This tree shows how the L2/L3 forwarding domains are structured. A `VRF` is a container for `Bridge Domains`, which in turn are containers for `Subnets`.

```text
Tenant
└─── VRF (Context)
     │
     └─── Bridge Domain (BD)
          │   │
          │   ├─── Subnet 1 (Gateway IP)
          │   └─── Subnet 2 (Gateway IP)
          │
          └─── Bridge Domain (BD)
              │
              └─── Subnet 3 (Gateway IP)


### 2. Policy Objects (The "Who" and "How")

This tree shows the policy structure. Application Profiles are containers for End-Point Groups (EPGs). Contracts exist in parallel to define the communication rules between EPGs.
These objects define security and communication rules.

Tenant
├─── Application Profile (AP)
│    │
│    └─── End-Point Group (EPG)
│         │
│         └─── Endpoint (e.g., a VM or server)
│
├─── Contracts
│    │
│    └─── Contract
│         │
│         └─── Subject
│              │
│              └─── Filter (e.g., TCP Port 443)
│
└─── Networking Objects (VRF, BD, etc. from above)

---

## Key Relationships & Rules

Understanding the links between these objects is critical.

1.  **EPG is linked to one BD:** An `EPG` must be associated with exactly one `Bridge Domain`. This places all endpoints in the EPG into a specific L2 broadcast domain.

2.  **BD can have multiple Subnets:** Unlike a traditional VLAN, a `Bridge Domain` can contain multiple subnets, and the fabric will correctly route between them.

3.  **Contracts enable communication:** By default, no traffic is allowed between EPGs (a zero-trust model). Communication is only permitted if a `Contract` is in place between the EPGs.
    *   One EPG **provides** the contract.
    *   The other EPG **consumes** the contract.


