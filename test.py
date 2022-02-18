def generate_item(name, hours, length):
    return name + " " * (length - len(str(hours)) - len(name)) + str(hours)


print(generate_item("Mike", "10:11:12", 37))
print(generate_item("Mikeeeee", "10:1:12", 37))
print(type("hi"))