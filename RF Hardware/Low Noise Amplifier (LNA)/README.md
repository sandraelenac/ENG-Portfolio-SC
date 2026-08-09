# Low Noise Amplifier (LNA)

## Objective

Design a 50 Ω (OHM) LNA printed circuit board (PCB) using **PSpice** for simulation and **KiCad** for schecmatic/layout/manufacturing files.

## Project Status: Rev 0.2
**Curent Revision:** Rev 0.2 - Design / Component Selection See [CHANGELOG.md](CHANGELOG.md) for the complete design revision history.

---
## Electrical Requirements
- Frquency Range: 100Mhz - 1 GHz
- Small Signal Gain: 10 - 20 dB
- Gain Flatness: +/- 1.5 dB
- Noise Figure: charterize
- Input Return Loss: better than -10 dB
- Output Return Loss: better than -10 dB
- Input Impedance: 50 Ω 
- Output Impedance: 50 Ω 
- Supply Voltage: 5 VDC
- Supply Current: <150mA
- Manufacturer: Texas Instrument (TI)

---
## Block Diagram
A simple block diagram is shown below to illustrate the LNA within a receiver front end. The signal received by the antenna passes through an antenna switch, RF preselector, and impedance-matching network before entering the LNA. After amplification, the signal passes through an output-matching network and is routed to the mixer and filter for further processing. 

<p align="center">
  <img src="1. Design/LNA-Block-Diagram.png" alt="Simple RX LNA Block Diagram" width="1000">
</p>

---
# PSPICE Schematic

---
# PSPICE Simulation Results

---
# KICAD Schematic 

## PCB Layout
