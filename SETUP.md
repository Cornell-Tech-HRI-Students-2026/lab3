# Setup: run the demos step by step

## Step 1: Install (once)

Use Python 3.12.

```bash
cd reachy-mini
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

In every new terminal, go to the `reachy-mini` folder and run `source .venv/bin/activate` first.

## Step 2: Robot and models

Open `common.py` and set `ROBOT_IP` to your robot's IP address.

Install [Ollama](https://ollama.com), then download the two free models:

```bash
ollama pull llama3.2     # Meta Llama, text only: demo 1
ollama pull gemma3:4b    # Google Gemma, text + images: demos 2 and 3
```

Models can make mistakes, especially small ones. Try different model sizes, other model families, or an API model to find what fits your computer and budget.

## Step 3: Run

Connect your laptop to the same network as the robot, and check that it is reachable:

```bash
curl http://<ROBOT_IP>:8000/api/daemon/status   # prints JSON = robot is reachable
```

Then run the demos:

```bash
python demo1_llm.py
python demo2_vlm.py
python demo3_vla.py
```

Type `q` to quit.

## Using an OpenAI API key (optional)

Put a file named `.env` in the `reachy-mini` folder (skip this if it is already there), containing:

```
OPENAI_API_KEY=sk-...
```

Then add `--api` to the commands, e.g. `python demo1_llm.py --api`. With `--api`, the robot also says its answers out loud (the free models have no voice), and you don't need Ollama.
