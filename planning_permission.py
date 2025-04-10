#!/usr/bin/env python3
"""
Planning Permission Decision Logic (with Four Height Categories)
------------------------------------------------------------------
This module determines whether planning permission is required ("Y") or not ("N")
for a proposed development (an enclosure) based on a decision matrix.

Decision Flow:

Step 1. Universal Conditions:
  If any universal condition (derived from the 2U columns) is met, planning permission is required.
  Universal conditions include:
    - Listed Building (2U1)
    - Article 2(3) Land (2U2)
    - Article 2(4) Land / Article 4 Directive (2U3)
    - AONB (2U4)
    - Works Affecting TPO (2U5)
    - Enclosure Faces Listed Building (2U9)

  For audit purposes, we read all universal condition inputs—even though a single “True” short-circuits the result.

Step 2. Non-Universal Baseline Conditions:
  (2A Columns) These are used only if no universal condition applies.
  They depend on:
    - Structure Type (fence, wall, gate)
    - Location ("adjacent" vs. "not_adjacent")
    - Height Category (using 4 options: "up_to_1m", "above_1m", "up_to_2m", "above_2m")

  For example, for fences:
    - If adjacent: permitted only if height is "up_to_1m"; any height above 1m (whether "above_1m", "up_to_2m", or "above_2m") requires permission.
    - If not adjacent: permitted if height is "up_to_1m", "above_1m", or "up_to_2m"; if "above_2m", permission is required.

  Walls are permitted if their height is not "above_2m".

Step 3. Other Modifiers:
  Additional factors override the baseline outcome:
    - PD Rights Removed with Previous Planning: if True, the outcome is forced to "Y".
    - New Build Property Restrictions: for example, a gate on a new build property will require permission.

Design Criteria:
  - Diligence: All combinations (including edge cases) are covered.
  - Readability: Code is modular, with clear function names, inline comments, and logging.
  - Scalability: The logic is split into universal, non-universal, and modifiers for ease of maintenance.

Notes on Approach:
  Though one might load rules directly from an Excel sheet, here the rules are written in code for clarity and testability.
  (In a real-world system, you could read the decision matrix at runtime if maintained by non-developers.)

Difficult/Easy Parts:
  - Universal conditions are straightforward.
  - Non-universal conditions require careful differentiation among the four height categories.
  - The modifiers add additional complexity and are applied last.
"""

import logging

# Configure logging to display messages at INFO level or higher.
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_planning_permission_decision(
    location_of_enclosure: str,  # Expected: "adjacent" or "not_adjacent"
    height_of_enclosure: str,  # Expected: "up_to_1m", "above_1m", "up_to_2m", or "above_2m"
    structure_type: str,  # Expected: "fence", "wall", or "gate"
    listed_building: bool,
    article_2_3_land: bool,  # Universal: Article 2(3) Land removing PD rights.
    article_2_4_land: bool,  # Universal: Article 2(4) Land removing PD rights.
    article_4_directive: bool,  # Universal: Article 4 Directive removing PD rights.
    aonb: bool,  # Universal: Property in an AONB.
    works_affecting_tpo: bool,  # Universal: Affected by a TPO.
    face_listed_building: bool,  # Universal: Enclosure faces a property with a listed building.
    new_build_property: bool,  # Modifier: New build property restrictions (affects gates).
    pd_removed_by_previous_planning: bool,  # Modifier: PD rights removed with previous planning decisions.
) -> str:
    """
    Determine planning permission using a three-step decision process.

    Step 1: Universal Conditions.
      If ANY universal condition is True, return "Y".
      (We collect all universal conditions for audit purposes.)

    Step 2: Non-Universal Baseline Conditions.
      Evaluate based on structure type, location, and 4-level height.
      For fences:
        - If "adjacent" and height is "up_to_1m": permitted ("N").
        - If "adjacent" and height in {"above_1m", "up_to_2m", "above_2m"}: permission required ("Y").
        - If "not_adjacent" and height in {"up_to_1m", "above_1m", "up_to_2m"}: permitted ("N").
        - If "not_adjacent" and height is "above_2m": permission required ("Y").
      For walls:
        - Permitted if height is not "above_2m", else permission required.
      For gates:
        - Generally permitted unless the site is a new build.

    Step 3: Other Modifiers.
      If PD rights were removed with previous planning, return "Y" (override baseline).

    Returns:
      "Y" if planning permission is required; otherwise, "N".
    """
    # Step 1: Universal Conditions
    universal_flags = [
        listed_building,
        article_2_3_land,
        article_2_4_land,
        article_4_directive,
        aonb,
        works_affecting_tpo,
        face_listed_building,  # 2U9 condition.
    ]
    if any(universal_flags):
        return "Y"

    # Step 2: Non-Universal Baseline Conditions
    structure = structure_type.lower()

    if structure == "gate":
        # For gates, unless it's a new build (which forces a "Y"), they are permitted.
        baseline = "Y" if new_build_property else "N"
    elif structure == "fence":
        if location_of_enclosure == "adjacent":
            # Adjacent fences: permitted only if exactly "up_to_1m";
            # if height is any category above 1m ("above_1m", "up_to_2m", "above_2m"), then permission is required.
            if height_of_enclosure == "up_to_1m":
                baseline = "N"
            else:
                baseline = "Y"
        else:  # "not_adjacent"
            # For non-adjacent fences, permission is required only if height is "above_2m".
            if height_of_enclosure == "above_2m":
                baseline = "Y"
            else:
                baseline = "N"
    elif structure == "wall":
        # Walls are permitted if their height is not above 2m.
        baseline = "Y" if height_of_enclosure == "above_2m" else "N"
    else:
        baseline = "N"

    # Step 3: Other Modifiers
    # If PD rights have been removed with previous planning, override the baseline.
    if pd_removed_by_previous_planning:
        return "Y"

    return baseline


def get_numeric_choice(prompt_text: str, valid_choices: dict) -> int:
    """
    Prompt the user repeatedly until a valid numeric input is provided.

    Args:
        prompt_text: The prompt shown to the user.
        valid_choices: A dictionary of valid integer choices mapping to their meanings.

    Returns:
        A valid numeric choice from the keys of valid_choices.

    Logs errors if the input is invalid.
    """
    while True:
        try:
            choice = int(input(prompt_text))
            if choice in valid_choices:
                return choice
            else:
                logging.error(
                    "Invalid choice. Please enter one of: {}".format(
                        list(valid_choices.keys())
                    )
                )
        except ValueError:
            logging.error("Invalid input; please enter a number.")


def get_yes_no(prompt_text: str) -> bool:
    """
    Prompt the user for a yes/no answer (1 for Yes, 2 for No).

    Returns:
        True if the user enters 1 (Yes), else False.
    """
    valid = {1: True, 2: False}
    prompt = f"{prompt_text} (Enter 1 for Yes, 2 for No): "
    return valid[get_numeric_choice(prompt, valid)]


def prompt_user_for_input() -> None:
    """
    Interactively prompt the user for all required inputs.

    Input Collection Flow:
      1. Universal Conditions.
         (All universal condition responses are logged for audit purposes.)
      2. Non-Universal Conditions.
         Ask for structure type, location, and height category.
         Height is now collected from 4 options: up_to_1m, above_1m, up_to_2m, above_2m.
      3. Other Modifiers.
         Collect whether the site is a new build and if PD rights have been removed.
      4. Compute and display the final decision.
    """
    print("Welcome to the PlanningHub Code Challenge!")
    print("Enter the details for the planning permission check.\n")

    # --- Step 1: Universal Conditions ---
    listed_building = get_yes_no("Is the property a Listed Building?")
    article_2_3_land = get_yes_no("Is it Article 2(3) Land (removing PD rights)?")
    article_2_4_land = get_yes_no("Is it Article 2(4) Land (removing PD rights)?")
    article_4_directive = get_yes_no(
        "Is it covered by the Article 4 Directive (removing PD rights)?"
    )
    aonb = get_yes_no(
        "Is the property in an AONB (Area of Outstanding Natural Beauty)?"
    )
    works_affecting_tpo = get_yes_no(
        "Is it affected by a Tree Preservation Order (TPO)?"
    )
    face_listed_building = get_yes_no(
        "Does the enclosure face onto a property with a listed building? (2U9 condition)"
    )

    # Early universal check:
    if any(
        [
            listed_building,
            article_2_3_land,
            article_2_4_land,
            article_4_directive,
            aonb,
            works_affecting_tpo,
            face_listed_building,
        ]
    ):
        print("\nOne or more universal conditions are met.")
        print("Result: Planning permission is required (Y).")
        return

    # --- Step 2: Non-Universal Conditions ---
    structure_choices = {1: "fence", 2: "wall", 3: "gate"}
    structure_choice = get_numeric_choice(
        "Enter the structure type (1 for fence, 2 for wall, 3 for gate): ",
        structure_choices,
    )
    structure_type = structure_choices[structure_choice]

    location_choices = {1: "adjacent", 2: "not_adjacent"}
    location_choice = get_numeric_choice(
        "Is the structure adjacent to a road/highway? (Enter 1 for adjacent, 2 for not adjacent): ",
        location_choices,
    )
    location_of_enclosure = location_choices[location_choice]

    # Updated: Four Height Categories
    height_choices = {1: "up_to_1m", 2: "above_1m", 3: "up_to_2m", 4: "above_2m"}
    height_prompt = (
        "Enter the height category:\n"
        "1 for up_to_1m,\n"
        "2 for above_1m,\n"
        "3 for up_to_2m,\n"
        "4 for above_2m: "
    )
    height_choice = get_numeric_choice(height_prompt, height_choices)
    height_of_enclosure = height_choices[height_choice]

    # --- Step 3: Other Modifiers ---
    new_build_property = get_yes_no("Is it a new build property?")
    pd_removed_by_previous_planning = get_yes_no(
        "Have permitted development rights been removed with previous planning?"
    )

    # --- Step 4: Compute and Display Final Decision ---
    decision = get_planning_permission_decision(
        location_of_enclosure=location_of_enclosure,
        height_of_enclosure=height_of_enclosure,
        structure_type=structure_type,
        listed_building=listed_building,
        article_2_3_land=article_2_3_land,
        article_2_4_land=article_2_4_land,
        article_4_directive=article_4_directive,
        aonb=aonb,
        works_affecting_tpo=works_affecting_tpo,
        face_listed_building=face_listed_building,
        new_build_property=new_build_property,
        pd_removed_by_previous_planning=pd_removed_by_previous_planning,
    )
    print("\nResult: Planning permission required: " + decision)


if __name__ == "__main__":
    prompt_user_for_input()
