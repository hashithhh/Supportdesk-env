from __future__ import annotations

from supportdesk_openenv.env import SupportDeskEnvManager, baseline_actions
from supportdesk_openenv.tasks import TASKS


def main() -> None:
    manager = SupportDeskEnvManager()
    scores: list[tuple[str, float]] = []
    for task_id in TASKS:
        reset_response = manager.reset(task_id)
        for action in baseline_actions(task_id):
            manager.step(reset_response.episode_id, action)
        grade = manager.grade(reset_response.episode_id)
        scores.append((task_id, grade.score))

    average = sum(score for _, score in scores) / len(scores)
    print("Baseline scores")
    for task_id, score in scores:
        print(f"- {task_id}: {score:.4f}")
    print(f"Average: {average:.4f}")


if __name__ == "__main__":
    main()
