#!/usr/bin/env python

# Send a test message to the display to verify it's working

import sys
import os

# Add the scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import lib_display
except ImportError as e:
    print(f"Error importing libraries: {e}")
    sys.exit(1)

print("Sending test message to display...")
print("=" * 50)

# Create display object and send test message
display = lib_display.display()

# Send a test message
test_lines = [
    'set:clear,time=5',
    's=h:ST7789 Display Test',
    's=b:Resolution: 240x240',
    's=b:Driver: ST7789 WAVESHARE',
    's=a:If you see this, it works!'
]

print("\nSending message:")
for line in test_lines:
    print(f"  {line}")

display.message(test_lines, logging=True)

print("\n" + "=" * 50)
print("Message sent!")
print("The display should show the test message for 5 seconds.")
print("If you don't see anything, check:")
print("  1. Display is enabled in config (conf_DISP=true)")
print("  2. Display driver is set to 'ST7789 WAVESHARE'")
print("  3. Resolution is set to 240x240")
print("  4. Connection is set to 'SPI'")
print("  5. Display daemon is running: sudo pgrep -fa display.py")
print("=" * 50)

