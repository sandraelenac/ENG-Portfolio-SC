# Amplifiers Study 

| Amplifier | Type | RF Capability | PSpice | Status | Reason |
|---|---|---|---|---|---|
| INA630 | Instrumentation Amplifier | Insufficient | Yes | $\color{red}{\text{Rejected}}$ | Bandwidth too low |
| INA823 | Instrumentation Amplifier | Insufficient | Yes | $\color{red}{\text{Rejected}}$ | Bandwidth too low |
| INA848 | Instrumentation Amplifier | Insufficient | Yes | $\color{red}{\text{Rejected}}$ | Wrong architecture |
| INA851 | Instrumentation Amplifier | Insufficient | Yes | $\color{red}{\text{Rejected}}$ | Bandwidth too low |
| ADL5521 | RF LNA | Excellent | No TI PSpice workflow | $\color{red}{\text{Rejected}}$ | Does not satisfy simulation requirement |
| ADL5523 | RF LNA | Excellent | No TI PSpice workflow | $\color{red}{\text{Rejected}}$ | Does not satisfy simulation requirement |
| TQP3M9036 | RF LNA | Excellent | No TI PSpice workflow | $\color{red}{\text{Rejected}}$ | Does not satisfy simulation requirement |
| OPA858 | High-Speed Amplifier | Candidate | Yes | Under Review | Requires architecture evaluation |
| LMH6401 | RF VGA | Candidate | Yes | Under Review | Added complexity from VGA architecture |
| LMH5401 | High-Speed FDA | Excellent | Yes | Leading Candidate | Strong combination of RF capability and simulation support |