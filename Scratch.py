with open("story_data.txt", "r") as hello:
    hi = hello.read()
hi = hi.replace(chr(13) + chr(10), "&carriage;")
hi = hi.replace(chr(13), chr(7))
with open("new_story", "w") as hello:
    hello.write(hi)
