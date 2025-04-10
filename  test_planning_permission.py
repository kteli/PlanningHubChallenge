#!/usr/bin/env python3
"""
Automated Test Suite for Planning Permission Decision Logic with Four Height Categories

This file contains unit tests for the get_planning_permission_decision function.
It covers all scenarios described in the decision matrix, including:
  - Universal conditions triggering immediate permission.
  - Various combinations of structure type (fence, wall, gate), location (adjacent vs. not_adjacent),
    and height (all four categories: up_to_1m, above_1m, up_to_2m, and above_2m).
  - The effect of additional modifiers like new build property and PD rights removal.
"""

import unittest
from planning_permission import get_planning_permission_decision


class TestPlanningPermissionDecision(unittest.TestCase):
    """Test cases for planning permission decision logic with 4 height categories."""

    # -----------------------
    # Universal Condition Tests
    # -----------------------
    def test_universal_listed_building(self):
        """If the property is listed, permission is required regardless of other parameters."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="up_to_1m",
            structure_type="fence",
            listed_building=True,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    def test_universal_face_listed_building(self):
        """If the enclosure faces a property with a listed building, permission is required."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="up_to_1m",
            structure_type="wall",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=True,  # 2U9 condition triggered
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    # -----------------------
    # Non-Universal Cases for Fences (Adjacent)
    # -----------------------
    def test_adjacent_fence_up_to_1m(self):
        """An adjacent fence with height 'up_to_1m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="up_to_1m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_adjacent_fence_above_1m(self):
        """An adjacent fence with height 'above_1m' should require permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="above_1m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    def test_adjacent_fence_up_to_2m(self):
        """An adjacent fence with height 'up_to_2m' (i.e. above 1m but not beyond 2m) requires permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="up_to_2m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    def test_adjacent_fence_above_2m(self):
        """An adjacent fence with height 'above_2m' requires permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="above_2m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    # -----------------------
    # Non-Universal Cases for Fences (Not Adjacent)
    # -----------------------
    def test_non_adjacent_fence_up_to_1m(self):
        """A non-adjacent fence with height 'up_to_1m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="up_to_1m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_non_adjacent_fence_above_1m(self):
        """A non-adjacent fence with height 'above_1m' is permitted (N) since it is still below 2m."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="above_1m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_non_adjacent_fence_up_to_2m(self):
        """A non-adjacent fence with height 'up_to_2m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="up_to_2m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_non_adjacent_fence_above_2m(self):
        """A non-adjacent fence with height 'above_2m' requires permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="above_2m",
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    # -----------------------
    # Non-Universal Cases for Walls
    # -----------------------
    def test_wall_up_to_1m(self):
        """A wall with height 'up_to_1m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",  # Location is less important for walls.
            height_of_enclosure="up_to_1m",
            structure_type="wall",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_wall_above_1m(self):
        """A wall with height 'above_1m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="above_1m",
            structure_type="wall",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_wall_up_to_2m(self):
        """A wall with height 'up_to_2m' is permitted (N)."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="up_to_2m",
            structure_type="wall",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_wall_above_2m(self):
        """A wall with height 'above_2m' requires permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="above_2m",
            structure_type="wall",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    # -----------------------
    # Cases for Gates with New Build Restrictions
    # -----------------------
    def test_gate_non_new_build(self):
        """A gate on a non-new build property is permitted (N), regardless of height."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",  # For gates, location is less critical.
            height_of_enclosure="up_to_1m",  # Height is not used for gate logic.
            structure_type="gate",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "N")

    def test_gate_new_build(self):
        """A gate on a new build property requires permission (Y)."""
        result = get_planning_permission_decision(
            location_of_enclosure="not_adjacent",
            height_of_enclosure="up_to_1m",  # Height irrelevant for gate decision.
            structure_type="gate",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=True,
            pd_removed_by_previous_planning=False,
        )
        self.assertEqual(result, "Y")

    # -----------------------
    # Test Modifier: PD Rights Removed by Previous Planning
    # -----------------------
    def test_pd_removed_overrides(self):
        """If PD rights are removed by previous planning, permission is required (Y) regardless of baseline."""
        result = get_planning_permission_decision(
            location_of_enclosure="adjacent",
            height_of_enclosure="up_to_1m",  # Normally permitted for an adjacent fence.
            structure_type="fence",
            listed_building=False,
            article_2_3_land=False,
            article_2_4_land=False,
            article_4_directive=False,
            aonb=False,
            works_affecting_tpo=False,
            face_listed_building=False,
            new_build_property=False,
            pd_removed_by_previous_planning=True,  # Override flag
        )
        self.assertEqual(result, "Y")


if __name__ == "__main__":
    unittest.main(verbosity=2)
