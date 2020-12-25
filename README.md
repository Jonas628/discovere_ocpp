# Chargesim # 

Dieses Projekt ist eine Simulation der wesentlichen Aspekte des Lademanagements.

## Installation ##
Die Dependencies können via pip über die requirements.txt Datei
installiert werden: \
`pip install -r requirements.txt`

## 1. Kommunikation zwischen CS und CP ##
g
Der einfachste Fall eines Ladesystems besteht aus einem Central System (CS) und einem
Charging Point (CP).

Das CS wird über die Konsole gestartet, hostet dann lokalen websocket server und wartet darauf,
dann sich ein CP verbindet:

input:\
`python central_system.py`\
output:\
`### starting the central system ###`

Der CP wird in einem neuen Thread gestartet, verbindet sich mit dem CS,
sendet eine Boot-Notification und dann in regelmäßigen Intervallen
Heartbeats. Diese werden vom CS angezeigt:

input:\
`python charging_point.py`\
output:\
`ChargePoint Connected!`\
`Connected to central system.`

## 2. Laden eines Fahrzeugs ##

## 3. Lastmanagement ##

## 4. Lademanagement ##



