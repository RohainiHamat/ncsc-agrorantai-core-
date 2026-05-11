"""
NCSC AgroRantai - RIF Engine v0.1
Residue Intelligence Firewall prototype with Moral Boundary Ruleset
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Tuple
from enum import Enum

# =============== 1. CLASSIFICATION OUTPUT ===============
class DecisionClass(Enum):
    SAFE = "A"       # Lulus, terus laksana
    BOUNDARY = "B"   # Persempadanan, perlu semakan manusia
    VIOLATION = "C"  # Langgar batas moral, sekat serta-merta

# =============== 2. FEATURE EXTRACTION ===============
def extract_features(decision_input: Dict) -> Dict:
    features = {
        "temp_deviation": abs(decision_input.get("temperature", 0) - 4.0),
        "residue_level": decision_input.get("residue_ppm", 0),
        "economic_risk": decision_input.get("economic_impact", 0) < -1000,
        "is_night_release": datetime.now().hour < 6,
        "actor_type": decision_input.get("actor", "unknown")
    }
    return features

# =============== 3. MORAL BOUNDARY RULESET (MBR) ===============
class MoralBoundaryRuleset:
    RULES = [
        {
            "name": "residue_limit",
            "condition": lambda f: f["residue_level"] > 0.5,
            "class": DecisionClass.VIOLATION,
            "reason": "Residu racun melebihi 0.5 ppm"
        },
        {
            "name": "temperature_safety",
            "condition": lambda f: f["temp_deviation"] > 2.0,
            "class": DecisionClass.BOUNDARY,
            "reason": "Suhu luar julat selamat >2°C"
        },
        {
            "name": "economic_sabotage",
            "condition": lambda f: f["economic_risk"] and f["is_night_release"],
            "class": DecisionClass.VIOLATION,
            "reason": "Risiko ekonomi tinggi + waktu malam (potensi sabotaj)"
        },
        {
            "name": "untrusted_actor",
            "condition": lambda f: f["actor_type"] == "untrusted",
            "class": DecisionClass.BOUNDARY,
            "reason": "Pelaku tidak diperakui, perlukan veto"
        }
    ]
    
    @classmethod
    def classify(cls, features: Dict) -> Tuple[DecisionClass, List[str]]:
        reasons = []
        final_class = DecisionClass.SAFE
        for rule in cls.RULES:
            if rule["condition"](features):
                reasons.append(rule["reason"])
                rule_class = rule["class"]
                if rule_class == DecisionClass.VIOLATION:
                    final_class = DecisionClass.VIOLATION
                elif rule_class == DecisionClass.BOUNDARY and final_class != DecisionClass.VIOLATION:
                    final_class = DecisionClass.BOUNDARY
        return final_class, reasons

# =============== 4. AUDIT LOGGER (System Diary) ===============
class SystemDiary:
    def __init__(self, log_path="audit_log.jsonl"):
        self.log_path = log_path
    
    def log(self, entry: Dict):
        entry["timestamp"] = datetime.utcnow().isoformat()
        entry["hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[AUDIT] {entry['decision_class']} | {entry['reason_summary']}")

# =============== 5. RIF ENGINE UTAMA ===============
class RIFEngine:
    def __init__(self):
        self.diary = SystemDiary()
    
    def evaluate(self, decision_input: Dict) -> Dict:
        features = extract_features(decision_input)
        decision_class, reasons = MoralBoundaryRuleset.classify(features)
        
        if decision_class == DecisionClass.SAFE:
            action_taken = "execute"
        elif decision_class == DecisionClass.BOUNDARY:
            action_taken = "require_review"
        else:
            action_taken = "block_and_alert"
        
        audit_entry = {
            "decision_input": decision_input,
            "features": features,
            "decision_class": decision_class.value,
            "reasons": reasons,
            "action_taken": action_taken,
            "reason_summary": reasons[0] if reasons else "none"
        }
        self.diary.log(audit_entry)
        
        return {
            "allowed": action_taken != "block_and_alert",
            "requires_review": (action_taken == "require_review"),
            "decision_class": decision_class.value,
            "reasons": reasons,
            "action": action_taken
        }

# =============== 6. SIMULASI ===============
if __name__ == "__main__":
    engine = RIFEngine()
    
    test_cases = [
        {"action": "release", "temperature": 4.1, "residue_ppm": 0.2, "economic_impact": 0, "actor": "certified_farmer"},
        {"action": "release", "temperature": 1.5, "residue_ppm": 0.1, "economic_impact": 0, "actor": "certified_farmer"},
        {"action": "release", "temperature": 4.0, "residue_ppm": 0.8, "economic_impact": 0, "actor": "certified_farmer"},
        {"action": "release", "temperature": 4.0, "residue_ppm": 0.1, "economic_impact": -5000, "actor": "untrusted"},
    ]
    
    for i, case in enumerate(test_cases):
        print(f"\n--- Ujian {i+1} ---")
        result = engine.evaluate(case)
        print(f"Keputusan: {result}")
