# models.py


from typing import Tuple

# A mixin for anything that has an ID
class HasID:
    def get_id(self):
        return str(self.id)

# A mixin to print objects as a row/tuple
class RowPrintable:
    def to_row(self) :
        return tuple(vars(self).values())

# The hub class
class Hub(HasID, RowPrintable):
    def __init__(self, hub_id, hub_name, campus):
        self.id = hub_id  # Unique hub ID
        self.hub_name = hub_name
        self.campus = campus

    def __repr__(self):
        return f"Hub({self.id}, {self.hub_name}, {self.campus})"

# The parcel class
class Parcel(HasID, RowPrintable):
    def __init__(self, parcel_id, recipient, priority, hub_id, destination, weight_kg):
        self.id = parcel_id  # Unique parcel ID
        self.recipient = recipient
        self.priority = priority.upper()  # EXPRESS or NORMAL
        self.hub_id = hub_id
        self.destination = destination
        self.weight_kg = (weight_kg)
    def __repr__(self):
        return f"Parcel({self.id}, {self.recipient}, {self.priority}, {self.hub_id}, {self.destination}, {self.weight_kg})"

# The rider class
class Rider(HasID, RowPrintable):
    def __init__(self, rider_id, name, max_load_kg, home_hub_id):
        self.id = rider_id
        self.name = name
        self.max_load_kg = (max_load_kg)
        self.home_hub_id = home_hub_id
    def __repr__(self):
        return f"Rider({self.id}, {self.name}, {self.max_load_kg}, {self.home_hub_id})"

# --- Bonus: Pickup points, personalizable! ---
class PickupPoint(HasID, RowPrintable):
    def __init__(self, pickup_id, label, hub_id, base_priority_bias):
        self.id = pickup_id
        self.label = label
        self.hub_id = hub_id
        self.base_priority_bias = base_priority_bias
    def __repr__(self):
        return f"PickupPoint({self.id}, {self.label}, {self.hub_id}, {self.base_priority_bias})"

#pickup point subclasses
class DavyJonesLocker(PickupPoint):
    def __init__(self, pickup_id, hub_id):
        super().__init__(pickup_id, 'DavyJonesLocker', hub_id, 1)

class ShiraiRyu(PickupPoint):
    def __init__(self, pickup_id: str, hub_id: str):
        super().__init__(pickup_id, 'ShiraiRyu', hub_id, 0)

class HuecoMundo(PickupPoint):
    def __init__(self, pickup_id: str, hub_id: str):
        super().__init__(pickup_id, 'HuecoMundo', hub_id, -1)


    