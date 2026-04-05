# Enzyme Parameter Calculator - Complete Reference

## Overview

Comprehensive calculator for **all enzyme kinetics parameters** covering:
- Michaelis-Menten kinetics
- Lineweaver-Burk linearization  
- Enzyme inhibition (4 types)
- Enzyme efficiency metrics
- Allosteric kinetics (Hill coefficient)
- Eadie-Hofstee plots
- Temperature effects & activation energy
- Multi-substrate kinetics

---

## Quick Start

### Installation
```bash
# Dependencies already available: scipy is installed via requirements
python enzyme_calculator.py
```

### Basic Usage
```python
from enzyme_calculator import MichaelisMentenCalculator

calc = MichaelisMentenCalculator()

# Calculate velocity
result = calc.velocity_from_km_vmax(vmax=100, km=50, substrate_conc=30)
print(result['velocity'])  # Output: 37.5 µM/s
```

---

## Complete Calculator Reference

### 1. MICHAELIS-MENTEN CALCULATOR

#### `velocity_from_km_vmax(vmax, km, substrate_conc)`
Calculate reaction velocity from kinetic parameters.

**Formula:** `v = (Vmax × [S]) / (Km + [S])`

**Example:**
```python
from enzyme_calculator import MichaelisMentenCalculator
calc = MichaelisMentenCalculator()

result = calc.velocity_from_km_vmax(vmax=100, km=50, substrate_conc=30)
# Returns: velocity=37.5 µM/s, percent_vmax=37.5%
```

#### `substrate_from_velocity(vmax, km, velocity)`
Calculate substrate concentration needed for specific velocity.

**Formula:** `[S] = Km × v / (Vmax - v)`

**Example:**
```python
result = calc.substrate_from_velocity(vmax=100, km=50, velocity=75)
# Returns: substrate_concentration=150 mM
```

#### `km_vmax_from_data(substrate_conc, velocities)`
Estimate Km and Vmax from experimental data using Lineweaver-Burk analysis.

**Example:**
```python
substrates = [10, 20, 50, 100]
velocity_data = [25, 35, 50, 60]

result = calc.km_vmax_from_data(substrates, velocity_data)
# Returns: calculated Km, Vmax, R² value
```

#### `percent_vmax(vmax, velocity)`
Calculate percent of maximum velocity (enzyme saturation).

**Example:**
```python
result = calc.percent_vmax(vmax=100, velocity=50)
# Returns: 50% Vmax (50% saturated with substrate)
```

#### `reaction_time_to_steady_state(km, vmax, enzyme_conc)`
Estimate time to reach steady-state kinetics.

**Example:**
```python
result = calc.reaction_time_to_steady_state(km=50, vmax=100, enzyme_conc=0.001)
```

---

### 2. LINEWEAVER-BURK CALCULATOR

#### `plot_parameters_from_line(slope, intercept)`
Extract Km and Vmax from Lineweaver-Burk plot parameters.

**Formula:**
```
Lineweaver-Burk: 1/v = (Km/Vmax) × (1/[S]) + 1/Vmax
Slope = Km/Vmax
Y-intercept = 1/Vmax
X-intercept = -1/Km
```

**Example:**
```python
from enzyme_calculator import LineweberBurkCalculator
calc = LineweberBurkCalculator()

result = calc.plot_parameters_from_line(slope=0.5, intercept=0.01)
# Returns: Vmax=100 µM/s, Km=50 mM
```

#### `inhibitor_mode_from_lineweaver_burk(slope_no_i, int_no_i, slope_with_i, int_with_i)`
Determine inhibition type from Lineweaver-Burk plots.

**Returns:** Competitive, Non-competitive, Uncompetitive, or Mixed

**Example:**
```python
result = calc.inhibitor_mode_from_lineweaver_burk(
    slope_no_i=0.5, int_no_i=0.01,
    slope_with_i=1.5, int_with_i=0.01  # Slope 3x → Competitive
)
# Returns: inhibition_type="Competitive"
```

---

### 3. INHIBITION CALCULATOR

#### `competitive_inhibition(km, vmax, substrate_conc, inhibitor_conc, ki)`
Calculate enzyme velocity with competitive inhibition.

**Formula:** `Km(app) = Km(1 + [I]/Ki)`

**Characteristics:**
- Apparent Km increases
- Vmax unchanged
- Can be overcome by increasing [S]

**Example:**
```python
from enzyme_calculator import InhibitionCalculator
calc = InhibitionCalculator()

result = calc.competitive_inhibition(
    km=50, vmax=100, substrate_conc=30,
    inhibitor_conc=10, ki=5
)
# Returns: Km_app=150 mM, reduced velocity
```

#### `noncompetitive_inhibition(km, vmax, substrate_conc, inhibitor_conc, ki)`
Calculate enzyme velocity with non-competitive inhibition.

**Formula:** `Vmax(app) = Vmax / (1 + [I]/Ki)`

**Characteristics:**
- Km unchanged
- Apparent Vmax decreases
- Cannot be overcome by increasing [S]

#### `uncompetitive_inhibition(km, vmax, substrate_conc, inhibitor_conc, ki)`
Calculate enzyme velocity with uncompetitive inhibition.

**Characteristics:**
- Both Km and Vmax decreased proportionally
- Km and Vmax decrease by same factor: `1 + [I]/Ki`

#### `mixed_inhibition(km, vmax, substrate_conc, inhibitor_conc, ka, kb)`
Calculate enzyme velocity with mixed inhibition.

**Parameters:**
- `ka`: Dissociation constant for E-I
- `kb`: Dissociation constant for ES-I

#### `ki_from_ic50(ic50, substrate_conc, km, inhibition_type)`
Convert IC50 (inhibitor concentration for 50% activity loss) to Ki.

**Formula (Competitive):** `Ki = IC50 / (1 + [S]/Km)`

**Example:**
```python
result = calc.ki_from_ic50(
    ic50=8.0, substrate_conc=30, km=50,
    inhibition_type="competitive"
)
```

---

### 4. ENZYME EFFICIENCY CALCULATOR

#### `kcat(vmax, enzyme_conc)`
Calculate turnover number (catalytic rate constant).

**Formula:** `kcat = Vmax / [E_total]`

**Returns:** Number of substrate molecules converted per enzyme per second

**Example:**
```python
from enzyme_calculator import EnzymeEfficiencyCalculator
calc = EnzymeEfficiencyCalculator()

result = calc.kcat(vmax=100, enzyme_conc=0.001)
# Returns: kcat=100000 s⁻¹
```

#### `specificity_constant(kcat, km)`
Calculate catalytic efficiency (specificity constant).

**Formula:** `specificity = kcat / Km`

**Units:** M⁻¹·s⁻¹ (or mM⁻¹·s⁻¹ depending on Km units)

**Interpretation:**
- > 10⁶ M⁻¹·s⁻¹: Excellent (limited by diffusion)
- 10⁴-10⁶: Good enzyme
- < 10⁴: Moderate enzyme

**Example:**
```python
result = calc.specificity_constant(kcat=100000, km=50)
# Returns: specificity_constant=2000 M⁻¹·s⁻¹
```

#### `enzyme_efficiency_relative(km, substrate_conc, kcat, specificity_threshold)`
Calculate relative enzyme efficiency and saturation state.

**Returns:** Efficiency grade, saturation level, comparative ratio

---

### 5. ALLOSTERIC KINETICS CALCULATOR

#### `hill_coefficient_from_data(substrate_conc, velocities, vmax)`
Calculate Hill coefficient from velocity data.

**Formula:** `v/Vmax = [S]^n / (K0.5^n + [S]^n)`

**Interpretation:**
- `n > 1`: Positive cooperativity (sigmoidal kinetics)
- `n = 1`: No cooperativity (Michaelis-Menten)
- `n < 1`: Negative cooperativity (rare)

**Example:**
```python
from enzyme_calculator import AllosericKineticsCalculator
calc = AllosericKineticsCalculator()

substrates = [10, 20, 50, 100]
velocities = [10, 22, 55, 85]

result = calc.hill_coefficient_from_data(substrates, velocities, vmax=100)
# Returns: hill_coefficient=1.5 (positive cooperativity)
```

#### `hill_velocity(vmax, substrate_conc, k0_5, hill_coeff)`
Calculate velocity using Hill equation.

**Example:**
```python
result = calc.hill_velocity(vmax=100, substrate_conc=50, k0_5=50, hill_coeff=1.5)
```

---

### 6. EADIE-HOFSTEE CALCULATOR

#### `plot_from_data(substrate_conc, velocities)`
Generate Eadie-Hofstee plot parameters.

**Formula:** `v = -Km(v/[S]) + Vmax`

**Advantages over Lineweaver-Burk:**
- Better weighting (no reciprocals)
- Easier to spot deviations
- More accurate parameter extraction

**Example:**
```python
from enzyme_calculator import EadieHofsteeCalculator
calc = EadieHofsteeCalculator()

result = calc.plot_from_data(
    substrate_conc=[10, 20, 50, 100],
    velocities=[25, 35, 50, 60]
)
# Returns: Km, Vmax, slope, intercept, R²
```

---

### 7. TEMPERATURE EFFECTS CALCULATOR

#### `arrhenius_activation_energy(temp1, temp2, velocity1, velocity2)`
Calculate activation energy from Arrhenius equation.

**Formula:** `ln(v2/v1) = (Ea/R) × (1/T1 - 1/T2)`

**Units:** Temperatures in Kelvin

**Typical Values:**
- Enzyme-catalyzed reactions: 40-80 kJ/mol
- Diffusion-limited: ≈20 kJ/mol
- Complex multistep: >100 kJ/mol

**Example:**
```python
from enzyme_calculator import TemperatureEffectsCalculator
calc = TemperatureEffectsCalculator()

result = calc.arrhenius_activation_energy(
    temp1=298.15,  # 25°C in Kelvin
    temp2=308.15,  # 35°C in Kelvin
    velocity1=50,
    velocity2=150
)
# Returns: Ea ≈ 53 kJ/mol
```

#### `q10_temperature_coefficient(temp1, temp2, velocity1, velocity2)`
Calculate Q10 (temperature coefficient).

**Formula:** `Q10 = (v2/v1)^(10/(T2-T1))`

**Interpretation:**
- Q10 ≈ 2-3: Typical enzymes
- Q10 > 5: High activation energy
- Q10 < 2: Diffusion-limited

**Example:**
```python
result = calc.q10_temperature_coefficient(
    temp1=25, temp2=35,  # Celsius
    velocity1=50, velocity2=150
)
# Returns: Q10 ≈ 3 (rate triples per 10°C)
```

---

### 8. MULTI-SUBSTRATE KINETICS CALCULATOR

#### `sequential_ordered_kinetics(km_a, km_b, vmax, conc_a, conc_b, kia)`
Calculate velocity for ordered sequential mechanism.

**Mechanism:** A must bind before B

**Formula:**
```
v = Vmax × [A][B] / (Km_A × Km_B + Km_A[B] + Km_B[A] + [A][B])
```

**Example:**
```python
from enzyme_calculator import MultiSubstrateCalculator
calc = MultiSubstrateCalculator()

result = calc.sequential_ordered_kinetics(
    km_a=20, km_b=30, vmax=100,
    conc_a=50, conc_b=50
)
```

#### `ping_pong_kinetics(km_a, km_b, vmax, conc_a, conc_b)`
Calculate velocity for Ping-Pong (double displacement) mechanism.

**Mechanism:** No ternary complex; enzyme modified during reaction

---

## Inhibition Type Comparison

| Parameter | Competitive | Non-competitive | Uncompetitive | Mixed |
|-----------|-------------|-----------------|----------|-------|
| **Km** | Increases | Unchanged | Decreases | Increases |
| **Vmax** | Unchanged | Decreases | Decreases | Decreases |
| **Lineweaver-Burk** | Slope↑, Int→ | Slope→, Int↑ | Slope↓, Int↓ | Both change |
| **Can overcome** | Yes (with [S]) | No | No | Partial |
| **Eadie-Hofstee** | Y-intercept→ | Y-intercept↓ | Both↓ | Both change |

---

## Real-World Examples

### Example 1: Drug Development
```python
# Calculate drug potency from IC50 to Ki
ki_result = InhibitionCalculator.ki_from_ic50(
    ic50=50,  # nM
    substrate_conc=100,
    km=250,
    inhibition_type="competitive"
)
print(f"Ki = {ki_result['ki']:.2f} nM")
```

### Example 2: Enzyme Assay Design
```python
# Find optimal substrate concentration
eff = EnzymeEfficiencyCalculator()
spec = eff.specificity_constant(kcat=100000, km=50)
# Use [S] = Km for 50% Vmax (most sensitive to changes)
```

### Example 3: Clinical Diagnosis
```python
# Calculate enzyme activity from temperature
ea_result = TemperatureEffectsCalculator.arrhenius_activation_energy(
    temp1=310.15,  # Body temperature
    temp2=298.15,  # Room temperature
    velocity1=activity_at_37,
    velocity2=activity_at_25
)
```

### Example 4: Enzyme Engineering
```python
# Compare enzyme efficiencies
enzymes = [
    {"name": "Wild-type", "kcat": 100, "km": 50},
    {"name": "Mutant 1", "kcat": 500, "km": 50},
    {"name": "Mutant 2", "kcat": 100, "km": 10},
]

for enzyme in enzymes:
    spec = EnzymeEfficiencyCalculator.specificity_constant(
        kcat=enzyme["kcat"], km=enzyme["km"]
    )
    print(f"{enzyme['name']}: {spec['specificity_constant']:.0e} M⁻¹·s⁻¹")
```

---

## Complete List of All Methods

### MichaelisMentenCalculator
1. `velocity_from_km_vmax()`
2. `substrate_from_velocity()`
3. `km_vmax_from_data()`
4. `percent_vmax()`
5. `reaction_time_to_steady_state()`

### LineweberBurkCalculator
1. `plot_parameters_from_line()`
2. `inhibitor_mode_from_lineweaver_burk()`

### InhibitionCalculator
1. `competitive_inhibition()`
2. `noncompetitive_inhibition()`
3. `uncompetitive_inhibition()`
4. `mixed_inhibition()`
5. `ki_from_ic50()`

### EnzymeEfficiencyCalculator
1. `kcat()`
2. `specificity_constant()`
3. `enzyme_efficiency_relative()`

### AllosericKineticsCalculator
1. `hill_coefficient_from_data()`
2. `hill_velocity()`

### EadieHofsteeCalculator
1. `plot_from_data()`

### TemperatureEffectsCalculator
1. `arrhenius_activation_energy()`
2. `q10_temperature_coefficient()`

### MultiSubstrateCalculator
1. `sequential_ordered_kinetics()`
2. `ping_pong_kinetics()`

---

## Running Examples

```bash
# Run all demonstrations
python enzyme_calculator_examples.py

# Shows:
# 1. Michaelis-Menten calculations
# 2. Lineweaver-Burk analysis
# 3. Inhibition types (4 types)
# 4. Efficiency metrics
# 5. Allosteric kinetics
# 6. Eadie-Hofstee plots
# 7. Temperature effects
# 8. Multi-substrate kinetics
# 9. Real-world scenarios
```

---

## Units & Constants

### Common Units
- **Velocity:** µM/s, nM/s, µmol/(min·mL)
- **Concentration:** mM, µM, nM
- **Km/Kd:** Same units as [S]
- **kcat:** s⁻¹ (reactions per second)
- **kcat/Km:** M⁻¹·s⁻¹

### Constants
- **R (Gas constant):** 8.314 J/(mol·K)
- **T (Standard):** 298.15 K (25°C)
- **ATP hydrolysis:** ΔG = -30.5 kJ/mol

---

## Integration with Existing Code

```python
from enzyme_calculator import *
from ligand_protein_interaction import find_ligand_and_protein_atoms

# Analyze protein-ligand binding with enzyme kinetics
pdb_data = find_ligand_and_protein_atoms(structure, "LIG")
distances = calculate_distances(pdb_data)

# Estimate Kd from distances
kd = estimate_kd_from_distances(distances)

# Calculate inhibition parameters
result = InhibitionCalculator.competitive_inhibition(
    km=50, vmax=100, substrate_conc=30,
    inhibitor_conc=kd, ki=kd
)
```

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Velocity must be < Vmax" | Calculated velocity ≥ Vmax | Check input values |
| "Ki must be positive" | Negative or zero Ki | Verify inhibitor concentration |
| "Need at least 3 data points" | Insufficient experimental data | Add more data points |
| "Arrays must have same length" | Mismatched arrays | Check substrate_conc and velocities |

---

## References

- Michaelis, L., & Menten, M. L. (1913). "Die Kinetik der Invertinwirkung"
- Lineweaver, H., & Burk, D. (1934). "The Determination of Enzyme Dissociation Constants"
- Cornish-Bowden, A. (2012). "Fundamentals of Enzyme Kinetics" (4th ed.)
- Berg, Tymoczko, Stryer. "Biochemistry" (8th ed.)

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Status:** ✅ Complete & Production Ready  
