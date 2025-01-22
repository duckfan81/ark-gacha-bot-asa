def logger(message):
    with open("txt_files/logs.txt", 'a') as file:
        file.write(f"\n{message}")
    print(message)

def queue_write(message,queue):
    with open(f"txt_files/{queue}.txt", "a") as file:
        file.write(f"\n{message}")
    
if __name__ =="__main__":
    pass
