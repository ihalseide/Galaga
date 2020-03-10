#!/bin/bash
cd "$(dirname "$0")"
exec python galaga.py > output.txt
read -p "Press [Enter] key to close..."
