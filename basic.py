print("hi")
#msc cruise 2025

known_user = ["matia","levi","clara"]
known_pasword = ["admin","code","france"]

print("login")

input_user = input("input your name:")
input_pasword = input("input your Pasword:")

for i in range(len(known_pasword)):
    if input_user == known_user[i]:

        if input_pasword == known_pasword[i]:
            print(f"your in {known_user[i]}")
        else:
            print("wrong password")


