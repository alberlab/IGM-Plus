import tempfile
import unittest
import warnings
from pathlib import Path

import h5py
import numpy as np

from igm.model import Model, Particle
from igm.model.forces import ExcludedVolume
from igm.restraints.sprite import Sprite


def make_model():
    model = Model()
    for x, radius in [(0, 1), (1, 2), (5, 0.5)]:
        model.addParticle([x, 0, 0], radius, Particle.NORMAL)
    return model


class TestNumpyScalarCompatibility(unittest.TestCase):
    def test_excluded_volume_scores(self):
        model = make_model()
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            scores = ExcludedVolume([0, 1, 2]).getScores(model.particles)
        np.testing.assert_array_equal(scores, [2, 0, 0])

    def test_sprite_restraint_bounds(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assignment.h5"
            with h5py.File(path, "w") as assignment:
                assignment["assignment"] = [0]
                assignment["indptr"] = [0, 3]
                assignment["selected"] = [0, 1, 2]
            model = make_model()
            restraint = Sprite(str(path), 0.5, 0)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error", DeprecationWarning)
                    model.addRestraint(restraint)
            finally:
                restraint.assignment_file.close()

        cluster_radius = ((1**3 + 2**3 + 0.5**3) / 0.5)**(1.0 / 3.0)
        self.assertEqual(len(model.forces), 3)
        self.assertTrue(all(isinstance(force.d, float) for force in model.forces))
        np.testing.assert_allclose(
            [force.d for force in model.forces],
            [cluster_radius - radius for radius in [1, 2, 0.5]],
            rtol=1e-6,
        )

class TestViolationLogging(unittest.TestCase):
    def test_unique_and_tied_worst_structures(self):
        import importlib
        import json
        import logging
        from unittest.mock import patch

        from alabtools.analysis import HssFile

        module = importlib.import_module("igm.steps.ModelingStep")

        class Capture(logging.Handler):
            def emit(self, record):
                messages.append(record.getMessage())

        logger = logging.Logger("numpy-compatibility-test", logging.INFO)
        logger.addHandler(Capture())

        for violations, expected in [
            ([1, 2], "Mostly violated in structure 1 =>  0.200000, [2 / 10]"),
            ([2, 2], "Mostly violated in  2 structures  =>  0.200000, [2 / 10]"),
        ]:
            with self.subTest(violations=violations), tempfile.TemporaryDirectory() as directory:
                messages = []
                total = sum(violations)
                summary = {
                    "n_violations": total, "n_imposed": 20, "violated_restr": total,
                    "byrestraint": {"test": {
                        "n_violations": total, "n_imposed": 20,
                        "viol_by_struct": violations, "imposed_by_struct": [10, 10],
                    }},
                    "bystructure": {
                        "total_energies": [10, 20], "pair_energies": [3, 4],
                        "bond_energies": [7, 16],
                    },
                }
                with HssFile(Path(directory) / "stats.hss", "w") as hss:
                    hss.nstruct, hss.nbead = 2, 3
                    hss["summary"] = json.dumps(summary)
                    with patch.object(module, "logger", logger), warnings.catch_warnings():
                        warnings.simplefilter("error", DeprecationWarning)
                        score = module.log_stats(hss, {"optimization/max_violations": 0.1})
                self.assertEqual(score, total / 20)
                self.assertTrue(any(expected in message for message in messages), messages)


if __name__ == "__main__":
    unittest.main()
