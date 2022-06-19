class Person:
    def __int__(self, addr, name, client):
        self.addr = addr
        self.client = client
        self.name = None

    def __set_name__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person({self.add}, {self.name})"
