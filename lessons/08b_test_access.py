from access import UserContext, decide

alice = UserContext("alice", "viewer")
carol = UserContext("carol", "admin")

print(decide(alice, "preview_sheet", {"sheet": "HIL vatable"},"1"))
print(decide(alice, "preview_sheet", {"sheet": "Master carton BOM"},"2"))
bob = UserContext("bob", "packing")

print(decide(alice, "search_item", {"text": "screw", "sheet": "roofing screw"},"3"))
print(decide(bob, "search_item", {"text": "screw", "sheet": "roofing screw"},"3b"))
print(decide(carol, "preview_sheet", {"sheet": "Master carton BOM"},"4"))