"""Tests for HardhatAi."""
from src.core import HardhatAi
def test_init(): assert HardhatAi().get_stats()["ops"] == 0
def test_op(): c = HardhatAi(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = HardhatAi(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = HardhatAi(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = HardhatAi(); r = c.process(); assert r["service"] == "hardhat-ai"
