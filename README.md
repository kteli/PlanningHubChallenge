# PlanningHub Code Challenge

Welcome to the **PlanningHub Code Challenge** repository! This project contains a Python implementation of planning permission decision logic based on a detailed decision matrix. The code determines whether planning permission is required ("Y") or not ("N") for erecting a fence, gate, or wall given various site and development conditions.

## Overview

The decision logic is divided into three main steps:

### Step 1. Universal Conditions
These conditions override all other criteria. They are derived from the decision matrix’s 2U columns. If any universal condition is met, planning permission is automatically required. Universal conditions include:
  
- **Listed Building (2U1):**  
  The property is a listed building.
  
- **Article 2(3) Land (2U2):**  
  Land designated under Article 2(3) where permitted development rights are removed.
  
- **Article 2(4) Land / Article 4 Directive (2U3):**  
  Land designated under Article 2(4) and/or covered by the Article 4 Directive, removing permitted development rights.
  
- **AONB (2U4):**  
  The property is in an Area of Outstanding Natural Beauty.
  
- **Works Affecting TPO (2U5):**  
  The project affects trees covered by a Tree Preservation Order.
  
- **Enclosure Faces Listed Building (2U9):**  
  The enclosure (gate, fence, wall, or other means of enclosure) faces onto a property with a listed building.

*For audit purposes, the program collects all universal condition inputs—even though a single “True” is sufficient to trigger planning permission. This provides a full record of which conditions were checked and met.*

### Step 2. Non‑Universal Baseline Conditions
(These conditions correspond to the 2A columns in the decision matrix and are only used if none of the universal conditions apply.)

They depend on the following parameters:
- **Structure Type:**  
  (e.g., fence, wall, gate; normalized to lower case)
- **Location:**  
  ("adjacent" vs. "not_adjacent" to a road)
- **Height Category:**  
  Four distinct options are used:
  - `up_to_1m`
  - `above_1m`
  - `up_to_2m`
  - `above_2m`

For example, for fences:
- **Adjacent fences:**  
  Permitted only if the fence is exactly `up_to_1m`.  
  Any height above 1m (whether `above_1m`, `up_to_2m`, or `above_2m`) requires planning permission.
- **Non-adjacent fences:**  
  Permitted if the height is `up_to_1m`, `above_1m`, or `up_to_2m`.  
  Fences `above_2m` require planning permission.

For walls:
- Walls are permitted if their height is not `above_2m`, else permission is required.

For gates:
- Gates are generally permitted unless the property is a new build (see below).

### Step 3. Other Modifiers (Overrides)
These additional factors modify the non‑universal outcome:
- **PD Rights Removed with Previous Planning:**  
  If true, this override forces the outcome to "Y" (permission required), regardless of the baseline decision.
- **New Build Property Restrictions:**  
  For example, a gate on a new build property requires planning permission, even though it might be permitted on a non-new build.

## Project Structure

- **planning_permission.py**  
  Contains the main planning permission decision logic, including functions to process universal conditions, non‑universal conditions (with four height categories), and additional modifiers. The code is modular, well-documented, and uses logging to capture invalid inputs.

- **test_planning_permission.py**  
  Contains the automated test suite using Python’s `unittest` framework. The tests cover all scenarios described in the decision matrix, including:
  - Universal conditions triggering immediate permission.
  - Various combinations of structure type, location, and all four height categories.
  - The effects of additional modifiers like new build property restrictions and PD rights removal.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/PlanningHubChallenge.git
   
   cd PlanningHubChallenge
   ```
2. **Install Required Packages:**

This project requires Python 3.6+ and the following packages:
- pandas
- openpyxl (for reading Excel files, not need for this code atm might need in future)

- Install them via pip:

    ```bash
    pip install pandas openpyxl


# Usage

## Interactive Mode

To run the interactive prompt where you manually input values:

```bash
python planning_permission.py
```


Follow the on-screen prompts to enter universal conditions, non‑universal details (structure type, location, height category), and other modifiers. The system will then output whether planning permission is required.

## Running Automated Tests
To run the automated test suite:
```bash
python test_planning_permission.py
```
The test suite verifies the decision logic against multiple scenarios, including all four height categories.

## Design Rationale

- **Diligence:**
The logic covers all possible combinations of inputs (universal and non‑universal conditions plus modifiers), including edge cases.

- **Modularity & Readability:**
The code is organized into clear, separate functions with descriptive names and detailed comments. Logging is used to flag any invalid inputs, making it easy for team members to understand and maintain.

- **Scalability:**
While the decision rules are currently defined in code for clarity and testability, the design can easily be adapted to load rules from an Excel file if those are maintained by non‑technical team members in the future.

##  Challenges & Considerations
- **Universal Conditions:**
Implementing these is straightforward; any condition being true forces a "Y". However, we continue to record all universal conditions for auditing purposes.

- **Non‑Universal Conditions:**
Distinguishing between four height categories required careful logic, especially for adjacent structures.

- **Modifiers:**
Applying PD rights removal and new build restrictions as overrides adds complexity, but this is essential to reflect the decision matrix accurately.

## Future Enhancements
A possible future enhancement is to load the decision rules directly from an Excel file. This would allow planners or other stakeholders to update the decision matrix without modifying the code itself. The current code is designed to be easily adaptable for such changes.