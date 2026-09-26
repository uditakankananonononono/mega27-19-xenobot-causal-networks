import unittest
from src.gate import DatasetEvidence, decide

class GateTests(unittest.TestCase):
    def test_organism_tracks_are_not_cells(self):
        g=decide(DatasetEvidence(organism_tracks=True))
        self.assertTrue(g['whole_organism_movement_descriptive'])
        self.assertFalse(g['cell_graph_prediction_eligible'])
        self.assertFalse(g['operational_memory_test_eligible'])
    def test_cell_track_without_independent_batch_fails(self):
        g=decide(DatasetEvidence(organism_tracks=True,cell_tracks_same_organisms=True))
        self.assertFalse(g['cell_graph_prediction_eligible'])
    def test_pooled_expression_not_treated_as_cell_expression(self):
        g=decide(DatasetEvidence(organism_tracks=True, cell_tracks_same_organisms=True,
                                 independent_experiments_per_condition=True))
        self.assertTrue(g['cell_graph_prediction_eligible'])
        self.assertFalse(g['fully_multimodal_graph_eligible'])
    def test_memory_requires_intervention_and_washout(self):
        x=DatasetEvidence(organism_tracks=True,cell_tracks_same_organisms=True,
                          independent_experiments_per_condition=True,raw_postwashout_timecourse=True)
        self.assertFalse(decide(x)['operational_memory_test_eligible'])

if __name__=='__main__':unittest.main()
