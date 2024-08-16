# ChessGPT

ChessGPT is a simple program that allows you to play chess against advanced AI models: ChatGPT-4o (the best model from OpenAI) and Claude 3.5 Sonnet (the best model from Anthropic). This is intended to showcase how AI models possess "narrow" intelligence and struggle to do non-writing tasks.

## Requirements

To use this software, you must have either an Anthropic API key or an OpenAI API key, depending on which AI opponent you choose to play against.

## Setup

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/YourUsername/ChessGPT.git
   cd ChessGPT
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the program:
   ```
   python chess_game.py
   ```

## How to Play

1. When you run the program, you'll be prompted to choose your AI opponent: ChatGPT or Claude.
2. After selecting your opponent, you'll be asked to enter the corresponding API key.
3. The chess board will appear, and you can start playing! Click on a piece to select it, then click on a valid square to move.
4. The AI will make its move automatically after you've made yours.

## Obtaining API Keys

### ChatGPT-4o (OpenAI)
To obtain an OpenAI API key:
1. Go to https://platform.openai.com/docs/quickstart](https://openai.com/index/openai-api/
2. Sign up or log in to your OpenAI account.
3. Navigate to the API section and create a new API key.

### Claude 3.5 Sonnet (Anthropic)
To obtain an Anthropic Claude API key:
1. Visit https://www.anthropic.com or https://www.anthropic.ai
2. Sign up for an account if you don't have one.
3. Once logged in, navigate to your account settings or API section.
4. Generate a new API key.

For more detailed instructions, visit:
https://www.nightfall.ai/ai-security-101/openai-api-key
or
https://www.nightfall.ai/ai-security-101/anthropic-claude-api-key

## How It Works

ChessGPT combines a graphical chess interface with AI language models to create a not-so-intelligent chess opponent. Here's a brief overview of its functioning:

1. **Chess Engine**: The program uses the `python-chess` library to manage the game state, validate moves, and check for game-ending conditions.

2. **GUI**: A graphical user interface is created using `tkinter`, allowing players to interact with the chess board visually.

3. **AI Integration**: When it's the AI's turn to move, the program does the following:
   - Converts the current board state to a FEN (Forsyth–Edwards Notation) string.
   - Generates a list of all legal moves.
   - Sends this information to the chosen AI model (ChatGPT or Claude) via their respective APIs.
   - The AI model, acting as a chess grandmaster, decides on the best move and returns it in standard chess notation.
   - The program then executes this move on the board.

4. **Move Validation**: All moves, both from the player and the AI, are validated by the chess engine to ensure they follow the rules of chess.

This approach allows the AI to make informed chess moves based on the current game state, creating a challenging and dynamic opponent for the player.
## Notes
- Keep your API keys confidential and never share them publicly.
- This program is for educational and entertainment purposes only.
- Enjoy your game of chess against some of the most advanced AI models available!

## Troubleshooting
If you encounter any issues, please check that:
- You have correctly installed all dependencies.
- Your API key is valid and correctly entered.
- You have a stable internet connection for API calls.

For any other problems, please open an issue in this GitHub repository.
