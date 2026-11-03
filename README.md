# Datheon Python Programming Internship

This repository contains four Python command-line projects completed for the
internship program.

## Projects

| Folder | Project | Description |
| --- | --- | --- |
| `Internship/` | Hangman | Guess a randomly selected word, with input validation and a limited number of mistakes. |
| `Task_2/` | Stock portfolio tracker | Calculate holding and portfolio gain/loss and append summaries to a CSV file. Prices are entered manually; the program does not fetch live market data. |
| `Task_3/` | File organizer | Move recognized files into extension-based category folders in a selected directory. |
| `Task_4/` | Customer support chatbot | Match rules and regular expressions for business hours and common support topics, with a fallback and exit commands. |

## Requirements

- Python 3.9 or newer
- No third-party packages are required.

## Run

Run each script from its project folder:

```powershell
python Internship\hangman.py
python Task_2\portfolio.py
python Task_3\organizer.py "C:\path\to\directory"
python Task_4\chatbot.py
```

The organizer defaults to the current user's Downloads folder when no directory
is provided. It moves files, so test it on a copy or a small test directory first.
The chatbot's sample business hours and responses should be customized before
being used for a real business.
