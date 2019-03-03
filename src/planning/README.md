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


Full command:
```sh
python get_visible_passes.py --day DAY --month MONTH --year YEAR --max_mag MAX_MAG --show_webpage --show_progressbar
```

If no arguments are passed, the current day is selected. The maximum magnitude is set to 5, the webpage is silent and no progressbar is shown:
```sh
python get_visible_passes.py 
```

### Functionality

The code downloads and processes the visible passes of the selected night (from midday of the selected day to midday of the next day). 

### Outputs



### Docker

Buid container

   ```docker build -t get_visible_passes . 
   ```
   
Run it

```docker run -v $(pwd):/ -ti get_visible_passes --day 02 --month 03 --year 2019```
