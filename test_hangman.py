from io import StringIO
import unittest
from unittest.mock import patch

from hangman import get_player_names, get_guess_word, get_guess_char, \
    evaluate_word, play_one_round, play_another_round

class TestHangman(unittest.TestCase):

    @patch('builtins.input')  # Mock the built-in input function
    def test_get_player_names(self, mock_input):
        # Simulate user input for player names
        mock_input.side_effect = ['Alice', 'Bob']  # List of expected inputs
        names = get_player_names()
        # Verify returned names
        self.assertEqual(names, ('Alice', 'Bob'))

    @patch('pwinput.pwinput')  # Mock pwinput
    def test_get_guess_word(self, mock_pwinput):
        # Simulate user input
        mock_pwinput.return_value = "secret"  # Replace with your desired input

        # Mock SystemExit (optional)
        with patch('sys.exit'):

            player = "Alice"
            user_word = get_guess_word(player)

            # Verify function call and returned value
            mock_pwinput.assert_called_once_with(f'Enter your word: ', mask='*')
            self.assertEqual(user_word, "secret")
            
    @patch('builtins.input')  # Mock built-in input
    def test_get_guess_char_valid_input(self, mock_input):
        # Simulate valid character guess (not already guessed)
        player = "Alice"
        all_guesses = []
        mock_input.return_value = "x"  # User enters 'x'

        char_guess = get_guess_char(player, all_guesses)

        # Verify returned guess and all_guesses update
        self.assertEqual(char_guess, 'x')
        self.assertEqual(all_guesses, ['x'])

    @patch('builtins.input')  # Mock built-in input
    def test_get_guess_char_already_guessed_then_valid(self, mock_input):
        # Simulate user input sequence
        player = "Alice"
        all_guesses = ["a"]
        mock_input.side_effect = ["", "a", "b"]  # Empty string for empty input

        # Capture the output during the test
        captured_output = StringIO()
        captured_err = StringIO()
        with patch('sys.stdout', new=captured_output):
            with patch('sys.stderr', new=captured_err):
               char_guess =  get_guess_char(player, all_guesses)

        # Verify all messages using captured_output
        expected_messages = [
            f"System didn\'t detect valid input. Please try again.",
            f"You already guessed a. Try again."
        ]
        captured_output_value = captured_output.getvalue()
        print(f'Output value: {captured_output_value}')
        for expected_message in expected_messages:
            self.assertIn(expected_message, captured_output_value)

        self.assertEqual(mock_input.call_count, 3)  # Verify 3 calls (empty, 'a', 'b')

        # Verify second guess is accepted
        self.assertEqual(char_guess, 'b')
        self.assertEqual(all_guesses, ['a', 'b'])

    def test_evaluate_word(self):
        # Test word evaluation
        actual_word = "hello"
        good_guess = ["l"]
        evaluated_word, remaining_chars = evaluate_word(actual_word, good_guess)
        self.assertEqual(evaluated_word, ["*", "*", "l", "l", "*"])
        self.assertEqual(remaining_chars, 3)

    @patch('hangman.get_guess_word')
    @patch('hangman.get_guess_char')
    @patch('hangman.evaluate_word')
    def test_play_one_round_win(self, mock_evaluate_word, mock_get_guess_char, mock_get_guess_word):
        # Mock return values for win scenario
        mock_get_guess_word.return_value = "APPLE"
        mock_get_guess_char.side_effect = ["A", "P", "L", "E"]  # Simulate winning guesses
        mock_evaluate_word.return_value = (["A", "P", "P", "L", "E"], 0)  # All characters guessed

        # Call the function
        round_id = 1
        playerA = "Alice"
        playerB = "Bob"
        score = play_one_round(round_id, playerA, playerB)

        # Assertions for win
        self.assertEqual(score, [0, 1])  # Player B wins
        mock_get_guess_word.assert_called_once_with(playerA)
        mock_get_guess_char.assert_called_with(playerB, [])  # Initial guess with empty list
        mock_evaluate_word.assert_called_once()  # Evaluate word after all guesses

    @patch('hangman.get_guess_word')
    @patch('hangman.get_guess_char')
    @patch('hangman.evaluate_word')
    def test_play_one_round_loss(self, mock_evaluate_word, mock_get_guess_char, mock_get_guess_word):
        # Mock return values for loss scenario
        mock_get_guess_word.return_value = "APPLE"
        mock_get_guess_char.side_effect = ["X", "Y", "Z", "P", "Q", "R", "S", "T"]  # Simulate wrong guesses
        mock_evaluate_word.return_value = (["-", "-", "-", "A", "P", "P", "L", "E"], 4)  # 4 characters remaining

        # Call the function
        round_id = 1
        playerA = "Alice"
        playerB = "Bob"
        score = play_one_round(round_id, playerA, playerB)

        # Assertions for loss
        self.assertEqual(score, [1, 0])  # Player A wins
        mock_get_guess_word.assert_called_once_with(playerA)
        mock_get_guess_char.assert_called()  # Called multiple times for guesses
        mock_evaluate_word.assert_called()  # Evaluate word after all guesses

    @patch('builtins.input')  # Patch the built-in input function
    def test_play_another_round_yes(self, mock_input):
        # Mock user input to be 'Y' (yes)
        mock_input.return_value = "Y"

        # Call the function
        result = play_another_round()

        # Assert that the function returns True for 'Y' input
        self.assertTrue(result)

    @patch('builtins.input')  # Patch the built-in input function
    def test_play_another_round_no(self, mock_input):
        # Mock user input to be 'N' (no)
        mock_input.return_value = "N"

        # Call the function
        result = play_another_round()

        # Assert that the function returns False for 'N' input
        self.assertFalse(result)

    @patch('builtins.input')  # Patch the built-in input function
    def test_play_another_round_invalid(self, mock_input):
        # Mock user input to be invalid (anything other than 'Y' or 'N')
        mock_input.return_value = "maybe"

        # Call the function
        result = play_another_round()

        # Assert that the function returns False for invalid input
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
