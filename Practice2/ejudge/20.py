n = int(input())
documen = {}

for _ in range(n):
    cmd, *args = input()
    if cmd == "set":
        key, value = args
        documen[key] = value
    elif cmd == "get":
        key = args[0]
        if key in documen:
            print(documen[key])
        else:
            print(f"KE: no key {key} found in the document")