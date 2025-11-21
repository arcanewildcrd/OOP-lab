# CourierLite Campus Delivery Engine

A simple Python 3.10+ project to simulate campus parcel delivery, featuring collections, object-oriented programming, generators, exceptions, structured logging, and a command-line interface.


## Features

- Loads hub, rider, and parcel data from CSV files
- Assigns parcels to riders by hub, weight, and priority (EXPRESS before NORMAL)
- Uses Python classes, mixins, and exceptions for clean code
- Provides a simple CLI for interaction
- Logs warnings and actions for debugging
- Easily extendable (test and bonus pickup types included)


## Project Structure

courierlite/
models.py
engine.py
cli.py
exceptions.py
logging.conf
README.md
data/
hubs.csv
parcels.csv
riders.csv
tests/



## Setup Instructions

1. **Install Python 3.10+**  
   Download from [python.org](https://www.python.org/downloads/) and add it to your system PATH.

2. **Project Structure**
   - Place all `.py` files and this `README.md` file in `courierlite/`
   - Add a `data` folder containing your `hubs.csv`, `parcels.csv`, and `riders.csv` files

3. **Run the CLI Program**
cd KATAWERA NOEL EPHRAIM COURIERLITECLI
python cli.py

If you get an error, try:
python3 cli.py (LINUX USERS)



## Example CSV files

**data/hubs.csv**
hub_id,hub_name,campus
H1,Main Hub,North Campus
H2,South Hub,South Campus


**data/parcels.csv**
parcel_id,recipient,priority,hub_id,destination,weight_kg
P1001,Kurosaki,EXPRESS,H1,Kawagai Hostel Room 101,2.5
P1002,Saboten,NORMAL,H2,Shiketsu Hostel Room 202,1.2
P1003,Ryuguji,EXPRESS,H1,Kagami Block Room 110,3.0


**data/riders.csv**
rider_id,name,max_load_kg,home_hub_id
R01,Hirokoshi,10.0,H1
R02,Tetsuya,8.5,H2




## How Parcel Assignment Works

- EXPRESS parcels are assigned before NORMAL.
- Each rider can only serve parcels for their home hub.
- No rider exceeds their own parcel weight limit.
- If multiple riders share a hub, round-robin is used (parcel gets assigned to the next free rider by rider_id).
- Parcels that cannot be assigned (no eligible rider with enough capacity at the hub) are listed as "unassigned".



## Troubleshooting

- If you get "file not found" errors, confirm folder and file names are correct.
- Make sure you’re running the program from the `courierlite` folder.
- If you see "python not found", install Python, or use `python3`.
- If edits don’t work in VS Code, make sure files are not read-only and Python is installed.



## Personalization & Bonus

- Create your own three pickup types in `models.py` for bonus marks.
- Tests can be added to the `tests/` folder.
- Logging can be customized in `logging.conf`.



## Author

Name:  KATAWERA NOEL EPHRAIM
REG NO: M24B13/013





