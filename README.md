# Paint Plant Robot System

A pair of Eva Robots https://automata.tech/about-eva/

IP, API key, and Barcode Reader path are defined in .env on the host controller machine, in the directory
```
/home/pi/eva-paint-robot/
```
## Installation
Install the requisite python modules with:

```
sudo pipenv install
```

Install the systemctl startup/shutdown script with:

```
sudo cp eva-paint-robot.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable eva-paint-robot.service --now
```