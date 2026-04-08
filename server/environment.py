from typing import Dict
from models import EmailObservation, EmailReward, StepResult
from server.email_generator import EmailGenerator
from server.grader import MultiDimensionalGrader


class EmailTriageEnvironment:
    def __init__(self):
        self.generator = EmailGenerator()
        self.current_email = None
        self.step_count = 0
        self.max_steps = 5

    # ---------------- RESET ----------------

    def reset(self) -> EmailObservation:
        self.step_count = 0

        self.current_email = self.generator.generate_email()

        return EmailObservation(
            email_id=self.current_email["email_id"],
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender=self.current_email["sender"],
            timestamp=self.current_email["timestamp"],
            email_chain_length=0,
            previous_messages=[],
            context_available=True
        )

    # ---------------- STEP ----------------

    def step(self, action: Dict) -> StepResult:
        self.step_count += 1

        grader = MultiDimensionalGrader(self.current_email)

        score, breakdown = grader.grade(action, self.current_email["body"])

        reward = EmailReward(
            correctness=breakdown["correctness"],
            action_relevance=breakdown["action_relevance"],
            response_quality=breakdown["response_quality"],
            efficiency=breakdown["efficiency"],
            penalty=breakdown["penalty"],
            total=breakdown["total"]
        )

        done = self.step_count >= self.max_steps

        # Generate next observation
        self.current_email = self.generator.generate_email()

        observation = EmailObservation(
            email_id=self.current_email["email_id"],
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender=self.current_email["sender"],
            timestamp=self.current_email["timestamp"],
            email_chain_length=0,
            previous_messages=[],
            context_available=True
        )

        return StepResult(
            observation=observation,
            reward=reward,
            done=done,
            info={"step": self.step_count}
        )

    # ---------------- STATE ----------------

    def state(self) -> Dict:
        return {
            "step_count": self.step_count,
            "current_email": self.current_email
        }