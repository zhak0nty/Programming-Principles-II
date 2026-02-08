print(10 > 9)
print(10 == 9)
print(10 < 9)   
x = "Hello"
y = 15

print(". ")

print(bool(x))
print(bool(y))

print(". ")

#expect 
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

print(". ")

class myclass():
    def __len__(self):
        return 0

myobj = myclass()
print(bool(myobj))