# work

This project is going to be a config-to-BOM project. It is the first step in a multi-step effort to help fix the logistics bottleneck in a simulated scenario.

## Run

From the project directory, run:

```bash
python3 main.py config.json
```

The starter configuration is in `config.json`. To save the generated BOM to a file:

```bash
python3 main.py config.json --output bom.json
```