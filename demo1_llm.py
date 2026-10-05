"""Demo 1 - LLM: chat with Reachy Mini.

You type a message, a language model answers, and the robot reacts
(tilts its head while "thinking", nods when it answers).

    python demo1_llm.py         # free open-source model
    python demo1_llm.py --api   # OpenAI model, and the robot says the answer out loud
"""

from common import LLM_MODEL, SPEAK, ask, connect_robot, move_head, nod, speak

SYSTEM_PROMPT = "You are Reachy Mini, a small friendly desktop robot. Answer in 1-2 short sentences."

with connect_robot(media=SPEAK) as mini:  # speaker only needed to speak
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Chat with Reachy Mini (q to quit).")
    while True:
        text = input("\nyou> ").strip()
        if text == "q":
            break
        if not text:
            continue

        messages.append({"role": "user", "content": text})
        move_head(mini, roll=15)  # tilt head: "thinking..."
        reply = ask(LLM_MODEL, messages)
        messages.append({"role": "assistant", "content": reply})

        print("reachy>", reply)
        speak(mini, reply)
        nod(mini)
