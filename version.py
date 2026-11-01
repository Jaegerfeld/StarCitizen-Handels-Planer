# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       25.10.2026
# Geändert:       01.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Einzige Quelle der Versionsnummer des Handels-Planers (SemVer) und des
#   Star-Citizen-Spielstands, auf den sich die Daten beziehen. Gelesen von
#   handels_planer_bauen.py (Kopfzeile, data.json, Routen-Guide).
#   PATCH wird bei jedem neuen Live-Patch von Hand nachgezogen.
# =============================================================================
"""Central version numbers of the StarCitizen trade planner."""
#: Tool version (SemVer), shown in the page header and written to data.json.
VERSION = "1.5.1"
#: Game version the price data refers to (update on each new live patch).
PATCH = "4.10.2-LIVE"   # Spielstand, auf den sich die Daten beziehen (bei neuem Patch anpassen)
