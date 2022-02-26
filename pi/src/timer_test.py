import time

capture_time = time.time()

while True:
    t = time.time()
    print(t)

    

    if (t - capture_time) > 3:
        print("image captured")
        capture_time = time.time()
    
