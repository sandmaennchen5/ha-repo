"""Check the actual decoder capabilities at image build and container start."""
import subprocess
from pathlib import Path
from owrx.config.core import CoreConfig
CoreConfig.load(Path("/etc/openwebrx/openwebrx.conf"))
from owrx.modes import Modes
from csdr.chain.toolbox import ZveiDemodulator
from owrx.feature import FeatureDetector
if not FeatureDetector().is_available("rtl_sdr"):
    raise SystemExit("RTL-SDR connector unavailable")

mode = Modes.findByModulation("zvei")
if mode is None or not mode.is_available():
    raise SystemExit("OpenWebRX+ ZVEI/multimon-ng support is unavailable")
result = subprocess.run(["multimon-ng", "--help"], capture_output=True, text=True, check=False)
for decoder in ("ZVEI1", "ZVEI2", "ZVEI3", "DZVEI", "PZVEI"):
    if decoder not in result.stdout + result.stderr:
        raise SystemExit(f"multimon-ng decoder missing: {decoder}")
print("OpenWebRX+ ZVEI and multimon-ng decoders available", flush=True)

for feature in ("rds", "packet", "ism", "page", "selcall", "mp3"):
    if not FeatureDetector().is_available(feature):
        raise SystemExit(f"Required decoder feature unavailable: {feature}")
print("RDS, APRS/packet, ISM, paging, SelCall and MP3 features available", flush=True)

from background import check_api
check_api()
from paho.mqtt.client import Client
print("Background ZVEI extension API and MQTT client available", flush=True)

from rds import check_api as check_rds_api
check_rds_api()
print("RDS metadata extension API available", flush=True)
