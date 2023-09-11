import RPi.GPIO as GPIO
import time

# Disable GPIO warnings to prevent unnecessary notifications
GPIO.setwarnings(False)

# Define GPIO pin assignments for the ultrasonic sensor and LED
TRIG_PIN = 21  # Trigger pin
ECHO_PIN = 20  # Echo pin
LED_PIN = 4    # LED pin (example pin; use a suitable GPIO pin)

# Configure GPIO mode to use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)

# Set up PWM for controlling LED brightness
GPIO.setup(LED_PIN, GPIO.OUT)
led_pwm = GPIO.PWM(LED_PIN, 100)  # 100 Hz PWM frequency
led_pwm.start(0)  # Start with 0% brightness

# Define brightness levels for 10 stages (5cm, 10cm, ..., 50cm)
brightness_levels = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

# Continuously perform distance measurements
while True:
    print("Measuring distance...")

    # Configure the trigger and echo pins
    GPIO.setup(TRIG_PIN, GPIO.OUT)  # Set TRIG_PIN as an output
    GPIO.setup(ECHO_PIN, GPIO.IN)   # Set ECHO_PIN as an input

    # Send a trigger signal to initiate distance measurement
    GPIO.output(TRIG_PIN, False)     # Ensure TRIG_PIN is low
    print("Waiting for the sensor to settle")
    time.sleep(0.2)                 # Allow time for sensor stability
    GPIO.output(TRIG_PIN, True)      # Generate a brief trigger pulse
    time.sleep(0.00001)              # Keep TRIG_PIN high for 10 microseconds
    GPIO.output(TRIG_PIN, False)     # Turn off the trigger pulse

    # Measure the duration of the echo pulse to calculate distance
    while GPIO.input(ECHO_PIN) == 0:  # Wait for the echo to start
        pulse_start_time = time.time() # Record the start time of the echo pulse
    while GPIO.input(ECHO_PIN) == 1:  # Wait for the echo to end
        pulse_end_time = time.time()   # Record the end time of the echo pulse

    # Calculate the duration of the echo pulse (time taken for sound to return)
    pulse_duration = pulse_end_time - pulse_start_time

    # Calculate the distance in centimeters using the speed of sound (17150 cm/s)
    distance = pulse_duration * 17150

    # Round the distance to the nearest multiple of 5
    distance = 2 * round(distance / 2)

    # Display the measured distance
    print("Distance:", distance, "cm")

    # Control LED brightness based on distance
    if distance >= 0 and distance <= 20:  # Within the specified range
        index = int((distance - 2) / 2)  # Map distance to brightness level
        led_pwm.ChangeDutyCycle(brightness_levels[index])
    else:  # Beyond the specified range
        led_pwm.ChangeDutyCycle(0)  # Turn off the LED

    # Wait for 1 second before the next measurement
    time.sleep(1)
