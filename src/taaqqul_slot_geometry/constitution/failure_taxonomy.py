"""
FailureCode taxonomy — ALL 100 constitutional prohibitions.
Origin: docs/00_MAQOOL_CONSTITUTION.md §7
"""
from enum import Enum


class FailureCode(str, Enum):
    """Exhaustive enumeration of all constitutional failure codes.

    Prefix convention:
      M_00_xx  — L0 violations
      M_01_xx  — L1 violations
      M_02_xx  — L2 violations
      M_03_xx  — L3 violations
      M_CX_xx  — Cross-cutting / constitutional violations
    """

    # ── L0 violations (M_00_xx) ──────────────────────────────────────────────
    M_00_01 = "no_signifier_before_sound"
    M_00_02 = "invalid_phonetic_pattern"
    M_00_03 = "grapheme_not_in_28"
    M_00_04 = "vowel_not_in_7"
    M_00_05 = "syllable_type_not_in_4"
    M_00_06 = "utterance_empty"
    M_00_07 = "binary_jamid_treated_as_derivational_root"
    M_00_08 = "harf_maani_missing_function"
    M_00_09 = "no_leap_between_layers"
    M_00_10 = "rank_promotion_forbidden_in_L0"
    M_00_11 = "missing_trace_ref"
    M_00_12 = "missing_rank_field"
    M_00_13 = "missing_residuals_field"
    M_00_14 = "phoneme_consonant_empty"
    M_00_15 = "phoneme_consonant_not_single_char"
    M_00_16 = "syllable_phoneme_sequence_empty"
    M_00_17 = "syllable_type_mismatch"
    M_00_18 = "signifier_requires_licensed_utterance"
    M_00_19 = "union_signifier_missing"
    M_00_20 = "union_signified_missing"
    M_00_21 = "signification_type_invalid"
    M_00_22 = "weight_pattern_invalid"
    M_00_23 = "jamid_anchor_phoneme_invalid"
    M_00_24 = "ternary_jamid_pattern_invalid"
    M_00_25 = "harf_maani_phonetic_form_empty"

    # ── L1 violations (M_01_xx) ──────────────────────────────────────────────
    M_01_01 = "l1_requires_l0_closure"
    M_01_02 = "definition_missing_term"
    M_01_03 = "postulate_missing_reference"
    M_01_04 = "common_notion_violation"
    M_01_05 = "bridge_license_missing"
    M_01_06 = "bridge_source_layer_invalid"
    M_01_07 = "bridge_target_layer_invalid"
    M_01_08 = "definition_not_formal"
    M_01_09 = "postulate_unprovable"
    M_01_10 = "common_notion_self_equality_violated"
    M_01_11 = "common_notion_whole_greater_part_violated"
    M_01_12 = "common_notion_substitution_violated"
    M_01_13 = "common_notion_transitivity_violated"
    M_01_14 = "l1_entity_missing_trace_ref"
    M_01_15 = "l1_entity_missing_rank"
    M_01_16 = "l1_entity_rank_promotion_forbidden"
    M_01_17 = "l1_bridge_license_ref_empty"
    M_01_18 = "l1_definition_38_terms_incomplete"
    M_01_19 = "l1_postulate_category_incomplete"
    M_01_20 = "l1_bridge_identity_not_preserved"

    # ── L2 violations (M_02_xx) ──────────────────────────────────────────────
    M_02_01 = "l2_requires_l1_closure"
    M_02_02 = "qiyas_origin_missing"
    M_02_03 = "qiyas_branch_missing"
    M_02_04 = "qiyas_cause_missing"
    M_02_05 = "qiyas_preventer_blocks"
    M_02_06 = "qiyas_condition_not_met"
    M_02_07 = "proof_postulate_not_licensed"
    M_02_08 = "proof_theorem_unprovable"
    M_02_09 = "closure_layer_not_closed"
    M_02_10 = "l2_bridge_license_missing"
    M_02_11 = "l2_entity_missing_trace_ref"
    M_02_12 = "l2_entity_rank_promotion_forbidden"
    M_02_13 = "l2_qiyas_five_components_incomplete"
    M_02_14 = "l2_proof_derives_from_unlicensed_source"
    M_02_15 = "l2_closure_verification_failed"
    M_02_16 = "l2_bridge_identity_not_preserved"
    M_02_17 = "l2_qiyas_origin_not_in_l1"
    M_02_18 = "l2_qiyas_branch_not_in_l0"
    M_02_19 = "l2_meaning_from_weight_alone_forbidden"
    M_02_20 = "l2_bridge_license_ref_empty"

    # ── L3 violations (M_03_xx) ──────────────────────────────────────────────
    M_03_01 = "l3_requires_l2_closure"
    M_03_02 = "evidence_type_invalid"
    M_03_03 = "manat_verification_failed"
    M_03_04 = "hukm_without_manat"
    M_03_05 = "tanzil_without_hukm"
    M_03_06 = "l3_bridge_license_missing"
    M_03_07 = "l3_entity_missing_trace_ref"
    M_03_08 = "l3_entity_rank_promotion_forbidden"
    M_03_09 = "hukm_candidate_in_l0_forbidden"
    M_03_10 = "tanzil_candidate_in_l0_forbidden"
    M_03_11 = "reality_claim_in_l0_forbidden"
    M_03_12 = "majaz_verdict_in_l0_forbidden"
    M_03_13 = "naql_verdict_in_l0_forbidden"
    M_03_14 = "l3_bridge_identity_not_preserved"
    M_03_15 = "l3_evidence_testimony_unverified"
    M_03_16 = "l3_evidence_observation_unverified"
    M_03_17 = "l3_evidence_tawatur_insufficient"
    M_03_18 = "l3_evidence_textual_unverified"
    M_03_19 = "l3_manat_reality_check_failed"
    M_03_20 = "l3_tanzil_without_licensed_bridge"

    # ── Waqf-Wasl boundary violations (M_WW_xx) ─────────────────────────────
    M_WW_01 = "weight_before_word_boundary"
    M_WW_02 = "word_before_syllable_license"
    M_WW_03 = "semantic_closure_without_relation"
    M_WW_04 = "harf_without_operand"
    M_WW_05 = "incomplete_verb_without_complement"
    M_WW_06 = "sub_ternary_in_derivational_weight"
    M_WW_07 = "phonetic_stop_claimed_as_meaning"
    M_WW_08 = "structural_stop_claimed_as_ifadah"

    # ── Cross-cutting violations (M_CX_xx) ──────────────────────────────────
    M_CX_01 = "identity_loss_on_transition"
    M_CX_02 = "leap_between_layers_forbidden"
    M_CX_03 = "bridge_without_license_ref"
    M_CX_04 = "transition_gate_adjacency_failed"
    M_CX_05 = "l3_construct_in_lower_layer"
    M_CX_06 = "frozen_dataclass_mutation_attempted"
    M_CX_07 = "impure_function_side_effect"
    M_CX_08 = "silent_exception_forbidden"
    M_CX_09 = "rank_ceiling_exceeded"
    M_CX_10 = "no_io_in_pure_context"
    M_CX_11 = "network_call_in_pure_context"
    M_CX_12 = "constitution_trace_ref_missing"
    M_CX_13 = "layer_index_out_of_range"
    M_CX_14 = "adapter_audit_layer_forbidden"
    M_CX_15 = "persistence_in_l0_forbidden"

    # ── Branching governance violations (M_CX_16..M_CX_20) ────────────────────
    M_CX_16 = "branch_without_roadmap_ref"
    M_CX_17 = "branch_trunk_incomplete"
    M_CX_18 = "branch_motive_missing"
    M_CX_19 = "branch_distinguishing_difference_missing"
    M_CX_20 = "branch_barrier_not_verified"
