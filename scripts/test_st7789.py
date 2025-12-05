#!/usr/bin/env python

# Quick test script for ST7789 display
# This script tests the ST7789 display connection and shows a test pattern

import sys
import time
import RPi.GPIO as GPIO

try:
    from luma.core.interface.serial import spi
    from luma.lcd.device import st7789
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install: pip3 install luma.lcd pillow RPi.GPIO")
    sys.exit(1)

# Cleanup GPIO
GPIO.cleanup()

# Display configuration for Waveshare 1.3inch IPS LCD Display HAT (240x240)
SPI_PORT = 0
SPI_DEVICE = 0
SPI_SPEED = 40000000
GPIO_DC = 25  # Data/Command pin for WAVESHARE HAT
GPIO_RST = 27  # Reset pin for WAVESHARE HAT
GPIO_BACKLIGHT = 18  # Backlight pin (may vary, check your HAT)
WIDTH = 240  # Waveshare 1.3inch IPS LCD Display HAT
HEIGHT = 240  # Waveshare 1.3inch IPS LCD Display HAT

print("ST7789 Display Test")
print("=" * 50)

# Try to initialize SPI connection
print("\n1. Testing SPI connection...")
try:
    # Try WAVESHARE configuration first (with GPIO pins)
    print("   Trying WAVESHARE configuration (DC=25, RST=27)...")
    serial = spi(port=SPI_PORT, device=SPI_DEVICE, bus_speed_hz=SPI_SPEED, gpio_DC=GPIO_DC, gpio_RST=GPIO_RST)
    print("   ✓ SPI connection established (WAVESHARE mode)")
    use_waveshare = True
except Exception as e:
    print(f"   ✗ WAVESHARE config failed: {e}")
    try:
        # Try standard SPI configuration
        print("   Trying standard SPI configuration...")
        serial = spi(port=SPI_PORT, device=SPI_DEVICE, bus_speed_hz=SPI_SPEED)
        print("   ✓ SPI connection established (standard mode)")
        use_waveshare = False
    except Exception as e2:
        print(f"   ✗ Standard SPI config failed: {e2}")
        print("\nERROR: Could not establish SPI connection")
        sys.exit(1)

# Try to initialize display
print("\n2. Initializing ST7789 display...")
try:
    device = st7789(
        serial_interface=serial,
        width=WIDTH,
        height=HEIGHT,
        h_offset=0,
        v_offset=0,
        gpio_LIGHT=GPIO_BACKLIGHT,
        bgr=False,
        inverse=False
    )
    print(f"   ✓ Display initialized: {device.width}x{device.height}")
    print(f"   Display mode: {device.mode}")
except Exception as e:
    print(f"   ✗ Display initialization failed: {e}")
    print("\nERROR: Could not initialize display")
    sys.exit(1)

# Configure display
print("\n3. Configuring display...")
try:
    device.capabilities(width=WIDTH, height=HEIGHT, rotate=0, mode='RGB')
    device.contrast(255)
    device.backlight(True)
    print("   ✓ Display configured")
except Exception as e:
    print(f"   ✗ Configuration failed: {e}")

# Test 1: Fill screen with colors
print("\n4. Test 1: Color fill test...")
try:
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 255), # White
        (0, 0, 0),      # Black
    ]
    
    for i, color in enumerate(colors):
        print(f"   Showing {color}...")
        image = Image.new('RGB', (device.width, device.height), color)
        device.display(image)
        time.sleep(1)
    print("   ✓ Color fill test passed")
except Exception as e:
    print(f"   ✗ Color fill test failed: {e}")

# Test 2: Text display
print("\n5. Test 2: Text display test...")
try:
    image = Image.new('RGB', (device.width, device.height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 24)
        except:
            font = ImageFont.load_default()
            print("   Using default font")
    
    # Draw text
    text = "ST7789 Test"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (device.width - text_width) // 2
    y = (device.height - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    draw.text((x, y + text_height + 10), "Working!", fill=(0, 255, 0), font=font)
    
    device.display(image)
    print("   ✓ Text display test passed")
    print("   You should see 'ST7789 Test' and 'Working!' on the display")
    time.sleep(3)
except Exception as e:
    print(f"   ✗ Text display test failed: {e}")

# Test 3: Pattern test
print("\n6. Test 3: Pattern test...")
try:
    image = Image.new('RGB', (device.width, device.height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a grid pattern
    step = 20
    for x in range(0, device.width, step):
        draw.line([(x, 0), (x, device.height)], fill=(128, 128, 128), width=1)
    for y in range(0, device.height, step):
        draw.line([(0, y), (device.width, y)], fill=(128, 128, 128), width=1)
    
    # Draw colored squares
    draw.rectangle([10, 10, 50, 50], fill=(255, 0, 0))    # Red
    draw.rectangle([60, 10, 100, 50], fill=(0, 255, 0))    # Green
    draw.rectangle([110, 10, 150, 50], fill=(0, 0, 255))   # Blue
    
    device.display(image)
    print("   ✓ Pattern test passed")
    print("   You should see a grid pattern with colored squares")
    time.sleep(3)
except Exception as e:
    print(f"   ✗ Pattern test failed: {e}")

# Final message
print("\n" + "=" * 50)
print("Test completed!")
print("If you see graphics on the display, the ST7789 is working correctly.")
print("If the display is blank, check:")
print("  - SPI is enabled: sudo raspi-config -> Interface Options -> SPI -> Enable")
print("  - Wiring connections (DC, RST, CS, MOSI, MISO, SCLK)")
print("  - Backlight pin connection")
print("  - Display resolution settings (width/height)")
print("=" * 50)

# Keep display on for a bit
time.sleep(2)

