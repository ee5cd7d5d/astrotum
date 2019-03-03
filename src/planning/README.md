### Requirements

- Anaconda
- Chrome/Chromium

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

### Docker

Buid container

   ```docker build -t get_visible_passes . 
   ```
   
Run it

```docker run -v $(pwd):/ -ti get_visible_passes --day 02 --month 03 --year 2019```
