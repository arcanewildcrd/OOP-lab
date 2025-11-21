# engine.py



import csv
import logging
from typing import List, Dict, Set
from models import Hub, Parcel, Rider
from exceptions import DataFormatError, DomainRuleError

logging.basicConfig(level=logging.INFO)

# --- Repositories (using dict for fast lookup) ---

class HubRepo:
    def __init__(self):
        self.hubs: Dict[str, Hub] = {}

    def add(self, hub: Hub):
        self.hubs[hub.get_id()] = hub

    def get(self, hub_id: str):
        return self.hubs.get(hub_id)

    def all(self) -> List[Hub]:
        return list(self.hubs.values())

    def exists(self, hub_id: str) -> bool:
        return hub_id in self.hubs

    def ids(self) -> Set[str]:
        return set(self.hubs.keys())

class ParcelRepo:
    def __init__(self):
        self.parcels: Dict[str, Parcel] = {}

    def add(self, parcel: Parcel):
        self.parcels[parcel.get_id()] = parcel

    def get(self, parcel_id: str):
        return self.parcels.get(parcel_id)

    def all(self) -> List[Parcel]:
        return list(self.parcels.values())

    def exists(self, parcel_id: str) -> bool:
        return parcel_id in self.parcels

    def ids(self) -> Set[str]:
        return set(self.parcels.keys())

class RiderRepo:
    def __init__(self):
        self.riders: Dict[str, Rider] = {}

    def add(self, rider: Rider):
        self.riders[rider.get_id()] = rider

    def get(self, rider_id: str):
        return self.riders.get(rider_id)

    def all(self) -> List[Rider]:
        return list(self.riders.values())

    def exists(self, rider_id: str) -> bool:
        return rider_id in self.riders

    def ids(self) -> Set[str]:
        return set(self.riders.keys())

# --- CSV Loader Functions ---

def load_hubs(path: str) -> HubRepo:
    repo = HubRepo()
    try:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    hub = Hub(
                        hub_id=row['hub_id'],
                        hub_name=row['hub_name'],
                        campus=row['campus']
                    )
                    repo.add(hub)
                except Exception as e:
                    logging.warning(f"Skipping hub row: {row}. Reason: {e}")
    except Exception as e:
        logging.error(f"Failed to open hubs file: {e}")
    return repo

def load_parcels(path: str) -> ParcelRepo:
    repo = ParcelRepo()
    try:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    parcel = Parcel(
                        parcel_id=row['parcel_id'],
                        recipient=row['recipient'],
                        priority=row['priority'],
                        hub_id=row['hub_id'],
                        destination=row['destination'],
                        weight_kg=float(row['weight_kg'])
                    )
                    repo.add(parcel)
                except Exception as e:
                    logging.warning(f"Skipping parcel row: {row}. Reason: {e}")
    except Exception as e:
        logging.error(f"Failed to open parcels file: {e}")
    return repo

def load_riders(path: str) -> RiderRepo:
    repo = RiderRepo()
    try:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    rider = Rider(
                        rider_id=row['rider_id'],
                        name=row['name'],
                        max_load_kg=float(row['max_load_kg']),
                        home_hub_id=row['home_hub_id']
                    )
                    repo.add(rider)
                except Exception as e:
                    logging.warning(f"Skipping rider row: {row}. Reason: {e}")
    except Exception as e:
        logging.error(f"Failed to open riders file: {e}")
    return repo

# --- Assign parcels to riders ---
def assign_parcels(hubs: HubRepo, riders: RiderRepo, parcels: ParcelRepo):
    assignments: Dict[str, List[Parcel]] = {}      # rider_id => list of parcels
    unassigned: Set[str] = set()                   # unassigned parcel_ids

    # Group riders by hub
    hub_riders: Dict[str, List[Rider]] = {}
    for rider in riders.all():
        hub_riders.setdefault(rider.home_hub_id, []).append(rider)

    # Prepare parcels by priority
    express = [p for p in parcels.all() if p.priority == 'EXPRESS']
    normal  = [p for p in parcels.all() if p.priority == 'NORMAL']
    all_parcels = express + normal

    # Track loads per rider
    rider_load: Dict[str, float] = {r.get_id(): 0 for r in riders.all()}

    # Round-robin assignment within each hub, by ascending rider_id
    for parcel in all_parcels:
        riders_at_hub = sorted(hub_riders.get(parcel.hub_id, []), key=lambda r: r.get_id())
        assigned = False
        for rider in riders_at_hub:
            rid = rider.get_id()
            if rider_load[rid] + parcel.weight_kg <= rider.max_load_kg:
                assignments.setdefault(rid, []).append(parcel)
                rider_load[rid] += parcel.weight_kg
                assigned = True
                break
        if not assigned:
            unassigned.add(parcel.get_id())
    return assignments, unassigned

# --- Example iterator for a rider's load ---
def rider_load_iterator(rider: Rider, parcels: List[Parcel]):
    total = 0
    for parcel in parcels:
        total += parcel.weight_kg
        yield parcel.get_id(), parcel.weight_kg, total
