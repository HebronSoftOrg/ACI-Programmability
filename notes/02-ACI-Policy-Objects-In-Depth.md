##  Policy Objects In-Depth

Policy objects define the security posture and communication rules for endpoints. They are the heart of ACI's "application-centric" design.

### Application Profile (AP)

*   **Purpose:** A container or folder for all the EPGs that make up a single, logical application.
*   **Example:** For a typical 3-tier application, one `Application Profile` would contain the `Web`, `App`, and `Database` EPGs.

### End-Point Group (EPG)

The EPG is the **most important object** in the ACI policy model.

*   **Purpose:** A collection of endpoints (servers, VMs, containers) that share common policy requirements.
*   **Core Principle:** Policies are applied to the **EPG as a group**, never to individual endpoints. This provides consistency and scalability.
*   **Critical Rule:** An EPG must be associated with **exactly one** `Bridge Domain`.

### Contracts

Contracts define the rules of communication *between* different EPGs. They are the "firewall rules" of the ACI fabric.

*   **Default Behavior:** Communication between different EPGs is **denied** by default (zero-trust security).
*   **Purpose:** A `Contract` explicitly permits traffic, defining *what* is allowed (e.g., which protocols and ports).
*   **Key Functions:**
    *   Control traffic flow between EPGs.
    *   Redirect traffic to Layer 4-7 services (e.g., firewalls, load balancers).
    *   Apply Quality of Service (QoS) policies.

### Rules of Communication

1.  **Intra-EPG Traffic (Endpoints in the same EPG):**
    *   **Rule:** **Allowed** by default.
    *   **Reason:** Endpoints in the same tier are trusted to communicate freely.

2.  **Inter-EPG Traffic (Endpoints in different EPGs):**
    *   **Rule:** **Denied** by default.
    *   **How to Allow:** A `Contract` must be established between the EPGs.

### The Provider/Consumer Model

This model governs how contracts are applied.

*   **Provider EPG:** The EPG that *offers* a service and exposes a `Contract`.
    *   *Example:* The `Database-EPG` **provides** a "SQL-access" contract.
*   **Consumer EPG:** The EPG that *uses* or initiates communication with a service.
    *   *Example:* The `App-Server-EPG` **consumes** the "SQL-access" contract to talk to the database.

This relationship is directional: the consumer initiates traffic to the provider.

### Visualizing the Provider/Consumer Model

A common use case is a 3-tier web application. The relationship between the EPGs and the Contracts would look like this:

```text
+-----------------------------------------------------------------+
|                 Application Profile: "OnlineStore"              |
|                                                                 |
|  +-----------+         +-----------+         +-----------+      |
|  |   EPG:    |         |   EPG:    |         |   EPG:    |      |
|  |  "Users"  |         |   "Web"   |         |   "App"   |      |
|  +-----------+         +-----------+         +-----------+      |
|       |                     |                     |             |
|       | consumes            | provides            | consumes    |
|       +---------------------+                     +-------------+
|                             |                     |             |
|                   +-------------------+   +-------------------+ |
|                   | Contract:         |   | Contract:         | |
|                   | "Web-Access"      |   | "App-Access"      | |
|                   | (Filter: TCP 443) |   | (Filter: TCP 8080)| |
|                   +-------------------+   +-------------------+ |
|                                                                 |
+-----------------------------------------------------------------+

