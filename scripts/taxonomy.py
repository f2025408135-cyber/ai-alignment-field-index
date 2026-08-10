#!/usr/bin/env python3
"""Single source of truth for the index taxonomy (brief Section 3).

Both the merge validator and the audit derive the allowed subtopic tags from
this module, so a fragment using an unexpected tag fails at merge time instead
of silently failing the final coverage audit.
"""

EXPECTED_SUBTOPICS = {
    "entry-tier": ["thought-experiments", "fermi-paradox", "sci-fi", "introductions"],
    "macrostrategy": ["xrisk-theory", "great-filter", "forecasting", "differential-development", "longtermism"],
    "agent-foundations": ["embedded-agency", "decision-theory", "corrigibility", "infra-bayesianism", "cartesian-frames", "logical-induction"],
    "interpretability": ["circuits", "superposition-saes", "tracing", "probing", "causal-abstraction", "slt", "rep-engineering", "tooling"],
    "oversight-rlhf": ["rlhf", "constitutional-ai", "debate", "amplification", "weak-to-strong", "process-outcome", "reward-hacking"],
    "evals-benchmarks": ["dangerous-capabilities", "deception", "autonomy", "red-teaming", "eval-critiques"],
    "governance-policy": ["compute-governance", "international", "lab-governance", "regulation", "analogies"],
    "security-redteam": ["adversarial-robustness", "jailbreaks", "weights", "supply-chain", "prompt-injection"],
    "philosophy-values": ["value-specification", "moral-uncertainty", "cev", "pluralism", "population-ethics"],
    "field-infrastructure": ["training", "funders", "orgs", "communities", "careers"],
}

DOMAIN_TITLES = {
    "entry-tier": "Entry Tier",
    "macrostrategy": "Macrostrategy & X-Risk",
    "agent-foundations": "Agent Foundations & Decision Theory",
    "interpretability": "Interpretability",
    "oversight-rlhf": "Scalable Oversight & RLHF",
    "evals-benchmarks": "Evals & Benchmarks",
    "governance-policy": "Governance & Policy",
    "security-redteam": "Security & Red-teaming",
    "philosophy-values": "Philosophy & Value Alignment",
    "field-infrastructure": "Field Infrastructure",
}
