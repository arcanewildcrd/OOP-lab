# cli.py
from models import Hub, Parcel, Rider
from engine import load_hubs, load_parcels, load_riders, assign_parcels, rider_load_iterator
from typing import Dict, List
from exceptions import DataFormatError, DomainRuleError


def main():
    hubs_csv = "data/hubs.csv"
    parcels_csv = "data/parcels.csv"
    riders_csv = "data/riders.csv"

    print("\n=== ⚜️CourierLite Campus Delivery CLI⚜️ ===\n")

    hubs = load_hubs(hubs_csv)
    parcels = load_parcels(parcels_csv)
    riders = load_riders(riders_csv)

    print(f"Hubs loaded: {len(hubs.all())}")
    print(f"Parcels loaded: {len(parcels.all())}")
    print(f"Riders loaded: {len(riders.all())}")

    assignments, unassigned = assign_parcels(hubs, riders, parcels)
    print("\nParcel assignments per rider:")

    for rider_id in assignments:
        rider = riders.get(rider_id)
        rider_parcels = assignments[rider_id]
        parcel_ids = [p.get_id() for p in rider_parcels]
        total_load = sum(p.weight_kg for p in rider_parcels)
        first_three_dests = [p.destination for p in rider_parcels[:3]]
        print(f"\nRider {rider_id} ({rider.name})")
        print(f"  Parcels: {parcel_ids}")
        print(f"  Total load: {total_load} kg")
        print(f"  First 3 destinations: {first_three_dests}")

        print("  Step-by-step rider load:")
        for parcel_info in rider_load_iterator(rider, rider_parcels):
            print("    Parcel:", parcel_info)
    print("\nUnassigned parcels (couldn't fit):", sorted(list(unassigned)))

if __name__ == "__main__":
    main()
