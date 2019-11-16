# Hella_Turbo_Controller
Programming the [Hella Universal turbo actuator I](https://www.hella.com/microsite-electronics/en/Universal-turbo-actuator-I-133.html). 

This turbo actuator is used on many verhicles, especially to control VTG turbo's. Two main interfaces to the ECU are used, the CAN bus or the PWM interface. The actuators are actually all the same and can be configured to work in either mode. Also especially in PWM mode, the range and sensitivity can be configured.

In the wiki, some more information can be found on how this works and what can be configured. This is still WIP!

Also this repository will host a python application to program the actuator using a standard SLCAN interface or any SOCKETCAN compatible interface if you're on Linux. 

Applying this information and/or software may break your actuator, computer, turbo, engine or car. If you do not know what you are doing, do not use this. Use this information and software at your own risk, I will not take any responsibility.

This repository and/or the information relayed here is in no way provided or affiliated to Hella company and is the result of private reverse engineering work.
