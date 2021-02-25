import paho.mqtt.client as mqtt
import logging

from threading import Timer

import pymqttlights.config as config
import pymqttlights.utils as utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class Hub:
    """Acts as a really-just-emulated-kind-of-hub to control the connected lights"""

    def __init__(self, broker_address, broker_port, broker_user, broker_password, base_channel):
        """Initialises the hub"""
        self.devices = {}
        self.connected = False
        self.scan_timer = None
        self.is_scanning = False
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.broker_user = broker_user
        self.broker_password = broker_password
        self.base_channel = base_channel
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        logger.debug("Hub initialisation completed.")

    def __repr__(self):
        """String representation for the hub."""
        return f'<MQTTLightsHub {"connected" if self.connected else "disconnected"} - {len(self.devices)} devices>'

    def connect(self):
        """Connects to the MQTT broker and subscribes to relevant channels."""
        if self.broker_user:
            self.mqtt_client.username_pw_set(self.broker_user, self.broker_password)
        if config.MQTT_CERTIFICATE:
            self.mqtt_client.tls_set(config.MQTT_CERTIFICATE)
        self.mqtt_client.connect(self.broker_address, self.broker_port, config.MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()
        logger.debug("MQTT loop started.")

    def on_connect(self, client, userdata, flags, rc):
        """MQTT callback when a connection to the broker has been established."""
        self.connected = True
        logger.debug("Connected to MQTT broker.")

    def on_disconnect(self, client, userdata, rc):
        """MQTT callback when a disconnection from the broker occurs."""
        self.connected = False
        log_message = f'Connection to MQTT broker lost with reason {rc}'
        if rc:
            logger.warn(log_message)
        else:
            logger.debug(log_message)

    def build_channel_from_base(self, channel):
        """Returns a string representation of a channel name, build up from the base channel."""
        return f'{self.base_channel}/{channel}'

    def build_discovery_topic(self, realm=config.MQTT_DEFAULT_REALM):
        """Builds the discovery topic."""
        return f'{self.build_channel_from_base(config.MQTT_DISCOVERY)}/{realm}'

    def subscribe_and_callback(self, topic, callback):
        self.mqtt_client.subscribe(topic, 0)
        self.mqtt_client.message_callback_add(topic, callback)

    def send(self, topic, payload=None, retain=False):
        """Sends the provided topic-payload pair to the MQTT broker."""
        logger.debug(f'Sending {str(payload)} to {topic}')
        self.mqtt_client.publish(topic, payload, retain)

    def scan(self, realm=None):
        """Scans for connected lights, optionally using custom realm."""
        if self.is_scanning:
            logger.warn('Scan request ignored, scan is already running')
            return
        self.subscribe_and_callback(f'{self.build_discovery_topic()}/+/+', self.on_discovery)
        self.send(self.build_discovery_topic())
        if realm:
            self.subscribe_and_callback(f'{self.build_discovery_topic(realm)}/+/+', self.on_discovery)
            self.send(self.build_discovery_topic(realm))
        self.scan_timer = Timer(config.SCAN_TIMEOUT_SECONDS, lambda: self.stop_scan(realm))
        self.scan_timer.start()
        self.is_scanning = True
        logger.debug(f'Starting scan for {config.SCAN_TIMEOUT_SECONDS} seconds in public realm{f" and custom realm {realm}" if realm else ""}')

    def stop_scan(self, realm):
        """Stops the scan for lights by removing the callbacks for the relevant topics."""
        self.mqtt_client.message_callback_remove(f'{self.build_discovery_topic()}/+/+')
        logger.debug('Stopped callbacks for scan in public realm')
        if realm:
            self.mqtt_client.message_callback_remove(f'{self.build_discovery_topic(realm)}/+/+')
            logger.debug(f'Stopped callbacks for scan in custom realm {realm}')
        self.is_scanning = False

    def on_discovery(self, client, userdata, message):
        """Persists a discovered light."""
        light_parts = message.topic.split('/')
        realm = light_parts[2]
        device_name = light_parts[3]
        light_topic = light_parts[4]
        friendly_name = message.payload.decode("utf8")
        logger.debug(f'Discovered light: {message.topic} {friendly_name}')
        self.add_light_and_device(device_name, realm, light_topic, friendly_name)

    def add_light_and_device(self, device_name, realm, light_topic, friendly_name):
        """Adds a given light to the hub."""
        device = self.get_device(device_name)
        if not device:
            logger.info(f'Adding new device with name {device_name}')
            device = Device(self, device_name)
            self.devices[device_name] = device
        device.add_light(realm, light_topic, friendly_name)

    def get_device(self, device_name):
        """Returns a given device if it is already known to the hub."""
        return self.devices.get(device_name, None)

    def get_all_lights(self):
        """Returns all lights of all devices as list."""
        return [light for device in self.devices.values() for light in device.lights.values()]

class Device:
    """Representation of a device which can operate fairylights."""

    def __init__(self, hub, name):
        """Initialises the device."""
        self.hub = hub
        self.name = name
        self.lights = {}

    def __repr__(self):
        """String representation of an MQTT fairylight device."""
        return f'<MQTTDevice {self.name}@{self.hub}>'

    def add_light(self, realm, light_topic, friendly_name):
        """Adds a given light to the hub."""
        light = Light(self.hub, self.name, realm, light_topic, friendly_name)
        if self.is_light_new(light):
            light.enable()
            light.get_status()
            self.lights[light.topic] = light
            logger.debug(f'Added new light, device: {self.name}, topic: {light_topic}, friendly name: {friendly_name}')
        else:
            logger.warn(f'Did not add light because it already exists: device: {self.name}, topic: {light_topic}, friendly name: {friendly_name}')

    def is_light_new(self, new_light):
        """Returns true if the light is not yet known to the hub, or false if it already is."""
        return new_light.topic not in self.lights

    def __eq__(self, other):
        """Customer comparison implementation to compare to other devices."""
        return self.name == (other.name if hasattr(other, 'name') else False)

class Light:
    """Representation of a MQTT fairylight."""

    def __init__(self, hub, device, realm, topic, friendly_name):
        """Initialises the light."""
        self.hub = hub
        self.mqtt_client = self.hub.mqtt_client
        self.device = device
        self.realm = realm
        self.topic = topic
        self.friendly_name = friendly_name
        self.status_topic = self.hub.build_channel_from_base(f'{config.MQTT_DEVICE}/{self.device}/{config.MQTT_LIGHT}/{self.topic}/{config.MQTT_STATUS}')
        self.control_topic = self.hub.build_channel_from_base(f'{config.MQTT_DEVICE}/{self.device}/{config.MQTT_LIGHT}/{self.topic}/{config.MQTT_CONTROL}')
        self.mode = 0
        self.brightness = 10
        self.step = 1
        self.min = 0
        self.max = 100
        self.delay = 100
        self.fade = False
        logger.debug(f'Initialisation complete for light {utils.get_unique_light_identifier(self)}')

    def __repr__(self):
        """String representation of an MQTT fairylight."""
        return f'<MQTTLight {self.topic}@{self.device} {self.friendly_name}>'

    def enable(self):
        """Subscribe to relevant topics for light and add callbacks."""
        self.mqtt_client.subscribe(f'{self.status_topic}/#', 0)
        self.mqtt_client.message_callback_add(f'{self.status_topic}/#', self.status_callback)
        logger.debug(f'Enabling subscriptions and callbacks for light {utils.get_unique_light_identifier(self)}')

    def get_status(self):
        """Requests a general status update for the light."""
        logger.debug(f'Requesting status for light {utils.get_unique_light_identifier(self)}')
        self.hub.send(f'{self.control_topic}', 'get_status')

    def status_callback(self, client, userdata, message):
        """Callback to process incoming status reports."""
        status_parts = message.topic.split('/')
        relevant_property = status_parts[6]
        relevant_value = message.payload.decode('utf8')
        if hasattr(self, f'handle_{relevant_property}') and callable(getattr(self, f'handle_{relevant_property}')):
            logger.debug(f'Forwarding update of property {relevant_property} for {utils.get_unique_light_identifier(self)} to handler handle_{relevant_property}')
            handler = getattr(self, f'handle_{relevant_property}')
            handler(relevant_value)
        elif hasattr(self, relevant_property):
            logger.debug(f'Updating property {relevant_property} for {utils.get_unique_light_identifier(self)}: {getattr(self, relevant_property)} -> {relevant_value}')
            setattr(self, relevant_property, relevant_value)
        else:
            logger.warn(f'Not updating unknown property {relevant_property} with value {relevant_value} for {utils.get_unique_light_identifier(self)}')

    def set_property(self, relevant_property, relevant_value):
        """Sets the given property to the given value for the light."""
        if not hasattr(self, relevant_property):
            logger.warn(f'Not requesting change of unkown property {relevant_property} to {relevant_value} for {utils.get_unique_light_identifier(self)}')
            return
        logger.debug(f'Requesting change of property {relevant_property} for {utils.get_unique_light_identifier(self)}: {getattr(self, relevant_property)} -> {relevant_value}')
        self.hub.send(f'{self.control_topic}/{relevant_property}', relevant_value)

    def handle_brightness(self, new_brightness):
        """Bespoke handler for brightness status messages."""
        logger.debug(f'Updating brightness and setting fade flag to False for {utils.get_unique_light_identifier(self)}: {self.brightness} -> {new_brightness}')
        self.brightness = new_brightness
        self.fade = False

    def handle_fade(self, new_brightness):
        """Bespoke handler for brightness status messages."""
        logger.debug(f'Updating brightness and setting fade flag to True for {utils.get_unique_light_identifier(self)}: {self.brightness} -> {new_brightness}')
        self.brightness = new_brightness
        self.fade = True
