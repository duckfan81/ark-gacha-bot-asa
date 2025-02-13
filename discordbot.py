import discord
import task_manager

def logger(message):
    with open("txt_files/logs.txt", 'a') as file:
        file.write(f"\n{message}")
    print(message)

def queue_write(message,queue):
    with open(f"txt_files/{queue}.txt", "a") as file:
        file.write(f"\n{message}")
    
async def embed_create(queue_type):
    embed = discord.Embed(title=f"{queue_type}")
    
    queue = getattr(task_manager.scheduler, queue_type, None)

    if queue is None or queue.is_empty():
        embed.add_field(name=queue_type, value="empty")
        return embed
    count = 0
    for i, entry in enumerate(queue.queue):
        if count >= 5:
            embed.add_field(
                name =f"...and {len(queue.queue) - 5} more tasks.",
                value = f"",
                inline= False
            )
            break
        if isinstance(queue, task_manager.priority_queue_prio):  # active queue is prio based 
            priority, exec_time, _, task = entry
            embed.add_field(
                name=f"Task {i+1}",
                value=f"Name: {task.name} | Priority: {priority} | Execution: NOW ",
                inline=False
            )
        else:  
            exec_time, _, priority, task = entry

            embed.add_field(
                name=f"Task {i+1}",
                value=f"Name: {task.name} | Priority: {priority} | Execution: <t:{int(exec_time)}:R>",
                inline=False
            )

        count += 1
    return embed
if __name__ =="__main__":
    pass
