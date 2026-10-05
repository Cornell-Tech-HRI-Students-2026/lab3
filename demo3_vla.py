"""Demo 3 - VLA (vision-language-action): image + instruction -> robot action, in a loop.

Real VLA models (SmolVLA, OpenVLA, pi0) output motor commands directly, but they are
trained on robot arms - there is no pretrained VLA for Reachy Mini. So here a VLM acts
as the policy: at each step it sees the camera image and picks ONE action from a small
fixed list (like RT-2's "actions as text tokens"). The robot moves, takes a new picture,
and the loop repeats until the model says "done".

    python demo3_vla.py         # free open-source model
    python demo3_vla.py --api   # OpenAI model, and the robot says "I found you!"
"""

from common import (VLM_MODEL, YAW_LIMIT, TILT_LIMIT, ask, clamp, connect_robot, get_frame,
                    image_content, move_head, speak, wiggle_antennas)

STEP = 15  # degrees per action
MAX_STEPS = 8

# action -> change in (yaw, pitch), degrees
ACTIONS = {
    "look_left": (+STEP, 0),
    "look_right": (-STEP, 0),
    "look_up": (0, -STEP),
    "look_down": (0, +STEP),
    "done": (0, 0),
}

PROMPT = """You control a robot head with a camera. The image is what the camera sees right now.
Task: {task}
Actions taken so far: {history}

Pick the next action:
- look_left / look_right: the target is in the left / right part of the image
- look_up / look_down: the target is in the top / bottom part of the image
- done: the target is near the center of the image
If the target is not in the image, turn left or right to search for it.
Reply with exactly one of: {actions}"""


def parse_action(reply):
    """Find the first known action name in the model's reply."""
    for name in ACTIONS:
        if name in reply.lower():
            return name
    return None


task = input("Instruction (Enter = 'Look at the person'): ").strip() or "Look at the person."

with connect_robot() as mini:
    yaw, pitch, history = 0, 0, []
    move_head(mini)  # start centered

    for step in range(1, MAX_STEPS + 1):
        frame = get_frame(mini)
        prompt = PROMPT.format(task=task, history=", ".join(history) or "none", actions=", ".join(ACTIONS))
        reply = ask(VLM_MODEL, [{"role": "user", "content": image_content(frame, prompt)}])
        action = parse_action(reply)
        print(f"step {step}: model said {reply.strip()!r} -> {action}")

        if action is None:
            print("Could not understand the reply, stopping.")
            break
        if action == "done":
            speak(mini, "I found you!" if "person" in task.lower() else "I found it!")
            wiggle_antennas(mini)
            print("Task done!")
            break

        d_yaw, d_pitch = ACTIONS[action]
        yaw, pitch = clamp(yaw + d_yaw, YAW_LIMIT), clamp(pitch + d_pitch, TILT_LIMIT)
        move_head(mini, yaw=yaw, pitch=pitch)
        history.append(action)
    else:
        print(f"Stopped after {MAX_STEPS} steps.")
