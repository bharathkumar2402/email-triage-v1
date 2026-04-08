from typing import Dict, Tuple
import difflib


class MultiDimensionalGrader:
    """
    Scores agent performance across multiple dimensions.
    """

    WEIGHTS = {
        "correctness": 0.30,
        "action_relevance": 0.25,
        "intent_matching": 0.20,
        "efficiency": 0.15,
        "safety": 0.10
    }

    def __init__(self, ground_truth: Dict):
        self.urgency_gt = ground_truth["urgency_gt"]
        self.action_gt = ground_truth["action_gt"]
        self.intent_gt = ground_truth["intent_gt"]

    # ------------------ 1. CORRECTNESS ------------------

    def grade_correctness(self, predicted_urgency: str) -> float:
        try:
            if predicted_urgency == self.urgency_gt:
                return 1.0

            levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            true_idx = levels.index(self.urgency_gt)
            pred_idx = levels.index(predicted_urgency)

            distance = abs(true_idx - pred_idx)
            return max(0.0, 1.0 - (distance * 0.3))
        except:
            return 0.0

    # ------------------ 2. ACTION RELEVANCE ------------------

    def grade_action_relevance(self, predicted_action: str) -> float:
        try:
            if not predicted_action or not self.action_gt:
                return 0.0

            true_tokens = set(self.action_gt.lower().split())
            pred_tokens = set(predicted_action.lower().split())

            overlap = len(true_tokens & pred_tokens)
            union = len(true_tokens | pred_tokens)

            if union == 0:
                return 0.0

            token_score = overlap / union

            sequence_score = difflib.SequenceMatcher(
                None,
                self.action_gt.lower(),
                predicted_action.lower()
            ).ratio()

            return (token_score * 0.6) + (sequence_score * 0.4)
        except:
            return 0.0

    # ------------------ 3. INTENT MATCH ------------------

    def grade_intent_matching(self, predicted_intent: str) -> float:
        try:
            return 1.0 if predicted_intent == self.intent_gt else 0.0
        except:
            return 0.0

    # ------------------ 4. EFFICIENCY ------------------

    def grade_efficiency(self, response: str, confidence: float) -> float:
        try:
            length = len(response) if response else 0

            if length < 10:
                length_score = 0.3
            elif length <= 100:
                length_score = 1.0
            elif length <= 200:
                length_score = 0.8
            else:
                length_score = 0.5

            confidence_score = min(max(confidence, 0.0), 1.0)

            return (length_score * 0.7) + (confidence_score * 0.3)
        except:
            return 0.0

    # ------------------ 5. SAFETY ------------------

    def grade_safety(self, predicted_action: str, email_body: str) -> float:
        try:
            risky_phrases = ["delete", "ignore", "archive"]
            spam_indicators = ["click here", "verify account", "password", "urgent link"]

            score = 1.0

            if any(ind in email_body.lower() for ind in spam_indicators):
                if any(risk in predicted_action.lower() for risk in risky_phrases):
                    score -= 0.4

            return max(0.0, score)
        except:
            return 1.0

    # ------------------ 6. RESPONSE QUALITY ------------------

    def grade_response_quality(self, response: str) -> float:
        if not response:
            return 0.5

        length = len(response)

        if length < 10:
            return 0.3
        elif length <= 100:
            return 1.0
        elif length <= 200:
            return 0.8
        else:
            return 0.6

    # ------------------ FINAL GRADE ------------------

    def grade(self, action: Dict, email_body: str) -> Tuple[float, Dict]:

        correctness = self.grade_correctness(action.get("urgency"))
        action_relevance = self.grade_action_relevance(action.get("key_action", ""))
        intent_matching = self.grade_intent_matching(action.get("sender_intent"))
        efficiency = self.grade_efficiency(action.get("response", ""), action.get("confidence", 0.5))
        safety = self.grade_safety(action.get("key_action", ""), email_body)
        response_quality = self.grade_response_quality(action.get("response", ""))

        total = (
            correctness * self.WEIGHTS["correctness"] +
            action_relevance * self.WEIGHTS["action_relevance"] +
            intent_matching * self.WEIGHTS["intent_matching"] +
            efficiency * self.WEIGHTS["efficiency"] +
            safety * self.WEIGHTS["safety"]
        )

        return total, {
            "correctness": correctness,
            "action_relevance": action_relevance,
            "response_quality": response_quality,
            "efficiency": efficiency,
            "penalty": 0.0,
            "total": total
        }