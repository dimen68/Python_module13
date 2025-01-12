# Задача "Асинхронные силачи"

import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for i in range(1,6):
        await asyncio.sleep(1/power)
        print(f'Силач {name} поднял {i} шар')
    print(f'Силач {name} закончил соревнования')

async def start_tournament():
    print('Соревнование началось')
    task_1 = asyncio.create_task(start_strongman('Дима', 3))
    task_2 = asyncio.create_task(start_strongman('Андрей', 4))
    task_3 = asyncio.create_task(start_strongman('Платон', 5))
    await task_1
    await task_2
    await task_3
    print('Соревнование закончилось')


if __name__ == '__main__':
    asyncio.run(start_tournament())