# Home Assistant configuration

This is my [Home Assistant](https://www.home-assistant.io) configuration.

I'm running Ubuntu 16.04.4 (Xenial) on an old laptop, and have installed [Hass.io](https://www.home-assistant.io/hassio/). 
I'm running a slew of different services in the same Docker environment, and use [Portainer](https://portainer.io) to manage it all.

- [Caddy](https://caddyserver.com) as a reverse proxy.
- [BlueIris](https://blueirissoftware.com) for surveillance.
- [InfluxDB](https://www.influxdata.com) to store sensor data from Home Assistant.
- [Grafana](https://grafana.com) to visualise all of that data.
- [Portainer](https://www.portainer.io) to manage my Docker environment.

## Devices and services I use with Home Assistant
- [Aeotec Z-Stick Gen5](https://aeotec.com/z-wave-usb-stick)
- [Aeotec Multisensor 6](https://aeotec.com/z-wave-sensor)
- [RFXtrx433E USB HA controller](http://www.rfxcom.com/RFXtrx433E-USB-43392MHz-Transceiver/en)
- [Fibaro Dimmer 2](https://www.fibaro.com/us/products/dimmer-2/)
- [Fibaro Double Switch](https://www.fibaro.com/us/products/switches/)
- [IKEA Trådfri](https://www.ikea.com/no/no/catalog/categories/departments/lighting/36812/)
    - We currently have 31 different bulbs in use, with everything working great.
- [Viking Remote Thermo Sensor](https://www.lohelectronics.se/hemautomation/433mhz/sensorer-1110/tradlos-termometer-for-inne-utomhusbruk)
