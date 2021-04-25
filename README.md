# Modern Forms smart fan interface
[Modern Forms](http://moderforms.com/fan/) has a collection of cloud connected Wi-Fi smart fans.  They can be controlled via their app, but they also support local control.  This project is an interface to control their fans locally via the REST API on the fan.

All aspects of the fan and option light kit can be controlled.

The REST API of the fan is unpublished.  It was mapped out using a packet capture and interactions with their app.  Since the manufacturer was unwilling to publish the API it is subject to change and break at any time.

## Invocation
Import into your code and create a `ModernFormsFan` object

```python
import modernforms
fan = moderforms.ModernFormsFan('192.168.1.10', 5)
```
Constructor takes 2 arguments.  The IP or hostname (if you DNS registered your fan) and the timeout for communicating with the fan.

The timeout is optional and has a default value of 5.

### Fan Control
The fan has 3 attributes to control:
* fan_on
* fan_speed
* fan_direction
```python
>>> fan.fan_on
False
>>> fan.fan_on = True
>>> fan.fan_on
True
```

### Light Control
The light kit has two attributes to control:
* light_on
* light_brightness
```python
>>> fan.light_on
False
>>> fan.light_on = True
>>> fan.light_on
True
```
