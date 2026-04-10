#!/bin/bash
# ==============================================================================
# Student Attendance & Engagement Tracker - Linux/Mac Startup Script
# Run this file: bash run.sh
# ==============================================================================

clear

cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     🎓 STUDENT ATTENDANCE & ENGAGEMENT TRACKER                ║
║                                                                ║
║              Starting Application...                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

EOF

echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python first."
    echo "   On Ubuntu: sudo apt-get install python3"
    echo "   On Mac: brew install python3"
    exit 1
fi

echo "✅ Python found!"
echo ""

# Run the universal launcher
python3 run.py
