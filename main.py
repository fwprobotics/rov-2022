"""
Write some description
"""

import pygame
import serial
import sys
import time
# Add any imports you need


def setup() -> tuple:
    """
    Fill this function out with any setup that you need to do.
    Can include starting the UI, creating the serial object, etc.
    """
    return None, None


def get_gamepad_event():
    """
    Receive the event from either a real gamepad or something you fake
    """
    return None


def get_rov_mode() -> tuple:
    """Get the speed settings, tool lockouts, etc from the UI"""
    return None, None, None


def map_inputs(gamepad_input, rov_speed_mode) -> tuple:
    """
    Map the gamepad's buttons to things like direction, tool control, etc
    This should only be to adapt buttons into something like 'forward'
    """
    return None, None


def scale_direction(commanded_direction, rov_speed_mode):
    """
    Give our commanded direction a magnituve
    """
    return None


def vector_to_message(commanded_vector, thruster_config) -> bytes:
    """Convert the commanded vector into actual thruster commanded and stuff that into a message for the arduino"""
    return b''


def tools_to_message():
    """Convert the desired state of the tools into a message the arduino can receive"""
    return None


def send_message(arduino_communicator, message: bytes):
    """Send a message to the arduino (or just print it if you're simulating/testing"""
    if message:
        pass


def handle_incoming_data(arduino_communicator):
    """"""
    if data_is_available:
        pass


def main(args: list) -> None:
    """"""
    arduino_communicator, pilot_profile = setup()
    
    while True:
        # Get the gamepad input for what buttons the pilot is pressing
        gamepad_input = get_gamepad_event()

        # Get the speed mode, tool lockouts, thruster adjustments, etc from the UI
        rov_speed_mode, tool_mode, thruster_config = get_rov_mode()
        
        # Go from buttons that the pilot pressed to when they mean in terms of which way the ROV goes
        commanded_direction, tool_command = map_inputs(gamepad_input, pilot_profile)

        # Scale the commanded direction to the speed the pilot set in the UI
        commanded_vector = scale_direction(commanded_direction, rov_speed_mode)

        # Convert the commanded direction and speed to a message that the arduino can receive and send it
        send_message(arduino_communicator, vector_to_message(commanded_vector, thruster_config))

        # Convert the tools command to a message that the arduino can receive and send it
        send_message(arduino_communicator, tools_to_message(tool_command, tool_mode))

        # Check for and handle and incoming data from the arduino
        handle_incoming_data(arduino_communicator)

        # Pause a little before repeating the loop
        time.sleep(0.005)


if __name__ == "__main__":
    main(sys.argv[1:])
