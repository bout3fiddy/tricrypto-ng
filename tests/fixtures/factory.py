import boa
import pytest


@pytest.fixture(scope="module")
def math_contract(deployer):
    with boa.env.prank(deployer):
        return boa.load("contracts/CurveCryptoMathOptimized3.vy")


@pytest.fixture(scope="module")
def gauge_interface():
    return boa.load_partial("contracts/LiquidityGauge.vy")


@pytest.fixture(scope="module")
def gauge_implementation(deployer, gauge_interface):
    with boa.env.prank(deployer):
        return gauge_interface.deploy_as_blueprint()


@pytest.fixture(scope="module")
def amm_interface():
    return boa.load_partial("contracts/CurveTricryptoOptimizedWETH.vy")


@pytest.fixture(scope="module")
def amm_implementation(deployer, amm_interface):
    with boa.env.prank(deployer):
        return amm_interface.deploy_as_blueprint()


@pytest.fixture(scope="module")
def hyperamm_interface():
    return boa.load_partial("contracts/CurveTricryptoHyperOptimizedWETH.vy")


@pytest.fixture(scope="module")
def hyperamm_implementation(deployer, hyperamm_interface):
    with boa.env.prank(deployer):
        return hyperamm_interface.deploy_as_blueprint()


@pytest.fixture(scope="module")
def views_contract(deployer, math_contract):
    with boa.env.prank(deployer):
        return boa.load(
            "contracts/CurveCryptoViews3Optimized.vy",
            math_contract,
        )


@pytest.fixture(scope="module")
def tricrypto_factory(
    deployer,
    fee_receiver,
    owner,
    amm_implementation,
    hyperamm_implementation,
    gauge_implementation,
    math_contract,
    views_contract,
    weth,
):
    with boa.env.prank(deployer):
        factory = boa.load(
            "contracts/CurveTricryptoFactory.vy",
            fee_receiver,
            owner,
            weth,
            math_contract,
        )

    with boa.env.prank(owner):
        factory.set_pool_implementation(amm_implementation, 0)
        factory.set_pool_implementation(hyperamm_implementation, 1)
        factory.set_gauge_implementation(gauge_implementation)
        factory.set_views_implementation(views_contract)

    return factory
