# 🚀 Cisco ACI Programmability Lab: Fabric Setup

This repository contains the automation scripts used to provision a multi-tier application environment in the **Cisco ACI DevNet Sandbox**.

---

## 🛠️ Achievements & Progress

### 🔹 Logical Object Creation
* **Tenant Provisioning:** Created `Lab-Tenant-Ahmad` as the primary administrative boundary.
* **Application Profile:** Defined `Web-App` to group related security and networking policies.
* **EPG Creation:** Initialized the `Web-Servers` Endpoint Group to act as the destination for our physical workloads.

### 🔹 Physical Fabric Binding
* **Interface Mapping:** Successfully mapped **Leaf 101, Port 1/10** to the logical EPG.
* **VLAN Encapsulation:** Configured **VLAN 100** for the static path binding to ensure proper L2 identification on the wire.

### 🔹 Resilient Automation
* **API Transition:** Pivoted from `acitoolkit` abstractions to the **Native REST API (Raw JSON)**. 
* **Why?** This bypasses Python library serialization constraints, ensuring successful and reliable fabric deployment.

---

## ✅ Verification & Troubleshooting

* **Automated Auditing:** Developed `check_bindings.py` using raw API queries to verify that the APIC **Managed Information Tree (MIT)** accurately reflects the intended configuration.
* **GUI Validation:** Confirmed all settings via the APIC Web Interface under the *Static Ports* operational tab.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `bind_port.py` | Script using native REST API to bind physical ports to EPGs. |
| `check_bindings.py` | Verification script to audit active fabric bindings. |
| `credentials.py` | Environment-specific APIC access details (Excluded via `.gitignore`). |

---

