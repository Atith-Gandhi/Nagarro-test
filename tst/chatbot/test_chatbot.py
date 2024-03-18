import unittest
from unittest.mock import patch
from src.chatbot.prompt import parse_prompt
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from utils import text_to_dict

class TestParsePrompt(unittest.TestCase):
    # @patch('Anthropic')
    # @patch('text_to_dict')
    def test_parse_prompt(self):
        # Mocking the return values for the Anthropic instance and text_to_dict function
        # mock_completion = Anthropic.return_value.completions.create.return_value
        # mock_completion.completion = "task_type: Create\n task_name: Example Task\n timestamp: 2024-03-17T12:00:00Z\n priority: High"
        # text_to_dict.return_value = {
        #     "task_type": "Create",
        #     "task_name": "Example Task",
        #     "timestamp": "2024-03-17T12:00:00Z",
        #     "priority": "High"
        # }

        # Call the function under test
        result = parse_prompt("task_type: Create, task_name: Example Task, timestamp: 17th March 2024 12:00:00 PM, priority: High")

        # Assert the function output
        self.assertEqual(result, {
            "task_type": "Create",
            "task_name": "Example Task",
            "timestamp": "2024-03-17 12:00:00",
            "priority": "High"
        })

if __name__ == '__main__':
    unittest.main()
