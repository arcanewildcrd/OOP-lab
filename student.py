class Phone:
    def __init__(self, brand, storage, Phone, number, camera, song, artist):
        self.brand = brand
        self.storage = storage
        self.phone = Phone
        self.number = number
        self.camera = camera
        self.song = song
        self.artist = artist
        
        
    def call(self, number):
        print(f'Calling {number} from {self.brand}!!')
        
    def take_photo(self):
        print(f'Snap taken by {self.brand} camera!')
        
    def music(self, song, artist):
        print(f'Now playing {song} by {artist}')   
        

Phone.number('0781782071')
Phone.take_photo('')
Phone.music('Man of the Year')




