# ST7789 Display Diagnostic Guide

## Quick Tests

Run these commands on your Raspberry Pi to diagnose the display:

### 1. Test Display with Configuration
```bash
sudo python3 /var/www/little-backup-box/test_display_config.py
```
This will:
- Load your actual configuration
- Test SPI connection
- Initialize the display
- Show a test pattern

### 2. Test Display with Message System
```bash
sudo python3 /var/www/little-backup-box/test_display_message.py
```
This will:
- Send a test message through the display system
- Verify the display daemon can receive and show messages

### 3. Check Display Configuration
```bash
sudo cat /var/www/little-backup-box/config.cfg | grep -E "conf_DISP_DRIVER|conf_DISP_CONNECTION|conf_DISP_RESOLUTION"
```

Expected values:
- `conf_DISP_DRIVER="ST7789 WAVESHARE"` or `"ST7789"`
- `conf_DISP_CONNECTION="SPI"`
- `conf_DISP_RESOLUTION_X=240`
- `conf_DISP_RESOLUTION_Y=240`

### 4. Check if Display Daemon is Running
```bash
sudo pgrep -fa display.py
```

### 5. Restart Display Daemon
```bash
sudo pkill -f display.py
sudo python3 /var/www/little-backup-box/display.py &
```

### 6. Check for Errors
```bash
sudo python3 /var/www/little-backup-box/display.py 2>&1 | head -50
```

## Common Issues

### Display is Blank but Test Script Works
- **Cause**: Display daemon may have failed initialization
- **Fix**: Restart the display daemon after configuration changes
- **Check**: Verify `hardware_ready` is True (check logs)

### Configuration Not Applied
- **Cause**: Config changes not saved or daemon not restarted
- **Fix**: 
  1. Save configuration in web interface
  2. Restart display daemon: `sudo pkill -f display.py && sudo python3 /var/www/little-backup-box/display.py &`

### SPI Not Enabled
- **Fix**: `sudo raspi-config` → Interface Options → SPI → Enable
- **Reboot**: Required after enabling SPI

### Wrong Resolution
- **Check**: Resolution must be 240x240 for Waveshare 1.3inch IPS LCD
- **Fix**: Set in web interface: Horizontal=240, Vertical=240

## Manual Test

To manually test the display without the daemon:

```bash
sudo python3 /var/www/little-backup-box/test_st7789.py
```

This should show:
- Color fills (red, green, blue, white, black)
- Text display
- Grid pattern

If this works but the daemon doesn't, the issue is in the display.py initialization or message system.

