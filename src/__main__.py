"""CLI for hardhat-ai."""
import sys, json, argparse
from .core import HardhatAi

def main():
    parser = argparse.ArgumentParser(description="HardHat AI — Safety Compliance Checker. Computer vision for construction site safety compliance.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = HardhatAi()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.process(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"hardhat-ai v0.1.0 — HardHat AI — Safety Compliance Checker. Computer vision for construction site safety compliance.")

if __name__ == "__main__":
    main()
