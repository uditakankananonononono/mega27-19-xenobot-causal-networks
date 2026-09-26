# External ChatGPT judge rounds - Xenobot project

Responses are advisory, not verified facts, authorization or official ISEF judgments. Scientific claims require independent source and data checks. The user asked for >=10 substantive rounds; only completed external responses count.

## Round 1, 2026-09-26 16:12 IST
Source URL: https://chatgpt.com/c/6ab7a19a-6f48-83e8-a29c-83c273c6d1fd

### Exact prompt submitted

Act as a demanding scientific judge, round 1 of at least 10. Critique this computational research proposal, not praise it: "Computationally Decoding Emergent Intelligence in Xenobots Through Causal Cellular Networks." Goal: cell-level dynamic graphs combining gene expression, bioelectric state, mechanics/signaling, tracked imaging, GNNs, causal inference/information theory and evolutionary optimization to find minimal networks for coordinated behavior, memory and self-replication. Current verified public-data constraints: Blackiston et al. repository provides 12 whole-Xenobot trajectory CSV archives with one treatment condition per numbered replicate, no per-cell tracks; 2025 basal Xenobot study has bulk RNA-seq of 3 Xenobot and 3 embryo samples, embryonic scRNA reference from another stage; March 2026 Xenobot memory preprint reports cell-spatial calcium imaging and stimuli but transcription samples pool 50 bots per biological replicate, and raw matched calcium+behavior movies remain unverified. We have only a preregistration and structural QC, no result. Judge scientific novelty relative to 2025/2026 work, fatal confounding/leakage, falsifiable scope, data feasibility, strongest fair benchmark and what exact addition could produce a new, independently valid discovery without wet-lab claims. Do not invent access to data or guarantee a benchmark win. Give prioritized weaknesses, fixes, and a clear pass/fail gate for the next iteration.

### Verbatim ChatGPT response (untrusted external critique)

Round 1/10 — Scientific Judge Review

Proposal: “Computationally Decoding Emergent Intelligence in Xenobots Through Causal Cellular Networks”
Judging standard: Competitive computational biology / ISEF-level / serious preprint-level scrutiny. I will evaluate what is actually feasible from the stated public-data constraints, not the ambition of the concept.

Overall verdict: FAIL in current form (high-concept, low empirical grounding)

The proposal currently describes a grand unification framework (cellular graphs + bioelectricity + mechanics + gene regulation + causal inference + evolutionary search), but the available evidence base does not support the central claims. The largest problem is not the modeling sophistication; it is that the proposed model requires paired, cell-resolved, multimodal causal data that apparently do not exist publicly in the required form.

At present, this is closer to a research vision than a falsifiable computational study.

A strong revision could become viable, but it must dramatically narrow the question.

1. Scientific novelty relative to 2025/2026 Xenobot work
Current novelty claim

The proposal appears to claim:

"We will discover the minimal causal cellular networks underlying emergent intelligence, memory, and self-replication."

This is extremely ambitious.

The issue:

Recent Xenobot work has already moved toward:

behavioral characterization,

regeneration/self-organization,

bioelectric control,

calcium dynamics,

transcriptomic characterization,

computational modeling of multicellular systems.

A new contribution cannot simply be:

"Use AI/GNNs on Xenobot data."

That is now a common pattern in biology.

The novelty must come from a specific unresolved biological question.

Examples of potentially novel questions:

Can behavioral trajectories be predicted from available morphological states alone?

Can a graph model identify conserved cellular interaction motifs across independently generated Xenobot morphologies?

Can information-theoretic measures distinguish coordinated collective behavior from random aggregation?

Can evolutionary optimization recover known behavioral constraints without being given the answer?

Those are narrower and testable.

2. Fatal feasibility issue: proposed data modality does not exist
Proposed input:

cell-level dynamic graphs combining:

gene expression

bioelectric state

mechanics/signaling

tracked imaging

This requires:

Cell identity ↔ spatial position ↔ time-resolved behavior ↔ molecular state.

Your stated data situation:

Blackiston trajectory data:

Available:

12 whole-Xenobot trajectory CSV archives.

Missing:

cell tracks

molecular states

cell identities

This is behavioral-level data, not cellular-network data.

Basal Xenobot RNA-seq:

Available:

3 Xenobot + 3 embryo bulk RNA-seq.

Problems:

Bulk RNA-seq gives:

average expression over thousands of cells

not:

cell i expression at location x,y,z at time t

Therefore it cannot create a cellular graph.

It can provide:

pathway enrichment,

differential expression,

broad molecular context.

It cannot support:

cell-cell causal edges,

cell-specific states,

dynamic regulatory networks.

Memory preprint:

This is the closest match.

Potentially:

calcium imaging,

stimulus response,

behavior.

But stated limitations:

transcription samples pooled 50 bots/replicate.

matched raw calcium + behavior movies unverified.

Without matched datasets:

You cannot connect:

stimulus → calcium dynamics → cellular state → behavior.

You have disconnected modalities.

3. Biggest scientific flaw: causal inference without intervention

The word "causal" is currently unsupported.

A GNN learns:

X→Y

correlations.

It does not automatically learn:

do(X=x)→Y

causal effects.

For biological causality, you normally need:

perturbations,

interventions,

temporal constraints,

mechanistic priors.

Example:

Observed:

Cell A calcium increases before Cell B movement.

Possible explanations:

A controls B.

Both respond to stimulus C.

Measurement artifact.

Developmental timing difference.

A causal model cannot distinguish these without additional information.

Required fix

Rename the objective unless interventions exist.

Bad:

"Causal cellular networks"

Better:

"Mechanistically constrained predictive models of Xenobot collective behavior"

or:

"Inferring candidate interaction networks from observational Xenobot dynamics"

The distinction matters.

4. Data leakage risks

This proposal has several severe leakage pathways.

Leakage 1: replicate identity

Only 12 trajectory archives.

A model could easily learn:

replicate-specific morphology,

recording conditions,

preprocessing artifacts.

A random train/test split would be invalid.

Correct:

Leave-one-replicate-out validation.

Example:

Train:
Replicates 1-11

Test:
Replicate 12

Repeat 12 times.

Leakage 2: morphology shortcut

The model may learn:

"large circular Xenobots move differently"

rather than:

"cellular organization creates behavior."

Need ablations:

Model A:

morphology only

Model B:

dynamics only

Model C:

proposed graph features

The graph must outperform simpler explanations.

Leakage 3: evolutionary optimization overfitting

Evolutionary algorithms are powerful enough to generate convincing nonsense.

If optimized directly against observed trajectories:

the algorithm may find:

"models that reproduce this dataset"

not:

"biological mechanisms."

Require held-out validation.

5. Falsifiability problem

Current hypothesis:

"Find minimal networks for coordinated behavior, memory, self-replication."

This is not falsifiable because:

Almost any result can be interpreted as success.

Example:

No network found.

Possible excuse:

insufficient data.

Network found.

Possible excuse:

discovered biology.

Need explicit predictions.

Better hypotheses:
Hypothesis 1

"A graph neural network using morphology-derived cell neighborhoods predicts Xenobot movement trajectories better than non-graph baselines."

Pass/fail:

Graph model improves held-out prediction by X%.

Hypothesis 2

"Information-theoretic network measures distinguish coordinated from random cell assemblies."

Pass/fail:

Metric separates predefined behavioral states.

Hypothesis 3

"Evolutionary optimization recovers known Xenobot morphology constraints."

Pass/fail:

Recovered solutions resemble experimentally observed morphologies.

6. Benchmark problem

The proposal currently has no credible benchmark.

"Discover intelligence" is not a benchmark.

A fair benchmark:

Benchmark A: trajectory prediction

Input:

initial morphology

historical movement

Output:

future trajectory

Compare:

Linear model

Random forest

CNN/video model

GNN

Metric:

trajectory displacement error

correlation

generalization to unseen replicate

Benchmark B: behavior classification

Predict:

aggregation

movement persistence

response state

from morphology/dynamics.

Benchmark C: synthetic validation

Because real cell graphs are unavailable:

Generate synthetic multicellular systems where:

ground-truth interactions are known.

Question:

Can the method recover known networks?

This does not prove Xenobot biology, but validates the algorithm.

7. The strongest scientifically defensible version

The project should become:

"Inferring emergent behavioral rules in Xenobot collectives from morphology and trajectory dynamics using graph-based models"

Inputs:

Available:

trajectory CSV

morphology features if extractable

public imaging where confirmed

Outputs:

predictive model

interpretable graph features

candidate behavioral motifs

Claims:

Allowed:

"Models identified features associated with coordinated behavior."

Not allowed:

"We discovered the neural equivalent of Xenobot intelligence."

8. Exact addition that could create an independently valid discovery

The biggest missing piece is not another AI architecture.

It is a unique, testable biological/computational insight.

A possible high-value addition:

Evolutionary reconstruction benchmark

Build an artificial multicellular simulator:

Cells have:

positions

adhesion rules

communication edges

movement rules

Create:

known emergent behaviors.

Hide rules.

Run your algorithm.

Question:

Can it recover the minimal interaction network?

If yes:

Discovery:

"A graph-information framework can recover latent multicellular interaction rules from emergent behavior."

Then apply cautiously to Xenobot trajectories.

This would be a valid computational contribution.

Prioritized weaknesses
Rank	Weakness	Severity
1	Required multimodal cell-level dataset unavailable	Fatal
2	"Causal" claims unsupported by observational data	Fatal
3	No falsifiable biological hypothesis	Major
4	Benchmark undefined	Major
5	High overfitting risk with tiny datasets	Major
6	AI complexity exceeds available information	Major
7	Self-replication/memory claims far beyond data	Major
Required fixes before Round 2
Must do:
1. Remove unsupported claims

Delete:

decoding intelligence

causal cellular networks

minimal networks for self-replication

Replace with:

predictive modeling

candidate interaction inference

behavioral dynamics

2. Define one question

Example:

"Can graph representations of Xenobot morphology improve prediction of collective movement compared with conventional models?"

3. Establish dataset table

Before modeling:

Dataset	Exists?	Resolution
trajectory CSV	Yes	organism level
cell tracks	Unknown/no evidence	cell level
calcium movies	Unknown	cellular
matched transcriptomics	No	molecular

No modeling until this table is complete.

4. Build baseline first

A judge should see:

Week 1:

linear baseline

Week 2:

random forest

Week 3:

GNN

If GNN does not beat baseline, abandon the biological interpretation.

Round 1 Gate
PASS to Round 2 only if:

✅ A publicly accessible dataset is confirmed
✅ The research question is reduced to one measurable prediction task
✅ A non-AI baseline exists
✅ Validation uses unseen replicates
✅ Claims are reduced from causal discovery to inference/prediction
✅ A failure condition is explicitly written

Current score (Round 1)

Scientific ambition: high
Data realism: low
Causal rigor: insufficient
Computational novelty: possible but unproven
ISEF viability in current form: low

Decision: NO PASS. Major redesign required before evaluation can continue.

### Independent assessment and response
The critique correctly calls out disconnected modalities, causal overreach, weak novelty and need for baselines. It ALSO mistakenly proposes leave-one-replicate-out as adequate despite one condition per numbered replicate; that split tests a new condition and cannot establish same-condition independent-batch performance. Its synthetic simulator suggestion could become a software validation but **not** a Xenobot biological discovery; the suggested guarantee of a computational "discovery" is not accepted. Do not delete the user's original vision, but clearly label it a longer-term hypothesis and select measurable subquestions. Action: independently audit raw calcium availability; design a fair organism-level fallback with leakage controls and preregistered pivot before outcome scoring. Not yet accepted as a benchmark win or scientific result.

Status: 1/10 external judge rounds completed; no gate passed.

## Round 2, 2026-09-26 16:13 IST - stalled-feasibility redirection
Source URL: https://chatgpt.com/c/6ab7a19a-6f48-83e8-a29c-83c273c6d1fd

### Exact prompt submitted

Round 2/10, redirection after a failed feasibility gate. Your prior critique suggested leave-one-replicate-out, but independently checking info.xlsx shows each of the 12 numbered replicates has ONE DISTINCT treatment condition. Thus leave-one-out estimates unseen-condition transport, not same-condition independent biological generalization; it cannot meet the preregistered flagship gate. Also the archived tracks are whole-bot centroids, not cells, and no linked raw calcium movies have been verified. Please correct your previous advice. Give three specific pivots that remain genuinely about Xenobots and public data, each with: exact public source to verify (do not assert an uninspected dataset exists), biological unit, hypothesis, pre-registered success metric versus a matched strong benchmark, genuinely new discovery criterion rather than generic model fit, controls for condition/replicate confounding, and a fail-stop/next pivot. Rank which one can be done without falsely claiming cellular causal mechanisms. Explain why a synthetic simulator-only "discovery" would or would not satisfy the user's request for a Xenobot finding. No guaranteed positive outcome.

### Verbatim ChatGPT response (untrusted external critique)

Round 2/10 — Corrected feasibility assessment after dataset audit

The previous recommendation of leave-one-replicate-out validation was insufficiently qualified. Given the new information from info.xlsx:

Each numbered replicate corresponds to one distinct treatment condition.

The archived trajectories are whole-Xenobot centroid tracks, not cell-resolved trajectories.

Raw matched calcium imaging + behavior movies have not been verified.

Therefore:

Leave-one-replicate-out is not a biological replication estimate. It is primarily a condition-transfer test.

It answers:

“Can a model trained on some treatment conditions predict trajectories from a held-out treatment condition?”

It does not answer:

“Does the model generalize to independent Xenobots under the same biological condition?”

For the original preregistered flagship claim (cellular causal networks explaining emergent intelligence), this distinction is fatal. The data structure does not support that gate.

The project must pivot from cell-level causal discovery to a question supported by organism-level public observations.

Pivot 1 (highest feasibility): Xenobot behavioral dynamics from morphology-free trajectory representations
Core question

Can statistical or graph-derived representations of whole-Xenobot movement reveal reproducible behavioral motifs across independently generated conditions?

This stays Xenobot-focused without pretending to see cells.

Public source to verify

Candidate source:

Blackiston et al. Xenobot repository/archive.

Required verification before commitment:

confirm repository URL,

confirm exact trajectory files,

confirm metadata linking each CSV to treatment condition,

confirm whether any morphology descriptors are available.

Do not assume additional metadata exists.

Biological unit

Whole Xenobot trajectory.

Not:

cell,

gene,

neuron-like unit,

molecular state.

Hypothesis

Example preregistration:

Xenobot collective movement trajectories contain condition-independent dynamical motifs that can be represented more efficiently than raw coordinate sequences.

Success metric

Primary:

Compare:

Proposed model:

trajectory representation model

against:

Strong matched benchmarks:

autoregressive baseline

hidden Markov model

dynamic time warping nearest neighbor

simple kinematic feature classifier

Metrics:

held-out condition trajectory prediction error

clustering stability

representation similarity across conditions

New discovery criterion

Not:

“The model predicts movement.”

That is generic.

Discovery would require:

A previously unrecognized behavioral state structure that:

appears across multiple conditions,

survives removal of condition labels,

predicts future trajectory dynamics,

has a simple interpretable physical description.

Example:

“Xenobot trajectories transition between three dynamical regimes characterized by persistence, confinement, and reversal.”

That would be a behavioral discovery.

Confounding controls

Because condition and replicate are nearly identical:

Required:

no random frame-level train/test split,

no mixing trajectories from the same condition into train/test,

leave-condition-out analysis.

Additional controls:

shuffle condition labels,

compare against condition-only classifier,

test whether morphology/recording duration explains the result.

Fail-stop

If:

embeddings merely separate treatment labels,

no condition-general structure exists,

simple kinematic features perform equally,

stop.

Pivot to descriptive trajectory analysis rather than machine learning.

Pivot 2: Xenobot morphology–behavior relationship (if morphology data are verified)
Core question

Do observable whole-organism morphological features predict behavioral differences?

This is much closer to classical organismal biology.

Public source to verify

Potential sources:

Blackiston Xenobot repositories.

Associated image/video repositories if publicly linked.

Verification required:

confirm raw images exist,

confirm they correspond to the trajectory experiments,

confirm segmentation is possible.

Do not assume.

Biological unit

Individual Xenobot morphology.

Examples:

shape descriptors,

area,

circularity,

aspect ratio,

movement centroid.

Hypothesis

Morphological geometry explains measurable variation in Xenobot movement behavior better than treatment labels alone.

Success metric

Compare:

Model A:
treatment condition only

Model B:
morphology features

Model C:
morphology + treatment

Metrics:

held-out condition prediction,

variance explained,

predictive improvement over treatment-only baseline.

Discovery criterion

A novel result would require identifying:

A reproducible morphology–behavior relationship not obvious from treatment assignment.

Example:

Specific shape parameter predicts persistence or directionality across multiple conditions.

Confounding controls

Critical:

Treatment may create both:

morphology differences,

movement differences.

Need:

condition-stratified analysis,

within-condition comparisons if multiple organisms exist,

permutation testing.

Fail-stop

If morphology only acts as a proxy for treatment:

Do not claim biological principle.

Report:

“Observed association attributable to experimental condition.”

Pivot 3: Literature-grounded Xenobot computational meta-analysis
Core question

Can a computational framework unify reported Xenobot behaviors without claiming discovery of hidden cellular mechanisms?

This is lower risk but lower novelty.

Public sources to verify

Verify individually:

published Xenobot papers,

supplementary datasets,

repositories.

No assumption that all supplementary data are machine-readable.

Biological unit

Published Xenobot experiment.

Examples:

regeneration,

movement,

morphology,

stimulation response.

Hypothesis

Existing Xenobot studies can be quantitatively organized into behavioral phenotypes using a common representation.

Success metric

Compare:

manual annotation baseline,

simple feature extraction,

proposed representation.

Metric:

agreement with published phenotype labels.

Discovery criterion

A new taxonomy of Xenobot behavioral states supported across independent publications.

Confounding controls

Account for:

species/source differences,

developmental stage,

laboratory protocol,

imaging modality.

Fail-stop

If categories only reproduce publication boundaries:

No discovery.

Ranking: Which pivot avoids false cellular-causality claims?
Rank	Pivot	Feasibility	Xenobot specificity	Risk
1	Trajectory dynamics	Highest	High	Moderate
2	Morphology–behavior	Medium (depends on data access)	High	Moderate
3	Literature meta-analysis	Highest	Medium	Low novelty

The first pivot is the strongest because it accepts the actual data resolution.

Why the original cellular-network idea fails

The original claim requires:

cell state(t)+cell location(t)+behavior(t)

to infer:

cell interaction mechanism

Current verified data provide closer to:

whole-bot position(t)

Those are different biological levels.

A sophisticated GNN cannot manufacture missing variables.

A graph over centroid trajectories is not a cellular graph.

Would a synthetic simulator-only "discovery" satisfy the Xenobot request?
Short answer: No, not by itself.

A simulator can validate:

algorithm recovery,

identifiability,

optimization behavior.

It cannot establish:

a Xenobot mechanism,

a Xenobot behavioral law,

a biological discovery.

A simulator result would be:

“We developed a method capable of recovering known interaction rules in artificial multicellular systems.”

That is a computational methods contribution.

It becomes relevant to Xenobots only if:

the method is validated on known Xenobot observations,

assumptions are explicitly transferred,

claims remain limited.

Revised Round 2 gate

Before continuing:

Must verify:

Exact accessible Xenobot datasets.

Biological resolution of each file.

Whether independent units exist.

Whether condition and replicate can be separated.

Pass condition:

A valid next iteration must produce:

one Xenobot-specific question,

one measurable outcome,

one strong baseline,

one confound-controlled validation,

one claim that does not exceed data resolution.

At present, the project should abandon “decoding emergent intelligence through causal cellular networks” as the primary claim. The viable path is a narrower Xenobot behavioral computation study with explicit limits.

### Independent assessment and response
The correction is accepted: a leave-replicate-out test only assesses unseen-condition transfer here. Candidate pivots: Xenobot trajectory dynamics; morphology-behavior only if morphology and tracks match; cross-study taxonomy only with harmonized raw measures. The original archived raw track CSVs contain a `size` field, which might encode segmentation area and permit a narrower morphology-behavior analysis after code/metadata verification. However, ChatGPT's proposed same-condition replication remains absent and its trajectory benchmark cannot meet the preregistered independent experiment criterion. The proposed literature taxonomy lacks a defined published same-task benchmark. Synthetic simulator-only work does not constitute a Xenobot biological discovery. Keep the user's original long-term concept as an aim; do not silently rename or abandon it on an external assistant's advice. Next: verify `size` semantics and seek raw matched imaging; lock any narrower endpoint before opening outcomes.

Status: 2/10 external judge rounds completed; no science gate passed.
