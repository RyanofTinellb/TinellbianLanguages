with open("story_data.txt", "r") as f:
    for line in f:
        for k in line:
            if ord(k) > 128:
                print(line)
