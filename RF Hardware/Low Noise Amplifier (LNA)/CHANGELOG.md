# LNA Project Change Log

This document tracks major requirement, architecture, component-selection, simulation, and PCB design changes throughout the LNA project.

The purpose of this change log is to document the evolution of the design and the engineering rationale behind significant design decisions.

---

## Revision 0.2 – PSpice Simulation Requirement

**Date:** August 2026  
**Status:** In Development

### Change Summary

The project requirements and amplifier architecture were revised to make PSpice simulation a primary design objective alongside KiCad PCB design.

### Original Design

The original project was defined as a broadband RF low-noise amplifier with the following primary requirements:

- Frequency range: 500 MHz–2 GHz
- Small-signal gain: 18–20 dB
- Gain flatness: ±1 dB
- Noise figure: <1.5 dB
- Input/output impedance: 50 Ω
- Input return loss: better than -10 dB
- Output return loss: better than -10 dB
- Supply voltage: 5 VDC
- Supply current: <100 mA
- Output P1dB: ≥+18 dBm

The original component-selection approach focused primarily on dedicated RF LNA and RF gain-block ICs.

### Reason for Change

During component research, several dedicated RF LNAs were identified that could potentially satisfy the original RF requirements. However, manufacturer-supported PSpice models were not consistently available for these devices.

One of the primary objectives of this portfolio project is to demonstrate both:

1. Circuit design and simulation using PSpice.
2. RF schematic and PCB design using KiCad.

Because of this objective, PSpice model availability was elevated from a preferred feature to a mandatory component-selection requirement.

### Architecture Change

The design approach was changed from:

Dedicated RF LNA / RF gain block

to:

TI high-speed, low-noise amplifier suitable for RF/IF applications with manufacturer-supported PSpice simulation.

This change allows the project to demonstrate a more complete simulation workflow while retaining high-frequency PCB design and RF signal-integrity considerations.

### Requirement Changes

| Parameter | Original Requirement | Revised Requirement |
|---|---|---|
| Amplifier Architecture | Dedicated RF LNA | High-speed low-noise RF/IF amplifier |
| Manufacturer | Any | Texas Instruments preferred/required for PSpice workflow |
| PSpice Model | Preferred | Required |
| Frequency Range | 500 MHz–2 GHz | 100 MHz–1 GHz target |
| Extended Frequency Characterization | N/A | Up to 2 GHz |
| Gain | 18–20 dB | 10–20 dB configurable/target |
| Gain Flatness | ±1 dB | ±1.5 dB target |
| Noise Figure | <1.5 dB | Characterize and minimize |
| Input Interface | 50 Ω | 50 Ω single-ended |
| Output Interface | 50 Ω | 50 Ω or differential depending on architecture |
| Supply Voltage | 5 V | 5 V preferred |
| Supply Current | <100 mA | <150 mA target |
| Output P1dB | ≥+18 dBm | Characterize based on selected amplifier |
| PCB | 4-layer FR-4 | No change |
| PSpice AC Analysis | Required | Required |
| PSpice Transient Analysis | Required | Required |
| PSpice Noise Analysis | If supported | Required where model permits |

### Engineering Impact

The revised architecture increases the amount of circuit-level engineering that can be demonstrated within the project.

PSpice will now be used to evaluate:

- DC operating point
- AC frequency response
- Gain versus frequency
- Input and output bias conditions
- Transient response
- Power-up behavior
- Power consumption
- Noise performance
- Supply-voltage variation
- Temperature variation
- Component tolerance sensitivity

The KiCad portion of the project will continue to demonstrate:

- High-frequency schematic design
- 4-layer PCB stackup
- Controlled-impedance routing
- 50 Ω transmission lines
- Differential routing where applicable
- Ground-plane design
- Via stitching
- RF/DC isolation
- SMA interfaces
- Power-supply decoupling
- Manufacturing outputs

### Component Selection Impact

Amplifiers without suitable PSpice model support may be rejected even when their RF performance is superior.

This is an intentional engineering trade made to satisfy the portfolio objective of demonstrating both simulation and physical PCB implementation.

A separate component-selection trade study documents all evaluated devices and the justification for their acceptance or rejection.

### Current Direction

The TI LMH5401 is currently the leading candidate for further evaluation due to its high bandwidth, low-noise characteristics, RF/IF capability, and availability of a PSpice simulation model.

Final component selection will occur after PSpice model validation and comparison against other candidate TI high-speed amplifiers.

---

## Revision 0.1 – Initial Requirements

**Date:** June 2026  
**Status:** Superseded

### Initial Project Definition

Established the initial requirements for a broadband RF low-noise amplifier intended for RF test equipment, SDR front ends, GPS receivers, and laboratory measurement systems.

### Initial Performance Targets

- 500 MHz–2 GHz operating frequency
- 18–20 dB small-signal gain
- ±1 dB gain flatness
- <1.5 dB noise figure
- 50 Ω input/output impedance
- Better than -10 dB input/output return loss
- 5 VDC operation
- <100 mA supply current
- ≥+18 dBm output P1dB
- Four-layer FR-4 PCB
- Edge-mounted SMA connectors

### Initial Design Tools

- KiCad – schematic capture and PCB layout
- PSpice – circuit simulation
- GitHub – design documentation and revision control

### Superseded By

Revision 0.2 modified the amplifier-selection criteria and several electrical requirements after PSpice model availability was identified as a major project constraint.