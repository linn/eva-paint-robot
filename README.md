# Paint Plant Robot System

A pair of Eva Robots https://automata.tech/about-eva/

IP and API key defined in /etc/environment on the host controller machine

## Installation
Install the requisite python modules with:

```python3 -m pip install -r requirements.txt```

Copy eva-paint-plant.service to /etc/systemd/system/

Execute sudo systemctl daemon-reload ; sudo systemctl enable eva-paint-plant.service --now