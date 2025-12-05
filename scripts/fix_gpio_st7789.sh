#!/bin/bash

# Script to fix GPIO issues for ST7789 WAVESHARE display
# This ensures GPIO pins are available before starting display

echo "Fixing GPIO for ST7789 WAVESHARE display..."

# Kill any processes that might be using GPIO
sudo pkill -f display.py
sleep 1

# Check if SPI is enabled
if ! lsmod | grep -q spi_bcm; then
    echo "WARNING: SPI module not loaded. Enable SPI in raspi-config."
fi

# Check for GPIO conflicts
echo "Checking GPIO pin usage..."
for pin in 25 27 18; do
    if [ -f "/sys/class/gpio/gpio${pin}/value" ]; then
        echo "  GPIO ${pin} is exported"
    fi
done

echo "Starting display daemon..."
sudo python3 /var/www/little-backup-box/display.py > /tmp/display.log 2>&1 &
sleep 2

if pgrep -f display.py > /dev/null; then
    echo "✓ Display daemon started successfully"
    echo "Check /tmp/display.log for any errors"
else
    echo "✗ Display daemon failed to start"
    echo "Errors:"
    cat /tmp/display.log 2>/dev/null || echo "No log file found"
fi

