class Profile: 
    def __init__(self, name, favourite_language, hobby, tech_stack, github_username, fun_fact):
        self.name = name
        self.favourite_language = favourite_language
        self.hobby = hobby
        self.tech_stack = tech_stack
        self.github_username = github_username
        self.fun_fact = fun_fact

    def introduce(self):
        print(f"Hey, I'm {self.name}, I love {self.favourite_language} and my hobby is {self.hobby}.")
        print(f"Fun_fact: {self.fun_fact}")
        
    def show_stack(self):
        print(f"\n {self.name}'s Tech Stack!")
        print("")
        for tech in self.tech_stack:
            print(f"-{tech}")
        print("")
        
    def github_link(self):
        return f"https://github.com/{self.github_username}"

# Instantiate and use the Profile class outside the class definition
my_profile = Profile(
    name = "Katawera Noel Ephraim",
    favourite_language = "Python",
    hobby = "Anime",
    tech_stack = ["Python", "MySQL", "Javascript", "HTML/CSS"],
    github_username = "arcanewildcrd",
    fun_fact = "I am unpredictible"
)

print("\n====MY DEVELOPER PROFILE====\n")
my_profile.introduce()
my_profile.show_stack()
print(f"\nCheck out my GitHub: {my_profile.github_link()}")
print("\n===========================")

