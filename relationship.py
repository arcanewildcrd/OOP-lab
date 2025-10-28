class RTracker:
    def __init__(self,partner):
        self.partner = partner
        self.__trust = 70
        self._mood = "nonchalant"
        self._vibe = 500
        
        
    def build_trust(self,amount):
        if amount <= 0:
            raise ValueError("LET'S KEEP IT POSITIVE")
        self._trust += amount
        
        
    def break_trust(self,amount):
        if amount <= 0:
            raise ValueError("For real!")
        self._trust -= amount
        
    def talk(self, duration):
        if duration <= 0:
            raise ValueError("Aight....aight!!!!")
        self._vibe += duration
        self._trust += 5
        self._mood  = 'Pretty aight i guess!'  
        
        
netflix = RTracker("Chill!")
netflix.build_trust(30)

netflix._trust = -242        