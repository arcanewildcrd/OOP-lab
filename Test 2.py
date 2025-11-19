import logging
from typing import List, Dict, Tuple, Set



# Mixins for logging
class LoggerMixin:
    def log(self, com):
        logging.info(com)

# Custom exception
class DeliveryError(Exception):
    pass


# Classes
class Courier(LoggerMixin):
    def __init__(self, courier_id, name):
        self.courier_id = courier_id
        self.name = name

class Deliveries(LoggerMixin):
    def __init__(self, order_id, item, destination):
        self.order_id = order_id
        self.item = item
        self.destination = destination  # e.g., ("Hostel A", "Room 101")


class DeliveryEngine(LoggerMixin):
    def __init__(self):
        self.couriers: Dict[int, Courier] = {}          # Dict of objects
        self.deliveries: List[Deliveries] = []            # List of objects
        self.completed: Set[int] = set()                # Set for completed IDs

    def add_courier(self, courier: Courier):
        self.couriers[courier.courier_id] = courier
        self.log(f"Courier added: {courier.name}")

    def add_delivery(self, delivery: Deliveries):
        self.deliveries.append(delivery)
        self.log(f"Delivery added: {delivery.item} to {delivery.destination}")

    # Generator example to list pending deliveries
    def pending_deliveries(self):
        for delivery in self.deliveries:
            if delivery.order_id not in self.completed:
                yield delivery

    def complete_delivery(self, order_id):
        if order_id in self.completed:
            raise DeliveryError("Order already completed!")
        self.completed.add(order_id)
        self.log(f"Order {order_id} completed!")


    def incomplete_deliveries(self):
        return [d for d in self.deliveries if d.order_id not in self.completed]    


def simple_cli():
    engine = DeliveryEngine()
    
    # Sample data using dict, list, tuple, set
    engine.add_courier(Courier(1, "Toshinori Yagi"))
    engine.add_courier(Courier(2, "Yami Sukehiro"))
    engine.add_courier(Courier(3, "Todoroki Shoto"))
    engine.add_delivery(Deliveries(101, "Tokoyaki and Gyosa", ("Black Bulls Base", "Room 5")))
    engine.add_delivery(Deliveries(102, "Ramen and Yakisoba", ("UA Apartments", "Room 11")))
    engine.add_delivery(Deliveries(105, "Weekly Jump Comic: My Hero Academia Chapter 123", ("Black Gate Hostel", "Room 20")))
    
    print("\n*⚜️===Welcome to Santorini Campus Delivery CLI!===⚜️*")
    while True:
        print("\nOptions: [delivery_list] [courier] [complete] [incomplete] [exit]")
        choice = input("What do you want to do? ").strip().lower()
        
        if choice == "delivery_list":
            print("\nPending deliveries:")
            # Iterator/generator usage
            for d in engine.pending_deliveries():
                print(f"Order {d.order_id}: {d.item} to {d.destination}")

        elif choice == "courier":
            print("\nCouriers:")
            for cid, courier in engine.couriers.items():
                print(f"Courier {cid}: {courier.name}")        

        elif choice == "complete":
            try:
                oid = int(input("Enter order ID to complete: "))
                engine.complete_delivery(oid)
                print(f"Order {oid} Marked as complete.")
            except DeliveryError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Please enter a valid integer ID.") 

        elif choice == "incomplete":
            print("\nIncomplete deliveries:")
            incompletes = engine.incomplete_deliveries()
            for d in incompletes:
                print(f"Order {d.order_id}: {d.item} to {d.destination}")
            if not incompletes:
                print("All deliveries are complete!")        

        elif choice == "exit":
            print("Jaane 😃, arigatou gozaimasu! Thank you for using the  Santorini Delivery CLI 🍀.")
            break

        else:
            print("Unknown option. Please try again, senpai.")

if __name__ == "__main__":
    simple_cli()
