#!/bin/bash

# Script to disable all backup scripts on startup
# This removes backup-autorun.py from crontab

echo "Disabling backup scripts on startup..."
echo ""

# Backup current crontab
if crontab -l > /tmp/crontab_backup.txt 2>/dev/null; then
    echo "✓ Backed up current crontab to /tmp/crontab_backup.txt"
else
    echo "No existing crontab found"
fi

# Remove backup-autorun.py from crontab
crontab -l 2>/dev/null | grep -v "backup-autorun" | crontab -

echo "✓ Removed backup-autorun.py from crontab"
echo ""

# Show updated crontab
echo "=== Updated Crontab ==="
crontab -l 2>/dev/null || echo "Crontab is now empty"
echo ""

# Stop any currently running backup processes
echo "Stopping any running backup processes..."
sudo /var/www/little-backup-box/stop_backup.sh 2>&1
echo ""

echo "=== Summary ==="
echo "✓ backup-autorun.py removed from startup"
echo "✓ Running backup processes stopped"
echo ""
echo "Backup scripts will no longer run automatically on startup."
echo "You can still start backups manually via the web interface or command line."

