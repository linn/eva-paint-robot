# Paint Plant Robot System

A pair of Eva Robots https://automata.tech/about-eva/

IP and API key defined in /etc/environment on the host controller machine

## Installation
Install the requisite python modules with:

```
python3 -m pip install -r requirements.txt
```

Install the systemctl startup/shutdown script with:

```
sudo cp eva-paint-robot.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable eva-paint-robot.service --now
```