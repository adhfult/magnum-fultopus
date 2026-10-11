# Project Charter: Heat, Bytes, Stars and Signals

*A four-pillar computational research program. Written 11 October 2026 as the
founding document for a new project that starts from scratch. "The Study of
Important Things" is prior work: read for context, never imported or extended.
Paste this whole file into the new project's knowledge/instructions, and copy
Part 12 into its `CLAUDE.md`.*

---

## Contents

0. How to use this file
1. The mission, in one argument
2. The hardware you actually have
3. Working rules (non-negotiable)
4. Prior work: context, not code
5. Pillar I: Thermodynamics and microchip engineering
6. Pillar II: AI hardware and small-memory models
7. Pillar III: Computational astrophysics and instrumentation
8. Pillar IV: Quantum and quantitative trading research
9. The shared core: math library, bench, telemetry, journal
10. Repository layout
11. The first twelve weeks
12. `CLAUDE.md` template for the new project
13. Reading list (primary sources)
14. Turning this into a future: outputs that count
15. Open questions to settle in week one

---

## 0. How to use this file

This is a charter, not a schedule. It says *what* the project is, *why* the four
pillars belong together, *how* work is done, and *what order* to do it in. The
dated week-by-week plan in Part 11 is the only part that should be rewritten as
time passes; everything else should change only when a real measurement
changes your mind.

Three uses:

- **As project knowledge** for Claude (chat, Cowork, Claude Code). It replaces
  re-explaining the project every session.
- **As your own map.** Each pillar has a ladder of levels (L0 → L4). You always
  know which rung you're on and what "done" means for it.
- **As the seed of a portfolio.** Part 14 is about turning measured results into
  things other people can see.

Every factual claim about outside hardware, papers or markets in this file is
either (a) something already measured in the old project, marked **[measured]**,
(b) a standard textbook result, or (c) marked **[verify]** to be checked against
a primary source before you build on it. The old project's Gemini transcripts
invented hardware specs three separate times. This project doesn't repeat that.

---

## 1. The mission, in one argument

The four pillars look like four hobbies. They're one argument approached from
four directions:

> **Computation is limited by moving bytes and removing heat. The mathematics
> that describes those limits (linear algebra, partial differential equations,
> stochastic processes) is the same mathematics that finds planets in noisy
> light curves and structure in noisy markets.**

Spelled out:

- **Pillar I (heat).** Every joule a chip uses becomes heat that has to leave
  through a chain of thermal resistances. Power density, not transistor count,
  is now the binding constraint on chips. The heat equation is the governing law.
- **Pillar II (bytes).** Generating text with a language model is mostly waiting
  for weights to arrive from memory. Tokens per second is bounded by memory
  bandwidth; tokens per joule is bounded by Pillar I. Making models run in
  8/16/32 GB is a problem of bytes per parameter, bytes per token of context,
  and how often each byte is read.
- **Pillar III (stars).** Finding a planet is pulling a 0.01% periodic signal out
  of correlated noise. Simulating a cluster is an O(N²) problem made tractable
  by approximation, which is the same move as attention approximations in
  Pillar II. Gravitational-wave detection is matched filtering, the same
  operation as convolution.
- **Pillar IV (signals).** A market is a high-dimensional, non-stationary noisy
  system. Factor models are SVD. Regime detection is a hidden Markov model.
  Portfolio selection is a combinatorial optimization problem, which is where
  the quantum part enters: QUBO formulations, QAOA and annealing.

**Shared tools:** SVD/PCA, Fourier transforms, ODE/PDE integrators,
optimization, Monte Carlo, and honest benchmarking. One math library feeds all
four pillars (Part 9). The old project already proved this once: one SVD module
found a planet in Kepler data *and* a market factor **[measured, 31 Aug 2026]**.

**What the project is for, in order:**

1. Real skill that compounds: physics, numerical methods, systems, ML internals.
2. Measured, published results with your name on them (Part 14).
3. A clear story for applications, competitions and mentors:
   *"I study the physical limits of computation, and I measure them on my own
   hardware."*
4. Optional, eventual income from the tooling. Explicitly not a goal before 2027.

---

## 2. The hardware you actually have

From the old project's machine audit (5 Sep 2026) and later checks. **[measured]**
unless marked otherwise. Confirm anything that changes with your own eyes, not
from old documents.

| Machine | Role | Specs | What it can do | What it can't |
|---|---|---|---|---|
| **PC** (`GAMER15`, "sim-server") | Simulation + local inference | Ryzen 5 7600X 6C/12T, ~31 GB RAM, **RX 570 8 GB** (7.75 GB usable per Vulkan heap table), Win 11 + WSL2 | llama.cpp via **Vulkan**, CPU numerics (NumPy/Julia), OpenFOAM/LAMMPS in WSL2, GPU power/temperature via LibreHardwareMonitor | **No CUDA, no supported ROCm** (Polaris/gfx803 was dropped). No PyTorch GPU, no bitsandbytes, no AWQ/GPTQ kernels |
| **Laptop** | Command deck | i5-1135G7, 32 GB RAM, Iris Xe | Editing, light CPU numerics, CPU temperature via LHM | Any heavy compute |
| **Raspberry Pi 400** | Edge node + station | Cortex-A72 4C @ 1.8 GHz, 4 GB, 256 GB card | Edge inference datapoint, real CPU temperature sensor, always-on jobs, camera/SDR experiments | Anything heavy |
| **Colab / Kaggle free GPU** | Borrowed CUDA | T4 16 GB (Colab) | Fine-tuning, training small models, AWQ/GPTQ quantization | Long jobs, guaranteed sessions |

**Three facts that shape every plan:**

1. **The RX 570 is an inference card, not a training card.** It runs quantized
   models through Vulkan and that's it. Training and CUDA-only quantization go
   to Colab/Kaggle. This is a feature for Pillar II: an old, limited card with
   real telemetry is exactly the "weak hardware" the pillar is about.
2. **Only one GPU can be measured directly.** Every other chip in Pillars I and
   II is a *prediction* from a model that has to be checked against the RX 570
   (and the Pi, as a second point) first.
3. **You'll build a telemetry pipeline** (power, temperature, utilization →
   a local cache) as one of the first pieces of this project. The old project
   proved it's possible on these machines, including GPU power through
   LibreHardwareMonitor on Windows. Almost no hobby benchmark has energy
   numbers. Once it runs, keep it running; unbroken history is an asset.

**Worth getting eventually (not required):** a wall-plug power meter (an honest
fallback if the GPU power sensor won't read), a Pi camera module (astrophotography),
an RTL-SDR dongle (radio astronomy), and a cheap thermocouple + reader for
physical heat experiments. Prices change; check before buying **[verify]**.

---

## 3. Working rules (non-negotiable)

Learned in the old project because they worked, sharpened where they didn't.

1. **You write the core logic by hand.** Solvers, attention, model architecture,
   prediction models, trading strategy and signal logic. Claude writes
   harnesses, plumbing, plotting, tests, data pulls and reviews. If you can't
   derive it on paper, you don't understand it yet, and the paper notebook is
   the proof.
2. **A run you didn't log didn't happen.** Every experiment records:
   hyperparameters, inputs, results, wall time, hardware, software versions
   (commit hashes, driver versions). Numbers, not adjectives. "1.4e-14", not "small".
3. **Verify before asserting.** Anything from a connector, a paper summary, a
   spec sheet or an AI transcript is a claim until it's run or cross-checked.
   Cite source + retrieval date. Cache every pull to disk so results reproduce
   offline.
4. **Measure before you optimize.** Profile, change one thing, measure again,
   log before/after. An optimization with no before/after number didn't happen.
5. **Baselines are mandatory.** RL controller → beat a tuned PID. New model →
   beat the same-size off-the-shelf model. Trading strategy → beat buy-and-hold
   SPY *after costs*. Quantum algorithm → beat classical simulated annealing on
   the same problem. If you lose, publish that. An honest loss is a stronger
   signal than an unbenchmarked win; the old project already proved this twice
   (Verlet beat RK45; nothing beat SPY after costs).
6. **Label every command by machine.** PC, Pi, laptop, or Colab.
7. **Trading is paper and backtest only.** No live orders, no brokerage account
   linking for order placement, no automated execution against real money.
   Read-only data is fine.
8. **No secrets in chat or in git.** Connectors authenticate through the account.
   `.env` files are gitignored. If a key gets pasted, rotate it.
9. **Running code beats more documents.** Don't write a plan when a two-minute
   command answers the question. This charter is the last big document; after
   it, write results.
10. **Record the wrong turns.** The journal keeps every dead end with its reason.

---

## 4. Prior work: context, not code

**This project starts from scratch.** Nothing from
`The Study of Important Things/research-lab/` is copied, imported or extended.
Every module here is written fresh, to this charter's standards, with its own
tests.

The old project is still useful in three ways, and only these three:

1. **Lessons.** What worked, what didn't, and why (below).
2. **Measured facts** about your own hardware, which don't change because the
   code is new (Part 2).
3. **A reference to check against *after* you've built something yourself.**
   When your new BLS or 2D solver is done, comparing its output against the old
   one is a valid test. Opening the old code *before* writing yours defeats the
   purpose of starting over.

Treat the old repo as **read-only and archived**. The Pi stock station can keep
running there; it isn't part of this project.

### What the old project established (findings, not code)

| Area | Finding | How sure |
|---|---|---|
| Hardware | RX 570 exposes 7.75 GB device-local VRAM via Vulkan, not the "~4 GB Polaris ceiling" the transcripts claimed. No CUDA, no supported ROCm | **[measured]** |
| Hardware | GPU and laptop CPU temperatures are readable on Windows only through LibreHardwareMonitor; `psutil` has no Windows sensor backend | **[measured]** |
| Thermal | Explicit 2D FDM converges at 2nd order when the CFL condition is respected; violating it blows up exactly as theory predicts | **[measured]** |
| Astro | Verlet (symplectic) conserves energy better than RK45 over long orbits: "higher order" isn't "better" for Hamiltonian systems | **[measured]** |
| Astro / Quant | One SVD routine both cleaned Kepler pixel systematics and extracted a market factor; the cross-domain thesis holds | **[measured]** |
| AI | QLoRA on 200 examples transferred writing *style*, not *facts*, and produced confident fabrication. Retrieval fixed the specific failures | **[measured]** |
| AI | TF-IDF retrieval scored 73% top-1 / 87% top-3 on paraphrases and failed when wording shared no vocabulary | **[measured]** |
| AI | AWQ/GPTQ/bitsandbytes need CUDA, so on this hardware they only run on Colab/Kaggle | **[measured]** |
| Quant | The EMA-cross family did not beat buy-and-hold SPY once costs reached ~5 bps | **[measured]** |
| Process | The bottleneck was never code; it was registering, emailing and publishing | Observed |
| Process | The Gemini transcripts invented hardware specs three times; AI-written claims need checking | Observed |
| Process | Plans multiplied faster than results: 5 plan revisions, 0 videos. Fewer documents, more runs | Observed |

### What to do differently this time

- **Design the shared core first** (Part 9) instead of discovering it halfway.
- **One provenance schema from day one**, so every result can be joined with
  telemetry without retrofitting.
- **Write the derivation in the paper notebook before the code**, every time.
- **Fewer, deeper threads.** Four pillars, one lead per fortnight (Part 11).
- **Publish early.** The first public post is due in the first quarter, not "when ready."

---

## 5. Pillar I: Thermodynamics and microchip engineering

### 5.1 The question

*How much heat can be removed from a chip, where is the bottleneck in the path
from transistor to air, and what does it cost in performance when you can't
remove it?*

### 5.2 Foundations you need (and the one equation for each)

| Concept | Core relation | Why it matters |
|---|---|---|
| Conduction (Fourier) | q″ = −k ∇T | Heat through die, TIM, spreader |
| Heat equation | ∂T/∂t = α ∇²T + q̇/(ρc) | Everything transient: hotspots, throttling |
| Thermal resistance | R = L/(kA) for a slab; ΔT = P · ΣR | The chain model that explains most cooling |
| Convection | q = hA(T_s − T_∞) | Heatsink to air or coolant |
| Lumped capacitance | C dT/dt = P − (T − T_amb)/R | Fitting real telemetry; valid when Biot number Bi = hL/k ≪ 1 |
| Dynamic CMOS power | P ≈ α C V² f | Why lowering voltage beats lowering frequency |
| Leakage power | grows roughly exponentially with temperature | Thermal runaway: hotter → leakier → hotter |
| Interface (Kapitza) resistance | R_K = ΔT / q″ at a boundary | Phonon mismatch between materials; the TIM problem |
| Phonon transport | k = ⅓ C v ℓ (kinetic theory) | Why diamond/graphene conduct well and why interfaces scatter |

**Typical convection coefficients** (textbook ranges, W/m²·K): natural
convection in air ~2–25; forced air ~25–250; forced liquid ~100–20,000;
boiling/condensation ~2,500–100,000. These ranges are why each step up in power
density forces a change of cooling technology.

### 5.3 The thermal-resistance chain, made concrete

```
T_junction = T_ambient + P × (R_die + R_TIM1 + R_spreader + R_TIM2 + R_sink + R_convection)
```

- For an air-cooled GPU, the heatsink-to-air term usually dominates.
- When cooling moves to direct-to-chip liquid, the convective term shrinks
  dramatically, so **the TIM layers become a large share of the total.** That
  is the whole reason interface materials matter, and it's where your Avenue 1
  research (carbon allotropes, Kapitza resistance, acoustic bridging) plugs in.
- **Heat flux**, not total watts, decides the cooling technology: W/cm² of die.
  Compute it for every chip you study. **[verify each chip's die area and power
  from vendor documents]**

### 5.4 The ladder

**L0: Analytical.** 1D steady and transient conduction, composite walls,
fins, the semi-infinite solid. Derive each on paper, implement, test against
hand-computed values. These become the reference answers every later solver is
checked against.

**L1: Numerical 2D.**
- Explicit 2D finite differences with a CFL stability check; prove 2nd-order
  convergence with a refinement study (error ratio ≈ 4 per halving of h).
- Then: (a) **contact-resistance boundary** between two material regions
  (a jump condition, ΔT = R_K · q″); (b) **anisotropic conductivity**
  (kₓ ≠ k_y), the graphene in-plane vs. through-plane problem;
  (c) **implicit time stepping** (Crank–Nicolson + sparse solve) so stiff
  multi-material stacks don't need tiny time steps.
- Deliverable: die → TIM → spreader → cold plate cross-section, with a sweep of
  TIM conductivity and thickness, verified against the analytical series-resistance answer.

**L2: Fit reality.**
- Fit a lumped RC (and then a 2–3 node RC network) model to the RX 570's real
  telemetry: power steps in, temperature out. Extract R and τ = RC.
- Check prediction: fit on one load run, predict another.
- Repeat on the Pi 400 (real sensor, very different thermal mass).
- This is also the system-identification step for the thermal controller in L4.
- Deliverable: "RX 570 thermal model: R = __ K/W, τ = __ s, prediction error __ °C."

**L3: Compact chip models and other chips.**
- Build a **floorplan-based compact thermal model**: split a die into blocks
  (cores, cache, memory controller), each a node with power, connected by
  lateral and vertical resistances. This is the approach of the academic
  HotSpot tool **[verify: HotSpot, University of Virginia]**. Run it with HotSpot
  as a check *after* writing your own.
- Apply it to 3–5 chips from public data: consumer GPU, data-center accelerator,
  phone SoC, the Pi's SoC. Compare hotspots, heat flux, and required h.
- **Chiplets and 3D stacking:** model a stacked-memory-on-logic case and show why
  the bottom die's heat has to pass through everything above it.
- **DVFS and throttling:** couple the power model (P ∝ V²f, plus leakage(T)) to
  the thermal model and simulate a chip that throttles. Find the sustained
  frequency each cooling solution supports.
- Deliverable: a table and plot of chip × cooling method → max sustained power,
  hotspot temperature and throttling point.

**L4: Atomistic and fluid (long horizon).**
- **Interface materials:** acoustic impedance screening (an afternoon in
  Python), then acoustic/diffuse mismatch models (AMM/DMM) for R_K, then
  non-equilibrium molecular dynamics in **LAMMPS** for a Si/interlayer/carbon
  interface. Compare your R_K values against literature **[verify]**.
- **Cold-plate CFD:** OpenFOAM conjugate heat transfer through a microchannel
  cold plate; pressure drop vs. thermal resistance trade-off.
- **Two-phase and immersion cooling:** read and model at the lumped level first;
  full two-phase CFD is graduate-level and can wait.
- **Thermal control:** fan/governor control on the Pi, a tuned PID baseline,
  then an RL controller trained in simulation on the L2 model. Publish the
  comparison honestly, whichever wins.

### 5.5 Optimization in this pillar

- **Solver performance:** profile the Julia solver (`BenchmarkTools`,
  allocations, loop order, threading). Report cells/second before and after.
- **Design optimization:** given a power map and a cooling budget, choose TIM
  thickness, spreader size and fin geometry to minimize T_junction. Start with a
  grid search, then gradient-free methods (Nelder–Mead, Bayesian optimization).
- **Workload-aware cooling:** schedule load to avoid hotspots; this links to
  Pillar II's energy measurements.

### 5.6 Done-when bar for the pillar's first year

A written, reproducible study: *"Where the heat gets stuck: a measured RX 570
model, a compact model applied to five chips, and how much better interface
materials would actually help,"* with code, data and plots public.

---

## 6. Pillar II: AI hardware and small-memory models

### 6.1 The question

*How fast and how well can a language model run in 8, 16 or 32 GB, on weak
hardware, per joule, and what can you change (format, architecture, decoding,
training) to move that frontier?*

### 6.2 The four budgets (memorize these)

**1. Weight memory.**
```
weight bytes ≈ parameters × bits per weight / 8
```
1B parameters at 16-bit = 2 GB; at 8-bit ≈ 1 GB; at ~4.8 bits (a typical
"Q4_K_M"-class GGUF average) ≈ 0.6 GB **[verify exact bits/weight per format]**.

**2. KV-cache memory** (grows with context):
```
KV bytes per token = 2 (K and V) × layers × kv_heads × head_dim × bytes per element
```
Worked example: a 7B-class model with 32 layers, 32 KV heads, head dim 128, fp16
→ 2 × 32 × 32 × 128 × 2 B = 524,288 B ≈ **0.5 MB per token**, so 4,096 tokens of
context ≈ **2 GB**. Grouped-query attention (fewer KV heads) and KV quantization
exist because of this number.

**3. Speed (decode).** Each generated token reads every weight once:
```
max tokens/sec ≈ memory bandwidth / weight bytes
```
RX 570: 224 GB/s ÷ ~1 GB (1.5B model at 4-bit) ≈ 220 tok/s ceiling. The measured
fraction of that ceiling is your efficiency factor. **Prefill** (reading the
prompt) is compute-bound and uses a FLOPs bound instead. Plot both and you have
your roofline.

**4. Energy.**
```
joules per token ≈ average power (W) / tokens per second
```
Measured from telemetry. This is the number that connects to Pillar I.

### 6.3 What fits where (approximate, before KV cache and OS overhead)

| Memory | Comfortable at ~4-bit | At 8-bit | Notes |
|---|---|---|---|
| **8 GB** | ~7–8B dense, short context | ~3–4B | Your RX 570 tier. Context is the squeeze |
| **16 GB** | ~13–14B dense | ~7–8B | Mixture-of-experts models become interesting |
| **32 GB** | ~30B dense | ~14B | Your PC's system RAM: CPU inference, much slower (bandwidth) |

The 32 GB row is the trap: it *fits*, but CPU memory bandwidth is several times
lower than VRAM bandwidth, so it's slow. **Measure your PC's actual RAM
bandwidth** (a STREAM-style benchmark) and add it to the table.

### 6.4 The levers for making weak hardware run models better

Grouped by what they attack:

**Fewer bytes per weight**
- Post-training quantization: GGUF k-quants, importance-matrix quants (imatrix),
  GPTQ, AWQ (the last two need CUDA, so Colab).
- Extreme low-bit: 2-bit, ternary ("1.58-bit") models trained that way from the
  start **[verify: BitNet b1.58 paper]**. Key point: they're *trained* low-bit,
  not compressed after.
- Pruning and sparsity (structured pruning actually saves memory; unstructured
  often doesn't on consumer hardware).

**Fewer bytes per token of context**
- Grouped-query / multi-query attention.
- KV-cache quantization (8-bit, 4-bit K/V).
- Sliding-window attention and attention sinks for long streams.

**Fewer weight reads per token**
- **Speculative decoding:** a small draft model proposes several tokens; the big
  model verifies them in one pass. Because decode is bandwidth-bound, verifying
  k tokens costs almost the same as generating one.
- **Mixture of experts:** only a fraction of weights are active per token, so
  bandwidth cost scales with *active* parameters, memory with *total*.
- Batching (more useful for servers than for one user).

**A smaller model that knows enough**
- **Distillation:** train a small student on a large teacher's outputs.
- **Retrieval:** store facts outside the weights. The old project's fine-tuning result is
  this pillar's starting hypothesis: fine-tuning taught style, retrieval
  supplied facts. Test it again here rather than assuming it.
- **Task-specific small models:** a 100M-parameter model trained for one domain
  can beat a general 1B on that domain.

**Better use of the hardware**
- Kernel and backend settings (llama.cpp threads, batch, offloaded layers,
  flash-attention flag, Vulkan vs. CPU).
- Memory layout and tiling. FlashAttention is a memory-access-pattern
  optimization, not a maths change.
- CPU+GPU split when a model doesn't fit: which layers go where.

### 6.5 The ladder

**L0: Internals.** A small GPT from a blank file: BPE tokenizer, single-head
then multi-head attention (asserted against a hand-computed 3×3 case), the full
block, a training loop. Diff against a reference implementation only after it
trains.

**L1: Measure.**
- Build the llama.cpp Vulkan toolchain and a fresh benchmark harness.
- Quantization matrix on the RX 570 for one off-the-shelf small open model
  (≈1–3B): Q8_0 / Q6_K / Q5_K_M / Q4_K_M (+ Q3/Q2). Perplexity on a fixed
  held-out text, tok/s prefill and decode, VRAM, joules/token.
- Same matrix on the Pi 400 (CPU) and PC CPU-only.
- Deliverable: **quality vs. joules/token vs. memory plot**, three devices.

**L2: Predict.**
- Write the speed/energy model from 6.2 yourself. Check it on all measured devices.
- Apply it to a comparison set of chips from spec sheets (old GDDR card, current
  consumer card, data-center HBM accelerator, unified-memory laptop chip, phone
  SoC). Mark measured vs. predicted rows clearly.
- KV-cache calculator: for any model config + context + quant, total memory and
  whether it fits in 8/16/32 GB.
- Deliverable: "Will it fit, how fast, how many joules": a small tool plus a
  table, validated on your three devices.

**L3: Optimize what exists.**
- **Optimizing harness** (glue code, Claude can write it): sweeps llama.cpp
  settings per model/quant/device, records every run with provenance, outputs
  the Pareto front over tok/s, J/token and peak temperature. v2 is
  thermal-aware: a config that throttles after five minutes loses.
- Speculative decoding on the RX 570: draft model size vs. acceptance rate vs.
  speedup. Measured.
- KV-cache quantization: memory saved vs. perplexity lost at long context.
- imatrix quantization vs. plain k-quants at the same size.

**L4: Build new small models.**
Realistic scale for your compute: **tens to low hundreds of millions of
parameters**, trained on Colab/Kaggle GPUs. That's enough for real research
questions, and not enough to compete with frontier labs on general chat, so
don't frame it that way.
- Train a ~10–50M model from your own mini-GPT code on a public dataset
  (e.g. a TinyStories-style corpus **[verify]**). Get the loss curve to match
  published small-model results first.
- Then vary one thing at a time and measure quality *per byte* and *per joule*:
  GQA vs. full attention, low-bit-aware training vs. post-training quantization,
  depth vs. width at fixed parameters, vocabulary size.
- Distill a small domain model (physics/astro Q&A) from a larger open model's
  outputs, then quantize it and run it on the Pi.
- Deliverable: "A __M-parameter model that runs at __ tok/s on a Raspberry Pi
  400 and beats __ on __," with the honest comparison included.

### 6.6 Done-when bar for the first year

A public benchmark of small-model inference on weak hardware *with energy
numbers*, a validated fit/speed/energy predictor, and one small trained model
with an honest comparison against an off-the-shelf model of the same size.

---

## 7. Pillar III: Computational astrophysics and instrumentation

### 7.1 The question

*What can one person with code, public data and cheap hardware actually detect,
simulate and measure about the universe, and how close can it get to
professional results?*

### 7.2 Foundations

| Topic | Core idea |
|---|---|
| Transit photometry | Depth ≈ (R_planet / R_star)²; period from repetition; shape from limb darkening |
| Period search | Box Least Squares (BLS) for transits; Lomb–Scargle for sinusoids |
| Systematics removal | Co-trending with SVD/PCA on pixel or star ensembles (old project did this; redo it) |
| Orbital mechanics | Kepler's laws; N-body; symplectic integrators conserve phase-space structure |
| Matched filtering | Correlate data with a template, weighted by noise spectrum; the GW detection method |
| Radial velocity | Doppler shift of stellar spectra; complements transits (mass vs. radius) |
| Radio astronomy | Neutral hydrogen emits at 1420.4 MHz (the 21-cm line); Doppler shifts map galactic rotation |

### 7.3 The ladder

**Arc A: Exoplanet transits.**
- Synthetic light curves with known planets (ground truth), then SVD/PCA
  co-trending on real pixel data.
- Then: BLS written by hand and tested against synthetic injections →
  Mandel–Agol limb-darkened transit model → fit real Kepler/TESS targets with
  `lightkurve` **[verify current API]** → **injection-recovery test** (inject
  fake planets into real light curves, measure the detection rate vs. depth and
  period). That last plot is a genuinely professional-grade result.
- Stretch: search a set of TESS light curves for candidates and compare against
  the official TOI catalogue.

**Arc B: N-body and dynamics.**
- Direct O(N²) simulator with energy diagnostics; reproduce the integrator
  comparison (Verlet vs. RK4/RK45) from scratch and write it up properly.
- Then **Barnes–Hut** tree code
  (O(N log N)) with a measured accuracy-vs-speed curve; leapfrog with adaptive
  timesteps; check against REBOUND **[verify]**.
- Optimization tie-in (Pillar II): vectorize, then try Julia, then try the GPU
  (Vulkan compute or OpenCL) and measure the speedup, bandwidth-bound or not.
- Science targets: stability of a planetary system (e.g. resonant chains),
  galaxy collision with dark-matter halos, cluster evaporation.

**Arc C: Gravitational waves.**
- Public strain data from GWOSC **[verify]**. Whiten, bandpass, then matched
  filtering of a known event (GW150914 is the canonical first target).
  Reproduce the signal-to-noise peak yourself.
- Same maths as convolution in Pillar II and correlation in Pillar IV.

**Arc D: Instrumentation: astronomy with your own hardware.**
- **Pi camera astrophotography:** stacking, dark/flat frames, plate solving.
  Light-pollution measurement over time, logged like telemetry.
- **Radio astronomy with an SDR:** a cheap RTL-SDR plus a homemade horn antenna
  can detect the 21-cm hydrogen line; with enough pointings, a rough Milky Way
  rotation curve. A well-documented amateur project **[verify build guides]**,
  and it ties in signal processing (FFT, integration, noise).
- **Variable star photometry** from your own images, compared against AAVSO data
  **[verify]**.

### 7.4 Done-when bar for the first year

An injection-recovery study on real TESS/Kepler data with your own BLS, a
published Barnes–Hut accuracy/speed result, and one result from your own
hardware (a hydrogen-line detection or a measured variable-star light curve).

---

## 8. Pillar IV: Quantum and quantitative trading research

### 8.1 The question

*Do quantum and quantum-inspired optimization methods find better portfolios
or signals than strong classical baselines, under honest costs, on data you
can reproduce?*

### 8.2 Interface with the Claude Code project

You have a separate Claude Code project building quantum trading logic right
now. This charter doesn't know its contents, so **in week one, fill in this
table** and treat that project as the pillar's starting point instead of
rebuilding it:

| Question | Answer (fill in) |
|---|---|
| What problem does it solve (portfolio selection, signal, execution, pricing)? | |
| What's "quantum" in it: QUBO/QAOA, annealing, quantum ML, or quantum-inspired? | |
| Which library (Qiskit, PennyLane, D-Wave Ocean, custom simulator)? | |
| What's the classical baseline it's compared against? | |
| What data, which date range, cached where? | |
| What are transaction costs assumed to be? | |
| Which parts did you write by hand? | |

Then the rules below apply to it as to everything else.

### 8.3 Foundations, honestly framed

**The classical core** (this is where returns are actually decided):
- Returns, volatility, Sharpe, drawdown; why log returns.
- Factor models: PCA/SVD on return covariance.
- Regime detection: hidden Markov models.
- Mean–variance optimization and why it's unstable (estimation error);
  shrinkage covariance estimators.
- Execution cost: the Almgren–Chriss model of market impact.
- **Validation:** walk-forward testing, out-of-sample discipline, and correcting
  for multiple testing (try 100 strategies and one will look great by luck).
  The deflated Sharpe ratio exists for exactly this **[verify: Bailey & López de Prado]**.

**The quantum part:**
- **QUBO:** portfolio selection ("pick k of N assets maximizing return minus
  risk") can be written as a quadratic unconstrained binary optimization. Write
  this mapping by hand; it's the core skill.
- **QAOA:** a variational quantum algorithm for QUBOs. On today's hardware and
  simulators it works on small N only. Simulate it classically for N ≈ 4–20.
- **Quantum annealing:** the same QUBO on annealing hardware; classical
  simulated annealing is the baseline it has to beat.
- **Quantum amplitude estimation:** a theoretical quadratic speedup for Monte
  Carlo pricing/risk. Needs fault-tolerant hardware that doesn't exist yet at
  useful scale. Learn the theory; don't promise results.
- **Quantum machine learning:** heavily hyped; benchmark any claim against a
  classical model of similar capacity.

**The honest expectation:** at the scales you can simulate, a well-tuned classical
solver (simulated annealing, exact branch-and-bound for small N, or plain
mean–variance) will usually match or beat QAOA. That's a fine result if
measured carefully. The research value is in (a) the mapping, (b) how solution
quality scales with N and circuit depth, and (c) where, if anywhere, the
crossover might appear. Quantum-*inspired* classical algorithms (e.g. tensor
networks, simulated bifurcation) are a legitimate and often stronger direction.

### 8.4 The ladder

**L0: Foundations.** A cached data pipeline, a backtester with explicit costs,
SVD factors and an HMM regime model, all written fresh with tests. Plus
whatever the Claude Code quant project already provides (8.2); that project is
current work, not old research-lab code, so it's fine to build on.

**L1: Baselines and validation harness.**
- One benchmark harness that every strategy, classical or quantum, goes through:
  same data, same costs, walk-forward splits, deflated Sharpe, turnover, drawdown.
- Baselines: buy-and-hold SPY, equal-weight, minimum-variance, mean–variance
  with shrinkage.

**L2: Portfolio selection as a QUBO.**
- Hand-write the QUBO for cardinality-constrained selection (penalty terms for
  the constraint; choosing the penalty weight is a real research question).
- Solve with: brute force (N ≤ 20, exact answer), simulated annealing, QAOA on
  a simulator at depth p = 1…5.
- Measure: approximation ratio vs. exact, vs. N and p; wall time; then
  out-of-sample performance of the chosen portfolios through the L1 harness.

**L3: Scaling and quantum-inspired methods.**
- Push N with classical heuristics and quantum-inspired solvers.
- Regime-conditional portfolios: HMM regime → different QUBO per regime.
- Optional: run a tiny instance on real quantum hardware via a free cloud tier
  **[verify current availability]** and compare noisy hardware vs. simulator.

**L4: Research write-up.**
- "Quantum vs. classical portfolio selection at small N, under honest costs,"
  with the code public and every negative result included.

### 8.5 Done-when bar for the first year

A reproducible comparison of QAOA, simulated annealing and classical
optimizers on the same QUBO family, plus out-of-sample performance through a
validation harness that includes costs and multiple-testing correction.

---

## 9. The shared core

### 9.1 One math library (`core/`)

Imported by all four pillars. Each function has tests against a hand-computed case.

| Module | Used by |
|---|---|
| `decomposition` (SVD, PCA, low-rank) | III co-trending, IV factors, II LoRA/compression |
| `spectral` (FFT, PSD, whitening, Lomb–Scargle) | III GW/periodicity, IV cycles, I transient analysis |
| `integrators` (Euler, RK4, Verlet/leapfrog, adaptive) | III N-body, I thermal ODEs |
| `pde` (FDM stencils, CFL checks, sparse implicit solves) | I heat, III (later) |
| `optimize` (grid, Nelder–Mead, simulated annealing, Bayesian) | I design, II harness, IV QUBO baseline |
| `stats` (bootstrap, walk-forward splits, deflated Sharpe, HMM) | IV, III detection significance |
| `montecarlo` (samplers, variance reduction) | IV pricing, III injection-recovery |

### 9.2 One benchmark/provenance format

Every measurement row, in every pillar, carries: timestamp, machine, git commit,
key software versions, driver version (if GPU), config, result, units. One
schema, one CSV/parquet convention, so any result can be joined with telemetry.

### 9.3 Telemetry

Write a new exporter for the PC and Pi (LibreHardwareMonitor on Windows,
sysfs on the Pi) that writes timestamped samples into one local cache using the
provenance schema. Experiments read their power/temperature window from that
cache. Pillar I uses it to fit thermal models; Pillar II uses it for energy.

### 9.4 The journal

`docs/JOURNAL.md`, newest first. Each entry: what was built and run, the numbers,
what it means (physics/maths written out so it can be copied into the paper
notebook), and the wrong turns.

---

## 10. Repository layout

```
<new-project>/
├── CLAUDE.md                 # Part 12, adapted
├── README.md                 # one-paragraph mission + how to run tests
├── docs/
│   ├── CHARTER.md            # this file
│   ├── NOW.md                # the dated fortnight; rewrite, don't grow
│   ├── JOURNAL.md
│   └── sources/              # cached papers' metadata, spec sheets, retrieval dates
├── core/                     # shared math library + tests
├── bench/                    # provenance schema, harnesses, optimizer sweeps
├── telemetry/                # new exporter + cache reader
├── p1_thermal/
│   ├── analytical/  fdm_julia/  compact_models/  fit_real/  atomistic/  cfd/  control/
├── p2_ai_hw/
│   ├── from_scratch/  quantization/  predictor/  harness/  speculative/  small_models/  rag/
├── p3_astro/
│   ├── transits/  nbody/  gw/  instruments/
├── p4_quant/
│   ├── data/  validation/  classical/  qubo/  qaoa/  results/
└── results/                  # committed CSVs + PNGs that back public claims
```

Large files (model weights, raw telescope/strain data, GGUFs) are gitignored and
regenerable; the numbers that matter get copied into `results/` and the journal.

---

## 11. The first twelve weeks (12 Oct 2026 to 3 Jan 2027)

Sized for a school schedule: about two evenings and one weekend block per week.
**One pillar is "lead" each week; the others get at most one small task.** If a
week slips, drop the stretch items, never the measurement.

### Week 0 (12–18 Oct): Founding
- [ ] Create the repo with the layout above; copy `CLAUDE.md` from Part 12.
- [ ] Mark the old `research-lab` repo archived (read-only). Don't copy code over.
- [ ] Define the provenance schema (Part 9.2) and write the first `core`
      functions with tests (SVD wrapper, a test helper for hand-computed cases).
- [ ] New telemetry exporter on the PC; confirm GPU power actually reads.
- [ ] Fill in the Part 8.2 table from the Claude Code quant project.
- [ ] Answer the Part 15 questions.
- [ ] Deadline check: Congressional App Challenge closes **26 Oct, 12:00 ET**. If
      you registered, decide this week what you're submitting.

### Weeks 1–2 (19 Oct–1 Nov): Pillar II leads, measure
- [ ] Build llama.cpp (Vulkan) and the benchmark harness.
- [ ] Run the quantization matrix on the RX 570 (perplexity, tok/s, VRAM, J/token).
- [ ] Same on PC CPU-only and the Pi 400.
- [ ] Measure the PC's RAM bandwidth.
- [ ] Commit the first plot + CSVs. Journal entry.

### Weeks 3–4 (2–15 Nov): Pillar I leads, fit reality
- [ ] Fit the RC thermal model to the RX 570 telemetry from weeks 1–2. Predict a
      held-out run.
- [ ] Analytical 1D baselines (L0), then the 2D explicit solver with a
      convergence study (L1).
- [ ] Acoustic impedance screening for TIM candidates (Avenue 1 Step 1).

### Weeks 5–6 (16–29 Nov): Pillar IV leads, harness and QUBO
- [ ] Validation harness: walk-forward, costs, deflated Sharpe; run the baselines.
- [ ] Data pipeline + backtester with costs (L0), if the Claude Code project
      doesn't already cover them.
- [ ] Hand-write the portfolio QUBO. Brute force vs. simulated annealing at N ≤ 20.
- [ ] Plug in the Claude Code project's quantum solver; first comparison table.

### Weeks 7–8 (30 Nov–13 Dec): Pillar III leads, transits
- [ ] Synthetic transit generator, then BLS by hand, validated on injections.
- [ ] First real Kepler/TESS light curve through the pipeline.
- [ ] Stretch: direct N-body + integrator comparison, rebuilt from scratch.

### Weeks 9–10 (14–27 Dec): Pillar II leads, predict and optimize
- [ ] Speed/energy predictor, validated on three devices; comparison-chip table
      with cached, sourced specs.
- [ ] Optimizing harness v1 (llama.cpp settings sweep → Pareto front).
- [ ] Speculative decoding experiment on the RX 570.

### Week 11 (28 Dec–3 Jan): Consolidate
- [ ] One public write-up of the strongest result so far (likely: quality vs.
      energy on an old GPU + the thermal fit, i.e. Pillars I and II together).
- [ ] Rewrite `NOW.md` for the next quarter based on what the measurements said.

### Quarter 2 preview (Jan–Mar 2027)
Contact resistance + implicit solver (I-L1), then the compact multi-chip model (I-L3) · first small model trained from
scratch (II-L4) · injection-recovery, N-body + Barnes–Hut, GW matched filtering (III) · QAOA depth/scaling
study (IV-L2/L3) · instrumentation build (SDR or camera).

---

## 12. `CLAUDE.md` template for the new project

```markdown
# <Project name>: working agreements

Four pillars: (I) thermodynamics & microchip engineering, (II) AI hardware &
small-memory models, (III) computational astrophysics & instrumentation,
(IV) quantum & quantitative trading research. One thesis: computation is limited
by moving bytes and removing heat; the same maths (SVD, PDEs, stochastic
processes, optimization) runs through all four. Full charter: docs/CHARTER.md.

## Starting from scratch
This project does not import, copy or extend code from the old
"The Study of Important Things/research-lab" repo. That repo is archived,
read-only context: its findings (docs/CHARTER.md Part 4) inform decisions, and
its outputs may be used as a comparison check *after* new code is written.
Don't suggest porting old modules.

## Before starting any session
1. Read docs/NOW.md and the top of docs/JOURNAL.md.
2. Run `git log --oneline -15` and `git status`. Don't redo finished work; don't
   touch another session's uncommitted files without asking.

## Who writes what
- Adham writes by hand: solvers, attention/model architecture, prediction
  models, trading strategy/signal logic, QUBO formulations. Claude may scaffold
  with clearly marked blanks, explain, and review, but not fill these in.
- Claude may write: harnesses, plumbing, data pulls, plotting, tests, CI,
  benchmarks, docs for code that exists.

## Rules
- Label every command with its machine: PC (sim-server: Ryzen 7600X, RX 570 8GB,
  Vulkan only, no CUDA/ROCm), laptop, Pi 400, or Colab/Kaggle.
- A run you didn't log didn't happen: config, versions/commits, hardware,
  results with units, wall time. Numbers, not adjectives.
- Verify before asserting. Specs, papers, connector data: cite source and
  retrieval date, cache to disk. Never type a spec from memory.
- Measure before optimizing; log before/after.
- Every result has a baseline (PID, same-size off-the-shelf model, SPY after
  costs, simulated annealing). Publish losses too.
- Trading is paper/backtest only. No live orders, no order-placing brokerage
  connections. Read-only data is fine.
- No secrets in chat or git. If a key appears, say it needs rotating.
- Running code beats more documents.

## Hardware facts (measured, don't re-derive)
- RX 570: 7.75 GB device-local VRAM via Vulkan; 224 GB/s; inference only.
- Training / CUDA-only quantization → Colab/Kaggle T4.
- Telemetry: exporter → parquet cache; GPU power via LibreHardwareMonitor on Windows.
```

---

## 13. Reading list (primary sources)

Read the originals, not summaries. Fetch via Consensus / Firecrawl / alphaXiv
and record retrieval dates. Titles are from memory, so **[verify]** each one
before citing.

**Pillar I**
- Incropera et al., *Fundamentals of Heat and Mass Transfer* (textbook; chapters
  on conduction, transient conduction, convection).
- Swartz & Pohl (1989), "Thermal boundary resistance," *Rev. Mod. Phys.* (AMM/DMM).
- Cahill et al., reviews of nanoscale thermal transport (2003, 2014).
- Skadron et al., the HotSpot compact thermal modeling papers.
- Dennard et al. (1974) on MOSFET scaling, to understand what ended.

**Pillar II**
- Vaswani et al. (2017), "Attention Is All You Need."
- Williams, Waterman & Patterson (2009), "Roofline" model.
- Dao et al. (2022), "FlashAttention."
- Hu et al. (2021), "LoRA"; Dettmers et al. (2023), "QLoRA."
- Frantar et al. (2022), "GPTQ"; Lin et al. (2023), "AWQ."
- Leviathan et al. (2023) and Chen et al. (2023) on speculative decoding.
- Ainslie et al. (2023), "GQA."
- Hinton et al. (2015), "Distilling the Knowledge in a Neural Network."
- Hoffmann et al. (2022), "Chinchilla" scaling laws.
- Ma et al. (2024), "The Era of 1-bit LLMs" (BitNet b1.58).
- Eldan & Li (2023), "TinyStories."

**Pillar III**
- Kovács, Zucker & Mazeh (2002), BLS algorithm.
- Mandel & Agol (2002), analytic transit light curves.
- Barnes & Hut (1986), "A hierarchical O(N log N) force-calculation algorithm."
- Abbott et al. (2016), observation of GW150914; GWOSC tutorials.
- Rein & Liu (2012), REBOUND.

**Pillar IV**
- Markowitz (1952), "Portfolio Selection."
- Almgren & Chriss (2000), optimal execution.
- Farhi, Goldstone & Gutmann (2014), "A Quantum Approximate Optimization Algorithm."
- Lucas (2014), "Ising formulations of many NP problems."
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio."
- Hamilton (1989), regime-switching models.
- Orús, Mugel & Lizaso (2019), review of quantum computing for finance.

---

## 14. Turning this into a future: outputs that count

Code in a private folder doesn't count for much on its own. These do:

- **Public write-ups with code and data.** A blog or GitHub Pages site; each post
  is one measured result with a reproducible repo. Four strong posts beat forty
  plans.
- **Preprints.** A well-done methodological study (e.g. energy-per-token on
  consumer hardware; injection-recovery with a homemade BLS) can become a short
  paper. Getting arXiv endorsement as an independent author takes a mentor;
  that's another reason to find one.
- **Science competitions.** Regional science fairs that feed into ISEF, and
  other national research competitions, reward exactly this kind of measured,
  honest project. Check each one's eligibility rules and deadlines **[verify]**.
  Pillars I+II together (the thermal cost of AI inference) are the strongest
  single entry.
- **App/tool competitions.** The Congressional App Challenge (26 Oct 2026) and
  similar. The fit/speed/energy predictor is a natural entry.
- **Mentors.** One email to a professor or grad student whose paper you've
  actually read and reproduced part of is worth more than ten generic ones.
  Lead with your measured result.
- **Open-source contributions.** A benchmark result, a docs fix or a bug report to
  llama.cpp, REBOUND, lightkurve or Qiskit is public, reviewable proof of skill.
- **Summer research programs.** Many have early-year deadlines; list them in
  `NOW.md` in December **[verify dates]**.

The old project's bottleneck was never code. It was the steps that involve
other people: registering, emailing, publishing. Put at least one of those in
every fortnight's `NOW.md`.

---

## 15. Open questions to settle in week one

1. **Name and location** of the new project (folder, repo, public or private).
2. **The old project's status:** archived read-only (decided). Only the stock
   station keeps running there.
3. **The Claude Code quant project:** does it move into `p4_quant/` or stay a
   separate repo that `p4_quant` imports?
4. **Python vs. Julia split:** Julia for PDE solvers and N-body hot loops, Python
   for everything else is a reasonable default; decide once.
5. **Hours per week**, honestly, during school. The Part 11 plan assumes ~6–8.
6. **One public outlet** (blog, GitHub Pages, or a channel) and the date of the
   first post.
7. **Which mentor** you'll email first, and which result you'll lead with.
