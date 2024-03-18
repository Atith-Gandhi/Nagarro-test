import unittest
from unittest.mock import patch
from src.chatbot.prompt import parse_prompt
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from utils import text_to_dict

class TestParsePrompt(unittest.TestCase):
    def test_parse_prompt(self):

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
