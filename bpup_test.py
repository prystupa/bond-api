import asyncio


from bond_api import BPUPSubscriptions, start_bpup


async def main(ip_address):
    """Example of library usage."""

    sub = BPUPSubscriptions()
    stop_bpup = await start_bpup(ip_address, sub)

    for i in range(500):
        print("BPUP is alive:", sub.alive)
        await asyncio.sleep(1)

    stop_bpup()


if __name__ == "__main__":
    print("Enter the device ip:")
    ip_address = input().strip()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(ip_address))
