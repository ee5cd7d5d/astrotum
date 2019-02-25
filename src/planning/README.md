 ### Install environment 
   
   ```sh
conda env create -f planning_env.yml
```
### Run Code
First, open conda environment
   ```sh
conda activate planning_env
```

Run code
   ```sh
python get_visible_passes.py --day DAY --month MONTH --year YEAR --max_mag MAX_MAG --silent_webpage --show_progressbar
```

