"""Demo 2 - VLM: Reachy Mini answers questions about what its camera sees.

Each question takes a fresh camera frame and sends image + question
to a vision-language model.

    python demo2_vlm.py         # free open-source model
    python demo2_vlm.py --api   # OpenAI model, and the robot says the answer out loud
"""

import cv2

from common import VLM_MODEL, ask, connect_robot, get_frame, image_content, speak, wiggle_antennas

DEFAULT_QUESTION = "What do you see? Answer in 1-2 sentences."

with connect_robot() as mini:
    print("Ask about what the robot sees (Enter = 'What do you see?', q to quit).")
    while True:
        question = input("\nyou> ").strip() or DEFAULT_QUESTION
        if question == "q":
            break

        frame = get_frame(mini)
        cv2.imwrite("last_frame.jpg", frame)  # check what the model actually saw
        messages = [{"role": "user", "content": image_content(frame, question)}]
        reply = ask(VLM_MODEL, messages)

        print("reachy>", reply)
        speak(mini, reply)
        wiggle_antennas(mini)
