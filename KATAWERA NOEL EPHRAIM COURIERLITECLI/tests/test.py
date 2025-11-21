import unittest
from models import Hub, Parcel, Rider
from engine import HubRepo, ParcelRepo, RiderRepo, assign_parcels

class TestCourierLite(unittest.TestCase):

    def setUp(self):
        # Create sample hubs
        self.hub1 = Hub("H1", "Main Hub", "North Campus")
        self.hub2 = Hub("H2", "South Hub", "South Campus")

        # Create HubRepo and add hubs
        self.hubs = HubRepo()
        self.hubs.add(self.hub1)
        self.hubs.add(self.hub2)

        # Create sample riders
        self.rider1 = Rider("R01", "Hirokoshi", 10.0, "H1")
        self.rider2 = Rider("R02", "Tetsuya", 8.5, "H2")

        # Create RiderRepo and add riders
        self.riders = RiderRepo()
        self.riders.add(self.rider1)
        self.riders.add(self.rider2)

        # Create sample parcels
        self.parcel1 = Parcel("P1001","Kurosaki","EXPRESS","H1","Kawagai Hostel Room 101",2.5)
        self.parcel2 = Parcel("P1002","Saboten","NORMAL","H2","Shiketsu Hostel Room 202",1.2)
        self.parcel3 = Parcel("P1003","Ryuguji","EXPRESS","H1","Kagami Block Room 110",3.0)  # Heavy parcel

        # Create ParcelRepo and add parcels
        self.parcels = ParcelRepo()
        self.parcels.add(self.parcel1)
        self.parcels.add(self.parcel2)
        self.parcels.add(self.parcel3)

    def test_repo_counts(self):
        self.assertEqual(len(self.hubs.all()), 2)
        self.assertEqual(len(self.riders.all()), 2)
        self.assertEqual(len(self.parcels.all()), 3)

    def test_assign_parcels(self):
        assignments, unassigned = assign_parcels(self.hubs, self.riders, self.parcels)
        # Check that parcels are assigned respecting capacity and priority
        self.assertIn("P1001", [p.get_id() for p in assignments.get("R01", [])])
        self.assertIn("P1002", [p.get_id() for p in assignments.get("R02", [])])
        # The heavy parcel exceeds rider1 capacity; should be unassigned
        self.assertIn("P1003", unassigned)

if __name__ == "__main__":
    unittest.main()
