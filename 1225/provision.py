from dataclasses import dataclass, field

@dataclass
class Switch:
    vendor: str
    serial_number: str
    machine_name: str


@dataclass
class Provision:
    ip: str
    mac: str
    state: bool = field(default = False)
    #switch:Switch = field(default_factory=dict)
    #switch:Switch
    switch:Switch = field(repr = False, init = False)
    #switch:Switch = field(init = False)



aa = Provision("192.168.1.68","ad:as")
print(aa)
#print(aa.switch)
#temp = {"vendor":"HP","serial_number":"1234","machine_name":"hp-5130"}
tt = Switch("HP","1234","hp-5130")
aa.switch = tt
print(aa.switch.vendor)
#bb = Provision("192.168.1.68","ad:as",temp)
#print(bb)
#print(bb.switch.vendor)
#aa.switch = {"HP","1234","hp-5130"}
#print(aa.switch)
