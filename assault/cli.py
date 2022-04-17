import click
import sys
import json

from typing import TextIO
from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    output_file = None
    if json_file:
        try:
            output_file = open(json_file, "w")
        except:
            print(f"Unbale to open file {json_file}")
            sys.exit(1)
    total_time, request_dicts = assault(url, requests, concurrency)
    results = Results(total_time, request_dicts)
    display(results, output_file)


def display(results: Results, json_file: TextIO):
    if json_file:
        # Write to a file
        json.dump(
            {
                "Successful Requests": results.successful_requests(),
                "Slowest": results.slowest(),
                "Fastest": results.fastest(),
                "Total Time": results.total_time,
                "Requests Per Minute": results.requests_per_minute(),
                "Requests Per Second": results.requests_per_second(),
            },
            json_file,
        )
        json_file.close()
        print(".... Done!")
    else:
        # Print to screen
        print(".... Done!")
        print("--- Results ---")
        print(f"Successful Requests\t{results.successful_requests()}")
        print(f"Slowest            \t{results.slowest()}s")
        print(f"Fastest            \t{results.fastest()}s")
        print(f"Total time         \t{results.total_time}s")
        print(f"Requests Per Minute\t{results.requests_per_minute()}")
        print(f"Requests Per Second\t{results.requests_per_second()}")
