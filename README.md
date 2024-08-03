# Background Music Player

A simple PyQt5-based desktop music player that can play several tracks simultaneously. The player supports starting, stopping, and adjusting the volume of each track independently. Before starting you need copy your tracks to the folder named "background_sounds" near main.py or background_player.exe.

## Features

- Play several tracks simultaneously
- Start and stop each track independently
- Adjust the volume of each track independently

## Prerequisites

- Python 3.11
- PyQt5

## Exploitation

1. Download 'background_player.exe' file
2. Create folder 'background_sounds' near 'background_player.exe'
3. Copy your tracks inside the folder 'background_sounds'
4. Run 'background_player.exe'

## Installation

1. **Clone the repository:**
```sh
git clone https://github.com/egor-bondarev/Background-Player.git
cd Background-Player
```

2. **Create a virtual environment and activate it (optional but recommended):**
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install the required packages:**
```sh
pip install -r requirements.txt
```

4. **Create folder "background_sounds" and your tracks inside.**

5. **Run the application:**
```sh
python main.py
```