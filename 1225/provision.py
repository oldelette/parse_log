from dataclasses import dataclass, field, is_dataclass

def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__
        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                     new_obj = field_type(**value)
                     kwargs[name] = new_obj
            original_init(self, *args, **kwargs)
        cls.__init__ = __init__
        return cls
    return wrapper(args[0]) if args else wrapper

@dataclass
class Switch:
    vendor: str
    serial_number: str
    machine_name: str


#@dataclass
@nested_dataclass
class Provision:
    ip: str
    mac: str
    state: bool = field(default = False)
    switch:Switch = field(default_factory=dict)
    #switch:Switch
    #switch:Switch = field(repr = False, init = False)
    #switch:Switch = field(init = False)



#aa = Provision("192.168.1.68","ad:as",switch = {"","",""})
aa = Provision("192.168.1.68","ad:as")
print(aa)
print(type(aa))
#temp = {"vendor":"HP","serial_number":"1234","machine_name":"hp-5130"}
tt = Switch("HP","1234","hp-5130")
aa.switch = tt
print(aa.switch.vendor)
#bb = Provision("192.168.1.68","ad:as",temp)
#print(bb)
#print(bb.switch.vendor)
#aa.switch = {"HP","1234","hp-5130"}
#print(aa.switch)
