#!/usr/bin/env bash
# SC Handels-Planer neu bauen (Preise live von star-head.de ziehen).
cd "$(dirname "$0")" || exit 1
python3 handels_planer_bauen.py && echo "Fertig. SC_Handels_Planer.html wurde aktualisiert."
