
import unittest
from unittest.mock import MagicMock, patch


class TestCVAgentInit(unittest.TestCase):

    @patch("warstwa_wizji.src.cv_agent.DetectionPipeline")
    @patch("warstwa_wizji.src.cv_agent.PersonAnalyzer")
    @patch("warstwa_wizji.src.cv_agent.VideoIO")
    @patch("warstwa_wizji.src.cv_agent.ModelManager")
    def test_creates_all_components(self, MockMM, MockVIO, MockPA, MockDP):
        from warstwa_wizji import CVAgent
        agent = CVAgent(weights_path="fake.pt", source=0)
        MockMM.assert_called_once()
        MockVIO.assert_called_once()
        MockPA.assert_called_once()
        MockDP.assert_called_once()
        self.assertIsNotNone(agent.models)
        self.assertIsNotNone(agent.video)
        self.assertIsNotNone(agent.person_analyzer)
        self.assertIsNotNone(agent.pipeline)