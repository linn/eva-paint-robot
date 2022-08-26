# Paint Plant Robot System

A pair of Eva Robots https://automata.tech/about-eva/

IP, API key, and Barcode Reader path are defined in .env on the host controller machine, in the directory
```
/home/pi/eva-paint-robot/
```

## Logging in to the host controller

The system is operated by an industrial Raspberry Pi. SSH is available, and can be used from the production network.

On a Mac or Linux machine, use the terminal and ```ssh``` to the device IP address.

On Windows, use Putty from https://www.chiark.greenend.org.uk/~sgtatham/putty/ - this has already been installed on the Metalwork workstations.

Web interfaces to the robot arms and Raspberry Pi controller are also available.

## Assigning barcodes

Log in to the host controller machine and run the following command:
```
sudo systemctl stop eva-paint-robot
```

This releases the exclusive lock on the barcode reader.

Within the eva-paint-robot directory, run following command
to start the barcode assigning process.

```/usr/bin/python3 /home/pi/eva-paint-robot/main.py```

It will take a moment to load, and then it will walk you through the process.

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

## Observing logs

The paint robot service operates in headless mode when running in day to day operations.
This allows it to recieve barcode events and act upon them without any other interaction required.
To check the behaviour of the system whilst it is running, logs are output to the following location.

```/home/pi/eva-paint-robot/eva.log```

It is possible to 'tail' the logs with a command such as this:

```tail -n 50 -f /home/pi/eva-paint-robot/eva.log```

This will show the last 50 lines of the log file, including anything new that is generated. Stop the command with ctrl+c

## Updating the Pi robot code

If this source code has been modified and commit to Git externally, such as via a workstation or laptop, it must also be synchronised down to the Pi.

SSH to the Raspberry Pi, and cd to the ```/home/pi/eva-paint-robot``` directory

Stop the robot system with ```sudo systemctl stop eva-paint-robot.service```

Execute ```git pull```, and the source code will be updated from the copy in Github.

Use ```git status``` to view the status of the filesystem compared to what source control expects. There should be no major differences.

Start the robot system with ```sudo systemctl start eva-paint-robot.service```