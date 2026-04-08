import random
from datetime import datetime, timedelta
from typing import List, Dict


class EmailGenerator:
    """Generates diverse emails with ground truth labels"""

    def __init__(self):
        self.random = random.Random()

    def generate_email(self, difficulty: str = "medium") -> Dict:
        """
        Generate an email with ground truth labels
        difficulty: easy, medium, hard
        """

        if difficulty == "easy":
            templates = self._get_critical_high_templates()
        elif difficulty == "medium":
            templates = self._get_high_medium_templates()
        else:
            templates = self._get_medium_low_templates()

        template = self.random.choice(templates)

        email = {
            "email_id": f"email_{self.random.randint(1,100000)}",
            "subject": template["subject"],
            "body": template["body"],
            "sender": f"user{self.random.randint(1,5000)}@company.com",
            "timestamp": (datetime.now() - timedelta(hours=self.random.randint(0, 48))).isoformat(),

            # ✅ Ground truth (VERY IMPORTANT)
            "urgency_gt": template["urgency"],
            "action_gt": template["action"],
            "intent_gt": template["intent"],
        }

        return email

    def generate_batch(self, n: int, difficulty: str) -> List[Dict]:
        return [self.generate_email(difficulty) for _ in range(n)]

    # -------------------- TEMPLATE GROUPS --------------------

    def _get_critical_high_templates(self) -> List[Dict]:
        return [
            {
                "subject": "🚨 URGENT: Production database is DOWN",
                "body": "All services offline. 5000+ customers affected. Need immediate fix.",
                "urgency": "CRITICAL",
                "action": "Declare incident and page engineers",
                "intent": "ALERT"
            },
            {
                "subject": "[SECURITY] Possible breach detected",
                "body": "Suspicious login attempts detected. Possible attack ongoing.",
                "urgency": "CRITICAL",
                "action": "Initiate security response and notify team",
                "intent": "ALERT"
            },
            {
                "subject": "Budget approval needed ASAP",
                "body": "Requesting $200k for marketing. Deadline tomorrow.",
                "urgency": "HIGH",
                "action": "Review and approve budget",
                "intent": "REQUEST"
            },
            {
                "subject": "Client escalation - urgent issue",
                "body": "Client unhappy with service. Needs immediate callback.",
                "urgency": "HIGH",
                "action": "Call client and resolve issue",
                "intent": "ESCALATION"
            },
        ]

    def _get_high_medium_templates(self) -> List[Dict]:
        return [
            {
                "subject": "Feature update released",
                "body": "New dashboard available for testing. Feedback needed.",
                "urgency": "MEDIUM",
                "action": "Test feature and give feedback",
                "intent": "FYI"
            },
            {
                "subject": "Team training pending",
                "body": "Some members haven’t completed training. Please follow up.",
                "urgency": "MEDIUM",
                "action": "Send reminders to team",
                "intent": "REQUEST"
            },
        ]

    def _get_medium_low_templates(self) -> List[Dict]:
        return [
            {
                "subject": "Team lunch?",
                "body": "Planning lunch this Friday. Suggestions?",
                "urgency": "LOW",
                "action": "Reply with preference",
                "intent": "FYI"
            },
            {
                "subject": "Office survey",
                "body": "Please fill office improvement survey.",
                "urgency": "LOW",
                "action": "Fill survey",
                "intent": "FYI"
            },
        ]