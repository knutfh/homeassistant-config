import appdaemon.plugins.hass.hassapi as hass

class Hass(hass.Hass):
  def initialize(self):
    self.log("Hass initialized")
    self.set_namespace('hass')
    
    self.handle = self.listen_event(self.test, "MQTT_MESSAGE")
    
  def test(self, event_name, data, kwargs):
    self.log("Message received")
    
