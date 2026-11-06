#!/bin/bash
# Doppelklick startet die Bedienoberfläche des Webseiten-Generators im Browser.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  echo "Richte Python-Umgebung ein (einmalig) …"
  python3 -m venv .venv && .venv/bin/pip install -q requests openpyxl
fi
exec .venv/bin/python generator/gui.py
