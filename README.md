# Tetris Game (俄罗斯方块)

A simple, classic Tetris game implementation in Python using pygame.

## Description

This is a fully functional Tetris game featuring:
- Classic Tetris gameplay with all 7 tetromino shapes
- Score tracking
- Smooth piece movement and rotation
- Line clearing mechanics
- Game over detection

## Requirements

- Python 3.6 or higher
- pygame 2.0.0 or higher

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd introduction-to-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install pygame directly:
```bash
pip install pygame
```

## How to Play

Run the game with:
```bash
python tetris.py
```

### Controls

- **LEFT/RIGHT Arrow Keys**: Move piece horizontally
- **DOWN Arrow Key**: Soft drop (move piece down faster)
- **UP Arrow Key**: Rotate piece clockwise
- **SPACE**: Hard drop (instantly drop piece to the bottom)

### Objective

- Arrange falling tetromino pieces to create complete horizontal lines
- Completed lines are cleared and you earn points
- The game ends when pieces stack up to the top of the screen
- Try to achieve the highest score possible!

## Scoring

- Each cleared line awards 100 points
- Clear multiple lines at once for maximum efficiency

## Game Features

- 7 unique tetromino shapes with different colors:
  - I-piece (Cyan): 4 blocks in a line
  - O-piece (Yellow): 2x2 square
  - T-piece (Magenta): T-shaped
  - L-piece (Orange): L-shaped
  - J-piece (Blue): Reverse L-shaped
  - S-piece (Green): S-shaped
  - Z-piece (Red): Z-shaped

- Automatic piece falling
- Collision detection
- Piece rotation
- Score display
- Game over screen

## License

This project maintains the original LICENSE.md from the repository.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Authors

See [AUTHORS](AUTHORS) file for contributors.
