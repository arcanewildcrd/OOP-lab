#visit
class Resident:
    def __init__(self, name, room_no):
        self.name = name
        self.room_no = room_no


class Visitor:
    def __init__(self, name, id_no):
        self.name = name
        self.id_no = id_no
        
        
class Hostel:
    def __init__(self, name):
        self.name = name
        self.visits = []
        
    def record_visit(self, visitor:Visitor, resident:Resident):
        entry = visitor.name + 'is visiting' + resident.name + 'in room' + resident.room_no
        self.visits.append(entry)
        
        
    def show_visits(self):
        print(f'Visit log for {self.name} Hostel')
        
        if not self.visits:
            print('No visits recorded yet')
            
        for visits in self.visits:
            print('-'+ visits)                   
            
            
#demo

hostel = Hostel('BlackGate')

resident1 = Resident('Raijin', '012')
resident2 = Resident('Satoyu', '123')

visitor1 = Visitor('Tsukasa', 'V223')             
visitor2 = Visitor('Todoroki', 'E245')
visitor3 = Visitor('Fujin', 'D567')
visitor4 = Visitor('Fujio', 'O242')

hostel.record_visit(visitor1, resident1)
hostel.record_visit(visitor2, resident2)
hostel.record_visit(visitor3, resident2)
hostel.record_visit(visitor4, resident1)