# Changelog


## [1.2.117.1] - 2026-11-04

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/luarvique/openwebrx

---

## [1.2.117] - 2026-06-26

### Upstream Release Notes

Stanislav (LZ2SLL) has built this SD card image for Raspberry Pi containing a clean OpenWebRX+ 1.2.117 installation. **The image should run on all devices except for RPI1, RPI2, and RPIZero1** and supports all common SDR devices out of the box. The RTL-SDR and SDRPlay devices have been confirmed to work with no additional modifications to the image.

To flash image to an SD card, run [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and click _"APP OPTIONS"_ button, then click _"EDIT"_ button on the _"Content Repository"_. Select _"Use Custom File"_ option, then browse to the JSON file you downloaded from this page.

**Prior to flashing SD card, you can tell RPI Imager to set up the root password.** If you skip this step, you will be asked to create root password on the first startup.

Please note that **this image comes without the software support for digital modes** (DMR, NXDN, etc), since the software decoder for these modes (mbelib) has questionable origins. In order to enable digital modes in this image, ssh into the user account you created while installing the image and type:

`sudo install-softmbe.sh`

Weitere Informationen: https://github.com/luarvique/openwebrx/releases/latest

---

