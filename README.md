<p align="center">
  <img width=300 src="https://raw.githubusercontent.com/tjtanjin/health_ping/master/assets/health_ping.png" />
  <h1 align="center">HealthPing</h1>
</p>

<p align="center">
  <img src="https://github.com/tjtanjin/health_ping/actions/workflows/build_and_test.yml/badge.svg" />
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
**HealthPing** is a lightweight python package that allows users to easily include liveness monitoring in their applications. If you've got a python program running (such as a telegram bot) and find yourself wondering from time to time about its liveness, then this is the package for you! HealthPing abstracts away the task of sending request to monitoring endpoints, managing timezones and retries - offering all these in as short as two lines of code:
```
from health_ping import HealthPing
HealthPing(url="https://hc-ping.com/<id>", timezone="UTC+08:00", schedule="1 * * * *").start()
```
**HealthPing** essentially adopts the "deadman switch" approach, where it regularly sends a "heartbeat" to a monitoring service such as [Healthchecks.io](https://healthchecks.io/). If a "heartbeat" does not arrive within a scheduled period, the service is assumed dead and an alert (e.g. email notification) is then sent out to the service owner.

**HealthPing** is published on [**pypi**](https://pypi.org/project/health-ping/) and can be easily installed with:
```
python3 -m pip install health_ping
```
Details on the usage of the package can be found on the [**wiki page**](https://github.com/tjtanjin/health_ping/wiki).

### Features
As a lightweight utility package, HealthPing serves to carry out a single yet important purpose - notify the monitoring service that your application is still healthy and running. In order to assist you with that, HealthPing comes equipped with the following parameters for configuration:
- url
- method
- headers
- body
- timezone
- schedule
- retries
- pre_fire
- post_fire
- log_file
- debug

For most of the use cases, specifying the `url`, `timezone` and `schedule` will be enough! Details on each parameter such as their default values and usage are described in the [**wiki page**](https://github.com/tjtanjin/health_ping/wiki).

### Technologies
Technologies used by HealthPing are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Project Repository
```
https://github.com/tjtanjin/health_ping
```

### Setup
This section will walk you through setting up a development environment if you wish to make modifications or contributions to the project.
1) First, `cd` to the directory of where you wish to store the project and clone this repository. An example is provided below:
    ```
    cd /home/user/exampleuser/projects/
    git clone https://github.com/tjtanjin/health_ping.git
    ```
2) Once the project has been cloned, `cd` into it and install required dependencies with the following command:
    ```
    python3 -m pip install --no-cache-dir -r requirements.txt requirements-dev.txt
    ```
3) Following which, create (or copy) a *.env* file at the root of the project using the provided [*.env.template*](https://github.com/tjtanjin/health_ping/blob/master/.env.template). In order to run tests, you need to replace the **TEST_URL** variable within the *.env* file with any valid URL of your choice.
4) Proceed to make changes to the project (you may also wish to add test cases if necessary) and when ready, run tests with:
    ```
    python3 -m pytest ./tests/test.py
    ```
5) Should you wish to build this into a package, you may run the following commands within the project root directory:
    ```
    python3 -m build
    ```

### Team
* [Tan Jin](https://github.com/tjtanjin)

Note: Special thanks to [Avery Khoo](https://github.com/averykhoo) for bouncing ideas and sharing knowledge!

### Contributing
If you have code to contribute to the project, open a pull request and describe clearly the changes and what they are intended to do (enhancement, bug fixes etc).

Alternatively, you may contact me via [**discord**](https://discord.gg/X8VSdZvBQY) or simply raise bugs or suggestions by opening an [**issue**](https://github.com/tjtanjin/health_ping/issues).

### Others
For any questions regarding the implementation of the project, you may also reach out on [**discord**](https://discord.gg/X8VSdZvBQY) or drop an email to: cjtanjin@gmail.com.

