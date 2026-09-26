"""Machine-checkable evidence gate for claims about measured Xenobot cell networks."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetEvidence:
    organism_tracks: bool = False
    cell_tracks_same_organisms: bool = False
    expression_same_cells_and_times: bool = False
    bioelectric_same_cells_and_times: bool = False
    mechanics_same_cells_and_times: bool = False
    signaling_same_cells_and_times: bool = False
    independent_experiments_per_condition: bool = False
    raw_intervention_and_control: bool = False
    raw_postwashout_timecourse: bool = False
    public_source_url: str = ''


def decide(e: DatasetEvidence):
    paired = e.organism_tracks and e.cell_tracks_same_organisms
    graph_benchmark = paired and e.independent_experiments_per_condition
    full_state = (graph_benchmark and e.expression_same_cells_and_times and
                  e.bioelectric_same_cells_and_times and
                  e.mechanics_same_cells_and_times and
                  e.signaling_same_cells_and_times)
    memory = (paired and e.raw_intervention_and_control and
              e.raw_postwashout_timecourse and e.independent_experiments_per_condition)
    return {
        'whole_organism_movement_descriptive': bool(e.organism_tracks),
        'cell_graph_prediction_eligible': bool(graph_benchmark),
        'fully_multimodal_graph_eligible': bool(full_state),
        'operational_memory_test_eligible': bool(memory),
        # Causal identification requires experiment-specific intervention controls,
        # not a graph model or an in-silico ablation alone.
        'experimental_causal_claim_established': False,
        'notes': 'Eligibility is not a passed scientific gate or proof of intelligence.'
    }
