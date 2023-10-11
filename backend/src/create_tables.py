from template.replace_me.data import ReplaceMeManager


async def run():
    await ReplaceMeManager.get_or_create_table()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
