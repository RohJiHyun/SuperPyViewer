class Env():
    this = None
    def __init__(self):
        pass

    def get_instance(self):
        if Env.this:
            return Env.this 
        else : 
            Env.this = Env()
            return Env.this






    

