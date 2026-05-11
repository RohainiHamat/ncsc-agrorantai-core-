# NCSC AgroRantai Core

**Governance‑First AI for National Food Supply Chain**

Visi: Membina framework AI yang **boleh diaudit, beretika, dan tahan terhadap kegagalan sistemik** dalam rantaian bekalan makanan nasional.  
Tidak bermula dengan model besar — bermula dengan **peraturan, akauntabiliti, dan arkitektur veto teragih**.

> “Bukan sekadar AI yang pintar, tetapi AI yang tahu batas moralnya.”

---

## Masalah Nasional
- Ketelusan data rantaian sejuk masih rendah.
- Tiada mekanisme *real‑time* untuk mengesan residu berbahaya atau keputusan ekonomi yang merbahaya.
- AI sedia ada bersifat “kotak hitam” – sukar dipersalahkan, sukar dihentikan.

## Seni Bina 7 Lapisan NCSC

```mermaid
flowchart TD
    L1[Sensor & IoT Layer]
    L2[Data Aggregation Layer]
    L3[Feature Extraction Layer]
    L4[Residue Intelligence Firewall RIF]
    L5[Moral Boundary Ruleset MBR]
    L6[Distributed Veto & Circuit Breaker]
    L7[Audit & System Diary]

    L1 --> L2 --> L3 --> L4
    L4 --> L5
    L5 --> L6
    L6 --> L7
    L5 -.->|Classification A/B/C| L7flowchart LR
    Input[Keputusan Input] --> FE[Feature Extraction]
    FE --> MBR[Moral Boundary Ruleset]
    MBR --> Class{Kelas?}
    Class -->|A: Selamat| Execute[Laksana]
    Class -->|B: Persempadanan| Review[Semakan Manual + Veto]
    Class -->|C: Langgar| Block[Sekat + Log + Buzzer]
    Execute --> Audit[Audit Logging]
    Review --> Audit
    Block --> Audit
