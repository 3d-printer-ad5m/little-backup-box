#!/bin/bash

# Script to disable backup scripts on startup
# This removes the backup-autorun.py from crontab

WORKING_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
const_WEB_ROOT_LBB="/var/www/little-backup-box"

echo "Disabling backup scripts on startup..."

# Remove backup-autorun.py from crontab
crontab -l 2>/dev/null | grep -v "backup-autorun.py" | crontab -

# Also check root crontab
sudo crontab -l 2>/dev/null | grep -v "backup-autorun.py" | sudo crontab - 2>/dev/null

echo "✓ Backup autorun removed from crontab"
echo ""
echo "Current crontab:"
crontab -l 2>/dev/null || echo "No user crontab"
echo ""
echo "Root crontab:"
sudo crontab -l 2>/dev/null || echo "No root crontab"

