#!/usr/bin/env bash
# SC Handels-Planer neu bauen (Doppelklick auf macOS).
cd "$(dirname "$0")" || exit 1
python3 handels_planer_bauen.py && echo "Fertig. SC_Handels_Planer.html wurde aktualisiert."
