# Reachy Mini + AI: LLM, VLM, VLA

Three short Python demos that connect AI models to the Reachy Mini robot.

| Demo | Model type | Input → Output | What the robot does |
|---|---|---|---|
| `demo1_llm.py` | LLM | text → text | Chats with you. Tilts its head while thinking, nods when it answers. |
| `demo2_vlm.py` | VLM | camera image + question → text | Describes what its camera sees, then wiggles its antennas. |
| `demo3_vla.py` | VLA | camera image + instruction → action | Turns its head step by step until the task is done. |

## How demo 3 works

The robot runs a loop: **look → choose an action → move → look again**. At each step a vision-language model sees the camera image and the instruction (e.g. "look at the cup"), and picks one action from a short list: `look_left`, `look_right`, `look_up`, `look_down`, `done`.

## Models

By default, the demos use free open-source models that run on your laptop with Ollama: Meta's Llama for demo 1 and Google's Gemma for demos 2 and 3. Add `--api` to a command to use OpenAI models instead (needs an API key); the robot then also says its answers out loud. The free models have no voice.

Models can make mistakes, especially small ones. Try different model sizes, other model families, or an API model to find what fits your computer and budget.

## Files

- `demo1_llm.py`, `demo2_vlm.py`, `demo3_vla.py`: the three demos
- `common.py`: shared code for calling the model, moving the robot and reading the camera
- `SETUP.md`: step-by-step guide to run everything
