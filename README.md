# Nand2Tetris I – Capstone: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCCNT301), School of Engineering & Technology, K.R. Mangalam University
**Student:** Arpit Patni
**Roll No.:** 2501730111
**Faculty:** Dr. Neetu Chauhan
**Personal number K:** 11 (last two digits of the roll number)

## About the project

The Hack computer is built and used to show a black box on the screen while a key is pressed. The project has three parts:

| Part | What was done |
|------|---------------|
| A | `CPU.hdl`, `Memory.hdl` and `Computer.hdl`, checked with the official test files |
| B | A two-pass assembler in Python (`assembler.py`) that turns `.asm` files into `.hack` files |
| C | `Box.asm`, a Hack assembly program that draws the box while a key is held |

## My values (K = 11)

| Item | Value |
|------|-------|
| Box start row | 11 |
| Box height | 20 rows |
| Box width | 16 × ((11 mod 4) + 1) = 64 pixels (4 words) |
| Start address | SCREEN + 32 × 11 = 16384 + 352 = 16736 |
| Extra assembler feature | K mod 3 = 2, so the assembler prints a warning if the same label is written twice |
| Box.hack size | 52 instructions |

## Folder structure

```
capstone/
├── hdl/
│   ├── CPU.hdl
│   ├── Memory.hdl
│   └── Computer.hdl
├── screenshots/            # test results, assembler runs, comparisons, box screenshots
├── assembler.py            # Part B: two-pass Python assembler
├── Add.asm / Add.hack
├── Max.asm / Max.hack
├── Rect.asm / Rect.hack
├── Pong.asm / Pong.hack
├── DuplicateTest.asm       # test file for the duplicate-label warning
├── Box.asm / Box.hack      # Part C: keyboard-controlled box
└── (report PDF)
```

## Part A – Test results

| Test file | Chip | Result |
|-----------|------|--------|
| CPU.tst | CPU | Passed |
| Memory.tst | Memory | Passed |
| ComputerAdd.tst | Computer | Passed |
| ComputerMax.tst | Computer | Passed |
| ComputerRect.tst | Computer | Passed |

## Part B – Assembler

The first pass removes comments and blank lines and stores each label's ROM address in the symbol table. The second pass converts every A-instruction and C-instruction into 16-bit binary. Variables get RAM addresses starting at 16, and the predefined symbols (SP, LCL, ARG, THIS, THAT, SCREEN, KBD, R0–R15) are supported.

Invalid instructions are reported with their source line number. Writing the same label twice prints a warning with the label name and line number, keeps the first definition and carries on.

### How to run

```bash
cd capstone
python3 assembler.py Box.asm
```

This creates `Box.hack` next to the source file. The same command works for `Add.asm`, `Max.asm`, `Rect.asm` and `Pong.asm`.

### Programs tested

| Program | Instructions generated |
|---------|------------------------|
| Add.asm | 6 |
| Max.asm | 16 |
| Rect.asm | 25 |
| Pong.asm | 27483 |
| Box.asm | 52 |

## Part C – Box program

`Box.asm` reads the keyboard word (KBD). If a key is pressed it sets the colour to -1 (black); otherwise it uses 0 (white). Starting at address 16736 it writes the colour into 4 consecutive words for each of 20 rows, then skips 28 words to reach the next screen row. After the last row it checks the keyboard again.

| Register | Use |
|----------|-----|
| R12 | Words left in the current row |
| R13 | Current screen address |
| R14 | Rows left |
| R15 | Colour (-1 or 0) |

`Box.hack` was produced with the custom assembler from Part B, not the official one, and run in the Nand2Tetris CPU Emulator.

## How to test the box

1. Open the Nand2Tetris CPU Emulator.
2. Load `Box.hack` into the ROM.
3. Enable the keyboard and run the program.
4. Hold any key to see the black box at the left edge of the screen; release the key and it disappears.
