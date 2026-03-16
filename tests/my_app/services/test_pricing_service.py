from src.my_app.services.pricing_service import PricingService


def test_pricing_calculation():
    service = PricingService(base_rate=2.0)
    cost = service.calculate_cost(minutes=10)
    assert cost == 20.0


def test_pricing_negative_minutes_are_zero():
    service = PricingService(base_rate=2.0)
    cost = service.calculate_cost(minutes=-10)
    assert cost == 0.0
