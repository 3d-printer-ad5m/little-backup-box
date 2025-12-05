#!/usr/bin/env python

# Test display with actual configuration from config.cfg
# This script reads the config and tests the display

import sys
import os
import RPi.GPIO as GPIO

# Add the scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import lib_setup
    from luma.core.interface.serial import spi
    from luma.lcd.device import st7789
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Error importing libraries: {e}")
    sys.exit(1)

# Cleanup GPIO
GPIO.cleanup()

print("Testing Display with Configuration")
print("=" * 50)

# Load configuration
setup = lib_setup.setup()

conf_DISP_CONNECTION = setup.get_val('conf_DISP_CONNECTION')
conf_DISP_DRIVER = setup.get_val('conf_DISP_DRIVER')
conf_DISP_SPI_PORT = setup.get_val('conf_DISP_SPI_PORT')
conf_DISP_RESOLUTION_X = setup.get_val('conf_DISP_RESOLUTION_X')
conf_DISP_RESOLUTION_Y = setup.get_val('conf_DISP_RESOLUTION_Y')
conf_DISP_OFFSET_X = setup.get_val('conf_DISP_OFFSET_X')
conf_DISP_OFFSET_Y = setup.get_val('conf_DISP_OFFSET_Y')
conf_DISP_BACKLIGHT_PIN = setup.get_val('conf_DISP_BACKLIGHT_PIN')
conf_DISP_BACKLIGHT_ENABLED = setup.get_val('conf_DISP_BACKLIGHT_ENABLED')
conf_DISP_COLOR_BGR = setup.get_val('conf_DISP_COLOR_BGR')
conf_DISP_COLOR_INVERSE = setup.get_val('conf_DISP_COLOR_INVERSE')

print(f"\nConfiguration:")
print(f"  Driver: {conf_DISP_DRIVER}")
print(f"  Connection: {conf_DISP_CONNECTION}")
print(f"  Resolution: {conf_DISP_RESOLUTION_X}x{conf_DISP_RESOLUTION_Y}")
print(f"  Offset: {conf_DISP_OFFSET_X}, {conf_DISP_OFFSET_Y}")
print(f"  Backlight Pin: {conf_DISP_BACKLIGHT_PIN}")
print(f"  Backlight Enabled: {conf_DISP_BACKLIGHT_ENABLED}")

if conf_DISP_DRIVER not in ['ST7789', 'ST7789 WAVESHARE']:
    print(f"\nERROR: Display driver is '{conf_DISP_DRIVER}', not ST7789!")
    print("Please configure the display driver in the web interface.")
    sys.exit(1)

if conf_DISP_CONNECTION != 'SPI':
    print(f"\nERROR: Connection is '{conf_DISP_CONNECTION}', not SPI!")
    print("Please configure the connection type in the web interface.")
    sys.exit(1)

# Initialize SPI
print(f"\n1. Initializing SPI connection...")
try:
    if conf_DISP_DRIVER == 'ST7789 WAVESHARE':
        serial = spi(port=int(conf_DISP_SPI_PORT), device=0, bus_speed_hz=40000000, gpio_DC=25, gpio_RST=27)
        print("   ✓ SPI initialized (WAVESHARE mode: DC=25, RST=27)")
    else:
        serial = spi(port=int(conf_DISP_SPI_PORT), device=0, bus_speed_hz=40000000)
        print("   ✓ SPI initialized (standard mode)")
except Exception as e:
    print(f"   ✗ SPI initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Initialize display
print(f"\n2. Initializing ST7789 display...")
try:
    backlight_pin = int(conf_DISP_BACKLIGHT_PIN) if conf_DISP_BACKLIGHT_PIN > 0 else 18
    
    device = st7789(
        serial_interface=serial,
        width=int(conf_DISP_RESOLUTION_X),
        height=int(conf_DISP_RESOLUTION_Y),
        h_offset=int(conf_DISP_OFFSET_X),
        v_offset=int(conf_DISP_OFFSET_Y),
        gpio_LIGHT=backlight_pin,
        bgr=bool(conf_DISP_COLOR_BGR),
        inverse=bool(conf_DISP_COLOR_INVERSE)
    )
    print(f"   ✓ Display initialized: {device.width}x{device.height}")
    print(f"   Display mode: {device.mode}")
except Exception as e:
    print(f"   ✗ Display initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Configure display
print(f"\n3. Configuring display...")
try:
    device.capabilities(
        width=int(conf_DISP_RESOLUTION_X),
        height=int(conf_DISP_RESOLUTION_Y),
        rotate=0,
        mode='RGB'
    )
    device.contrast(255)
    device.backlight(bool(conf_DISP_BACKLIGHT_ENABLED))
    print("   ✓ Display configured")
except Exception as e:
    print(f"   ✗ Configuration failed: {e}")
    import traceback
    traceback.print_exc()

# Test display with content
print(f"\n4. Testing display output...")
try:
    # Create a test image
    image = Image.new('RGB', (device.width, device.height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw background
    draw.rectangle([0, 0, device.width, device.height], fill=(0, 0, 255))
    
    # Draw text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
        except:
            font = ImageFont.load_default()
    
    text = f"{conf_DISP_DRIVER}"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (device.width - text_width) // 2
    y = (device.height - text_height) // 2 - 20
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    draw.text((x, y + text_height + 10), f"{conf_DISP_RESOLUTION_X}x{conf_DISP_RESOLUTION_Y}", fill=(0, 255, 0), font=font)
    draw.text((x, y + (text_height + 10) * 2), "Working!", fill=(255, 255, 0), font=font)
    
    # Display the image
    device.display(image)
    print("   ✓ Test image displayed")
    print("   You should see blue background with white/green/yellow text")
    
except Exception as e:
    print(f"   ✗ Display test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test completed!")
print("If you see the test image, the display hardware is working.")
print("If the display is blank, check the configuration values above.")
print("=" * 50)

