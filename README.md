# Sandra Castrejon — Engineering Portfolio
Electrical & Computer Engineer

RF • Flight Test • Radar • PCB Design • Python • SQL • AI • Data Engineering

---

Welcome to my engineering portfolio.

This repository showcases personal, academic, and professional-inspired engineering projects spanning RF hardware design, flight-test systems, PCB development, Python automation, database engineering, and applied machine learning.

Every project emphasizes structured engineering processes, technical documentation, reproducibility, and measurable performance.
This repository contains selected engineering projects demonstrating practical experience with:
---

## Featured Projects

| Project | Engineering Focus | Technologies | Status |
|---|---|---|---|
| [Low Noise Amplifier](./Low%20Noise%20Amplifier%20%28LNA%29) | RF amplifier design from electrical requirements through simulation and PCB development | KiCad, PSpice, RF Design | In Progress |
| [RX Test Acquisition Unit](./RX%20Test%20ACQ%20Unit) | High-speed optical receiver front end, PCB design, simulation, and manufacturing documentation | KiCad, OrCAD, PSpice | Completed Design |
| [Banking Database](./SQL/BankingDB) | Relational schema design, synthetic data generation, ETL, SQL optimization, and scalability testing | Python, SQL, SQLite | Completed |
| [Aviation Anomaly Analysis](./MARL%for%ATC%Managenent) | Aviation-focused data analysis and anomaly-modeling coursework | Python, Data Analytics | Completed |

---

## Engineering Portfolio Areas

### RF and Electronics

- RF and analog circuit requirements development
- 50-ohm impedance-controlled design
- Low-noise amplifier design
- Transimpedance amplifier signal chains
- High-speed differential interfaces
- Component selection and circuit simulation
- Schematic capture and PCB layout
- Gerber, drill, and pick-and-place generation
- Hardware revision and configuration management

### Software and Data

- Python scripting and automation
- SQL schema design and query development
- SQLite database implementation
- Synthetic data generation
- Extract, transform, and load workflows
- Query benchmarking and optimization
- Data validation and engineering analysis
- Reproducible command-line workflows
- Git and GitHub version control

### Test and Systems Engineering

- Requirements verification
- Ground and flight-test planning
- Test execution and coordination
- Engineering data validation
- Technical report development
- Risk identification and resolution
- Cross-functional team leadership
- Integration of developmental and operational testing

---

# Projects

## 1. Low Noise Amplifier

[View the LNA project](./Low%20Noise%20Amplifier%20%28LNA%29)

The Low Noise Amplifier project is an RF hardware-development effort focused on designing a 50-ohm amplifier for operation from 500 MHz to 2 GHz.

The project is intended to demonstrate the complete design process:

1. Define electrical and mechanical requirements.
2. Select an RF amplifier architecture and components.
3. Develop and simulate the circuit in PSpice.
4. Create the schematic and PCB layout in KiCad.
5. Generate manufacturing and assembly documentation.
6. Evaluate the design against its original requirements.

### Key Electrical Requirements

| Parameter | Requirement |
|---|---:|
| Frequency range | 500 MHz–2 GHz |
| Small-signal gain | 18–20 dB |
| Gain flatness | ±1 dB |
| Noise figure | Less than 1.5 dB |
| Input return loss | Better than −10 dB |
| Output return loss | Better than −10 dB |
| Input impedance | 50 Ω |
| Output impedance | 50 Ω |
| Supply voltage | 5 VDC |
| Supply current | Less than 100 mA |

### Planned Deliverables

- System block diagram
- Component-selection analysis
- PSpice simulation
- KiCad schematic
- PCB stack-up and layout
- RF grounding and routing review
- Bill of materials
- Manufacturing outputs
- Design verification summary

---

## 2. RX Test Acquisition Unit

[View the RX Test Acquisition Unit project](./RX%20Test%20ACQ%20Unit)

The Test Acquisition Unit is a high-speed optical receiver board that converts low-level photodiode current into a differential electrical signal suitable for FPGA-based bit-error-rate testing.

The signal chain includes:

```text
Optical Input
     │
     ▼
Photodiode
     │
     ▼
LMH6629 Transimpedance Amplifier
     │
     ▼
MAX3747 Limiting Amplifier
     │
     ▼
Differential Output
     │
     ▼
FPGA / BER Test Equipment
```

### Hardware Features

- High-speed analog signal path
- Photodiode input interface
- LMH6629 transimpedance amplifier
- MAX3747 limiting amplifier
- Differential output interface
- Adjustable voltage regulation
- Debugging and measurement test points
- Two-layer PCB implementation
- Multiple hardware revisions
- Manufacturing-ready fabrication files

### PCB Layout

<p align="center">
  <img src="./RX%20Test%20ACQ%20Unit/images/RevG_PCB.png" alt="TAU Revision G PCB layout" width="800">
</p>

### Receiver Architecture

<p align="center">
  <img src="./RX%20Test%20ACQ%20Unit/images/Overview_of_Recevier_Circuit.png" alt="Test Acquisition Unit receiver architecture" width="800">
</p>

### Design Files

The project includes:

- KiCad schematics
- KiCad PCB layouts
- Revision F and Revision G designs
- Cadence OrCAD and PSpice files
- Gerber fabrication outputs
- NC drill files
- Pick-and-place files
- Simulation files
- Design images and documentation

---

## 3. Banking Database

[View the Banking Database project](./SQL/BankingDB)

The Banking Database project demonstrates the design, population, validation, optimization, and benchmarking of a relational database using Python, SQL, and SQLite.

The project models realistic banking entities such as:

- Customers
- Accounts
- Transactions
- Branches
- Loans
- Cards
- Merchants

### Database Architecture

<p align="center">
  <img src="./SQL/BankingDB/docs/imgs/BankingSchmea-V2.png" alt="Banking database schema" width="850">
</p>

### Processing Workflow

<p align="center">
  <img src="./SQL/BankingDB/docs/imgs/BankingDB_flowchart.png" alt="Banking database workflow" width="850">
</p>

### Project Workflow

```text
Synthetic Data Generation
          │
          ▼
CSV Data Files
          │
          ▼
SQL Schema Creation
          │
          ▼
Python ETL and Validation
          │
          ▼
SQLite Banking Database
          │
          ▼
Baseline SQL Workload
          │
          ▼
Index Optimization
          │
          ▼
Performance Benchmarking
          │
          ▼
Scalability Analysis
```

### Technical Features

- Normalized relational database schema
- Primary and foreign key enforcement
- `CHECK` and `UNIQUE` constraints
- Synthetic banking-data generation
- Automated SQLite database creation
- Python-based ETL pipeline
- Twenty-query analytical workload
- Baseline and optimized performance testing
- Index design and performance evaluation
- Automated result export
- Dataset scaling up to one million transactions

### Query Categories

| Category | Analysis |
|---|---|
| Customer analysis | Customer lookups and account relationships |
| Transaction analysis | Account activity, spending, inflows, and merchant volume |
| Branch analysis | Daily volume, cash flow, and transaction summaries |
| Loan analysis | Outstanding principal, APR, and portfolio distribution |
| Card analysis | Card-network and lifecycle-status summaries |
| Performance analysis | Baseline versus indexed query execution |

### Primary Technologies

- Python
- SQL
- SQLite
- pandas
- NumPy
- Command-line automation
- Database indexing
- Performance benchmarking

---

## 4. Aviation Anomaly Analysis

[View the Aviation Anomaly project](./ECE508-ABM-AviationAnomaly)

This project contains aviation-focused anomaly-analysis and modeling work developed for ECE 508.

The project expands this portfolio into:

- Aviation data analysis
- Anomaly identification
- Python-based analytical workflows
- Model development and evaluation
- Engineering interpretation of data

Additional documentation, methodology, and results will be added as the project develops.

---

# Technical Skills

## Hardware and RF

![KiCad](https://img.shields.io/badge/KiCad-314CB0?style=flat-square&logo=kicad&logoColor=white)
![PSpice](https://img.shields.io/badge/PSpice-Cadence-red?style=flat-square)
![PCB Design](https://img.shields.io/badge/PCB-Design-green?style=flat-square)
![RF Design](https://img.shields.io/badge/RF-Circuit%20Design-blue?style=flat-square)

- KiCad
- Cadence OrCAD Capture
- Cadence PSpice
- Schematic capture
- PCB layout
- Analog circuit design
- RF circuit design
- Signal-chain analysis
- Gerber and manufacturing-output generation

## Programming and Data

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)

- Python
- SQL
- SQLite
- pandas
- NumPy
- Data processing
- Database design
- ETL development
- Query optimization
- Performance benchmarking
- Git and GitHub

## Engineering

- Requirements development
- Requirements verification
- Test planning and execution
- Engineering data validation
- Root-cause analysis
- Technical reporting
- Configuration management
- Cross-functional leadership
- Systems integration

---

# Software Requirements

Different projects require different engineering environments.

| Project | Recommended Software |
|---|---|
| Low Noise Amplifier | KiCad 8 or later, Cadence PSpice |
| RX Test Acquisition Unit | KiCad 7 or later, Cadence OrCAD/PSpice |
| Banking Database | Python 3.8 or later, SQLite 3 |
| Aviation Anomaly Analysis | Python and project-specific dependencies |

Individual project directories contain more detailed setup and execution instructions.

---


# Portfolio Purpose

This repository is intended to demonstrate the ability to take engineering work from an initial problem statement through implementation and documentation.

The projects emphasize:

- Clear and measurable requirements
- Structured engineering processes
- Traceable design decisions
- Reproducible technical workflows
- Verification through analysis, simulation, or testing
- Professional documentation
- Continuous design improvement

