from flask_teapot.teapot.teapot import TeapotState
from flask_teapot.db import get_db


teapot_state_names = {
    'ON': TeapotState.ON,
    'OFF': TeapotState.OFF,
    'BOILED_UP': TeapotState.BOILED_UP,
    'STOPPED': TeapotState.STOPPED
}


async def insert_into_temperature_by_time(
        temperature: float, 
        time_at: str
) -> None:
    db = await get_db()
    query = "INSERT INTO temperature_by_time (temperature, time)" \
        + f" VALUES ({temperature: .3f}, '{time_at}');"
    await db.execute(query)
    await db.commit()


async def insert_into_teapot_state(
        state: TeapotState,
        time_at: str
) -> None:
    db = await get_db()
    query = "INSERT INTO teapot_state (state, time)" \
        + f" VALUES ('{state.name}', '{time_at}');"
    await db.execute(query)
    await db.commit()


async def read_last_state() -> TeapotState:
    query = "SELECT state, time FROM teapot_state" \
        + " WHERE time = (SELECT MAX(time) FROM teapot_state);"
    db = await get_db()
    result = []
    async with db.execute(query) as cursor:
        async for row in cursor:
            result.append(row['state'])
            print(row['state'])
    if result:
        return teapot_state_names[result[0]]

    return None


async def read_last_temperature() -> float:
    query = "SELECT * FROM temperature_by_time" \
        + " WHERE time = (SELECT MAX(time) FROM temperature_by_time);"
    db = await get_db()
    result = []
    async with db.execute(query) as cursor:
        async for row in cursor:
            result.append(row['temperature'])
    if result:
        return result[0]

    return None
