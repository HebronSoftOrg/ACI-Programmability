## Automating ACI with Python: The `acitoolkit`

While ACI can be automated with any language that speaks REST, Python is the most common 
choice. Cisco provides two primary Python libraries for this purpose.

### ACI Python Libraries

1.  **Cobra SDK:**
    *   A low-level, comprehensive SDK generated directly from the ACI Management Information Model (MIT).
    *   **Use Case:** Advanced development requiring access to all objects and attributes. It is powerful but complex.

2.  **`acitoolkit`:**
    *   A high-level, user-friendly library focused on simplifying common, day-to-day operational tasks.
    *   **Use Case:** The recommended starting point for ACI automation. Perfect for retrieving information, monitoring, and basic configuration changes.

---

### Example: Using `acitoolkit` to List Endpoints

The following script demonstrates the power and simplicity of the `acitoolkit`. Its goal is to log in to the APIC and print a formatted table of all learned endpoints and their parent objects.

#### Script Workflow Explained

**1. Setup and Login**
*   The script imports the `acitoolkit` library.
*   It uses `aci.Session(URL, USER, PASS)` to create a session object.
*   The `SESSION.login()` method handles the entire authentication process in the background (building the `aaaUser` JSON payload and managing the session cookie).
*   It includes a simple `if not RESP.ok:` check to gracefully exit if the login fails.

**2. Retrieve Data**
*   A single, powerful line of code is used to get the data:
    ```python
    ENDPOINTS = aci.Endpoint.get(SESSION)
    ```
*   This function abstracts away the underlying REST API call. It queries the APIC and parses the JSON response into a list of Python `Endpoint` objects.

**3. Process and Display Data**
*   The script loops through each `Endpoint` object in the `ENDPOINTS` list.
*   It uses the intuitive `.get_parent()` method to navigate up the MIT hierarchy:
    *   `epg = EP.get_parent()` gets the EPG that contains the endpoint.
    *   `app_profile = epg.get_parent()` gets the Application Profile that contains the EPG.
    *   `tenant = app_profile.get_parent()` gets the Tenant that contains the Application Profile.
*   Finally, it prints the desired attributes from each object (e.g., `EP.mac`, `tenant.name`) in a clean, formatted table.

#### Key Takeaway

The `acitoolkit` demonstrates the power of a good SDK. It allows the developer to think in terms of ACI objects (`Endpoint`, `EPG`) and their relationships (`.get_parent()`) rather than the low-level mechanics of HTTP requests, JSON parsing, and cookie management.


### Example: Creating Objects with `acitoolkit`

The `acitoolkit` simplifies not only reading data but also creating new configurations on the APIC. The workflow follows a "define, then push" model.

#### Script Workflow Explained

**1. Authentication**
*   First, a `Session` object is created and a `.login()` is performed to authenticate with the APIC and obtain a session cookie. Best practice is to store credentials in a separate `credentials.py` file and import them.

**2. Define Desired State (In-Memory)**
*   The script creates instances of toolkit classes like `aci.Tenant`, `aci.Context` (VRF), and `aci.BridgeDomain`.
*   **Crucially, no API calls are made at this stage.** These are just Python objects in local memory.
*   Parent-child relationships are defined by passing the parent object during creation (e.g., `aci.Context('Lab-VRF', tenant)`).
*   Relational links are made using helper methods (e.g., `bd.add_context(vrf)` links a Bridge Domain to a VRF).

**3. Push to APIC**
*   The top-level object (in this case, `tenant`) is used to generate the full configuration.
*   The `.get_json()` method serializes the entire object hierarchy (tenant and all its children) into a single JSON payload.
*   The `session.push_to_apic(url, json_payload)` method sends the configuration to the APIC in a single `HTTP POST` request.
*   The script then checks the response's status code to confirm if the configuration was accepted.

This approach demonstrates the power of Infrastructure as Code (IaC): the Python script becomes the single source of truth for the desired network configuration.
