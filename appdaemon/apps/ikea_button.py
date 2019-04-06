import appdaemon.plugins.hass.hassapi as hass

import json
from datetime import datetime, timedelta


class IKEAButton(hass.Hass):


  def initialize(self):
    
    self.set_namespace('hass')
    self.button_topic = self.args.get('button_topic', 'zigbee2mqtt/IKEA-button-1')
    self.light = self.args.get('light')
    
    self.listen_event_handle_list = []
    self.timer_handle_list = []
    
    self.dimmer_timer_handle = None
    
    self.listen_event_handle_list.append(self.listen_event(self.mqtt_callback_cb, "MQTT_MESSAGE", namespace = 'mqtt'))


  def mqtt_callback_cb(self, event_name, data, kwargs):
    topic = data['topic']
    payload = data['payload']

    if topic != self.button_topic  or payload == "":
      return

    payload = json.loads(payload)
    action = payload.get('action')

    self.log(action)

    if action == 'toggle':
      self.light_toggle()
      
    if action == 'brightness_up_click':
      self.light_dim(+0.25)
      
    if action == 'brightness_down_click':
      self.light_dim(-0.25)
      
    if action == 'arrow_right_click':
      self.light_color_change(+70)
      
    if action == 'arrow_left_click':
      self.light_color_change(-70)
      
    # if action == 'brightness_up_hold':
    #   self.log("Dimming {} up".format(self.light))
      
    #   trigger_time = datetime.now() + timedelta(seconds=2)
    #   self.log(trigger_time)
      
    #   self.dimmer_timer_handle = self.run_every(self.dimmer_callback(direction='up'), trigger_time, 0.5)
    #   self.timer_handle_list.append(self.dimmer_timer_handle)
      
    #   self.log("Setting timer handle {}".format(self.dimmer_timer_handle))
      
    # if action == 'brightness_down_hold':
    #   self.log("Dimming {} down".format(self.light))
      
    #   trigger_time = datetime.now() + timedelta(seconds=1)
    #   self.log(trigger_time)
      
    #   self.dimmer_timer_handle = self.run_every(self.dimmer_callback(direction='down'), trigger_time, 0.5)
    #   self.timer_handle_list.append(self.dimmer_timer_handle)
      
    #   self.log("Setting timer handle {}".format(self.dimmer_timer_handle))
      
    # if action == 'brightness_up_release':
    #   if self.dimmer_timer_handle != None:
    #     self.log("Release timer {}".format(self.dimmer_timer_handle))
    #     self.cancel_timer(self.dimmer_timer_handle)
        
    # if action == 'brightness_down_release':
    #   if self.dimmer_timer_handle != None:
    #     self.log("Release timer {}".format(self.dimmer_timer_handle))
    #     self.cancel_timer(self.dimmer_timer_handle)  
      
        
  def light_toggle(self):
      self.log("Toggle light {}".format(self.light))
      self.toggle(self.light)
      
  def light_dim(self, *args):
    attributes = self.get_state(self.light, attribute="all")['attributes']
    
    if 'brightness' in attributes:
      brightness_pct_old = attributes['brightness']/255
    else:
      brightness_pct_old = 0
      
    brightness_pct_new = brightness_pct_old + args[0]
    
    if brightness_pct_new > 1:
      brightness_pct_new = 1
    elif brightness_pct_new < 0:
      brightness_pct_new = 0
     
    self.log("Settings {} brightness to {}".format(self.light, brightness_pct_new))
    self.call_service("light/turn_on", entity_id=self.light, brightness_pct=brightness_pct_new*100, transition=1)
      
  
  def light_color_change(self, *args):
    
    attributes = self.get_state(self.light, attribute="all")["attributes"]
    min_mireds = attributes['min_mireds']
    max_mireds = attributes['max_mireds']
    current_mireds = attributes['color_temp']
    
    self.log("{} current temp: {}, {}/{}".format(self.light, current_mireds, min_mireds, max_mireds))
    
    self.call_service("light/turn_on", 
                      entity_id=self.light, 
                      color_temp=current_mireds + args[0], 
                      transition=1)
      
  def dimmer_callback(self, **kwargs):
    """Dim the light by 10%. If it would dim above 100%, start again at 10%"""
    self.log("Fire dimmer")
    
    direction = kwargs['direction']

    brightness_pct_old = int(self.get_state(self.light, attribute="all")["attributes"]["brightness"]) / 255
    
    if direction == 'up':
      brightness_pct_new = brightness_pct_old + 0.25
      
      if brightness_pct_new > 1:
        brightness_pct_new = 0.1
      
    if direction == 'down':
      brightness_pct_new = brightness_pct_old - 0.1
      
      if brightness_pct_new < 0:
        brightness_pct_new = 1
      
    self.call_service("light/turn_on", entity_id=self.light, brightness_pct=brightness_pct_new*100)
      
      
  def terminate(self):
    for listen_event_handle in self.listen_event_handle_list:
      self.cancel_listen_event(listen_event_handle)
    
    for timer_handle in self.timer_handle_list:
      self.cancel_timer(timer_handle)