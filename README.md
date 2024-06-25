# Spaceship Shooting Game

Welcome to the **Spaceship Shooting Game**! This game is a thrilling arcade-style shooter where you control a spaceship, dodge asteroids, and shoot your way to a high score.

## Game Features

- **Control a spaceship** and shoot bullets to destroy incoming asteroids.
- **Collect power-ups** to gain extra lives.
- **Level progression**: The game gets progressively harder with each level.
- **Pause and resume** the game using the `P` key or on-screen button.
- **Toggle background music** using the `M` key or on-screen button.
- **High score tracking**: Your top three high scores are saved and displayed.

## Controls

- **Arrow keys**: Move the spaceship left and right.
- **Spacebar**: Shoot bullets.
- **P key**: Pause/Resume the game.
- **M key**: Mute/Unmute background music.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Malitha-Gunathilaka/Spaceship-Shooting-Game.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd Spaceship-Shooting-Game
    ```

3. **Install dependencies**:
    Make sure you have `pygame` installed. If not, you can install it using pip:
    ```bash
    pip install pygame
    ```

4. **Run the game**:
    ```bash
    python game.py
    ```

## Assets

Make sure to have the following images and sounds in the project directory:

- `spaceship.png`
- `asteroid.png`
- `bullet.png`
- `power_up.png`
- `background.png`
- `pause.png`
- `play.png`
- `sound_on.png`
- `sound_off.png`
- `start_button.png`
- `shoot.wav`
- `hit.wav`
- `lose_life.wav`
- `power_up.wav`
- `background.mp3`

## Code Overview

The game is written in Python using the Pygame library. Here’s a brief overview of the main components:

- **Initialization**: The game initializes Pygame, loads images and sounds, and sets up the display.
- **Game Loop**: The main game loop handles events, updates game state, and renders the game objects.
- **Collision Detection**: The game checks for collisions between bullets and asteroids, and between the spaceship and asteroids/power-ups.
- **User Interface**: The game displays score, lives, level, and provides buttons for pausing and muting.

## Developer

This game was developed by **Malitha Gunathilaka**.

- GitHub: [Malitha-Gunathilaka](https://github.com/Malitha-Gunathilaka)
- Email: malithavisada@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to the project by opening issues or submitting pull requests. Enjoy the game!
