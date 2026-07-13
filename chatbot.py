import pwd


while True:
    user = input("You: ")

    if user.lower() == "bye":
        print("Bot: Goodbye!")
        break

    print("Bot: You said:", user)
    pwd.getpwuid(os.getuid())