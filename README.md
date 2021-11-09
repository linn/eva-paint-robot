# Paint Plant Robot System

A pair of Eva Robots https://automata.tech/about-eva/

IP, API key, and Barcode Reader path are defined in .env on the host controller machine, in the directory
```
/home/pi/eva-paint-robot/
```
## Assigning barcodes

Log in to the host controller machine and run the following command:
```
sudo systemctl stop eva-paint-robot
```

This releases the exclusive lock on the barcode reader.

Within the eva-paint-robot directory, run the command
```./main.py``` to start the barcode assigning process.

When complete, press ctrl-c to exit the program.

To start the system again, run the following command
```
sudo systemctl start eva-paint-robot
```

## Installation

Clone this repository to your local machine, within the directory ```/home/pi/eva-paint-robot/```

```cd /home/pi/eva-paint-robot/``` and install the requisite python modules with:

```
sudo pipenv install
```

Install the systemctl startup/shutdown script with:

```
sudo cp eva-paint-robot.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable eva-paint-robot.service --now
```