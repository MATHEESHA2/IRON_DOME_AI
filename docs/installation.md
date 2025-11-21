
# Installation Guide (quick)

1. Create Python venv and install packages:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Ensure torch is installed for your GPU (see pytorch.org).

3. Test pipeline simulator:
   python integration/pipeline_simulator.py
