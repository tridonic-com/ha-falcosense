<img src="icon.png" alt="Tridonic FalcoSENSE" width="128" align="right" />

# Tridonic FalcoSENSE — HACS test distribution

[![HACS](https://github.com/tridonic-com/ha-falcosense/actions/workflows/hacs.yml/badge.svg)](https://github.com/tridonic-com/ha-falcosense/actions/workflows/hacs.yml)
[![Hassfest](https://github.com/tridonic-com/ha-falcosense/actions/workflows/hassfest.yml/badge.svg)](https://github.com/tridonic-com/ha-falcosense/actions/workflows/hassfest.yml)
[![Release](https://img.shields.io/github/v/release/tridonic-com/ha-falcosense?sort=semver)](https://github.com/tridonic-com/ha-falcosense/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/tridonic-com/ha-falcosense#readme)
[![License](https://img.shields.io/github/license/tridonic-com/ha-falcosense)](LICENSE)

Pre-release distribution of the **Tridonic FalcoSENSE** Home Assistant
integration for early testers, before it is available in Home Assistant core. It
integrates the [Tridonic FalcoSENSE](https://www.tridonic.com/de/int/product/32878)
people-counting / occupancy sensor over its local REST and MQTT APIs.

> This is a temporary channel. Once the integration ships in Home Assistant core,
> install it from there and remove this custom repository.

## Requirements

- A running Home Assistant instance (OS, Container, or Supervised recommended;
  these ship `git`, which is needed to install the `falcosense` dependency).
- [HACS](https://hacs.xyz) installed.
- Network access on the Home Assistant host (first setup installs the
  `falcosense` library from GitHub via pip).
- A commissioned FalcoSENSE sensor on your network with the MQTT endpoint enabled
  and an API token generated in its dashboard.

## Install

1. Add the repository to HACS, either with the button below or manually via
   **HACS → Integrations → three-dot menu → Custom repositories** (add this
   repository's URL with category **Integration**):

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tridonic-com&repository=ha-falcosense&category=integration)
2. Find **Tridonic FalcoSENSE** in HACS, install it, then **restart Home
   Assistant**.
3. Go to **Settings → Devices & Services → Add integration**, search for
   **FalcoSENSE** (under the Tridonic brand), and enter the sensor's host and
   API token.

## How this repo is maintained

The integration here is a copy of the core integration, kept in sync with
[`scripts/sync.py`](scripts/sync.py), which copies
`homeassistant/components/falcosense/` from a local Home Assistant core checkout
and applies the two changes a HACS custom integration needs: a `version` field
and a git-URL requirement for the `falcosense` library. Re-run it after any
change in core and cut a matching release tag.
