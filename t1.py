from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep


def check_device(device: str) -> str:
    print(f"Checking {device}")
    sleep(2)  # Simulate waiting for a device
    return f"{device}: PASS"


def main():
    devices = ["device-A", "device-B", "device-C"]

    started = perf_counter()

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(check_device, devices))

    for result in results:
        print(result)

    print(f"Total time: {perf_counter() - started:.2f} seconds")


if __name__ == "__main__":
    main()
