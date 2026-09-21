# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    # Load 20 into the counter
    dut.ui_in.value = 1
    dut.uio_in.value = 20

    # Wait for one clock cycle to load the value
    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")

    # Disable load and enable the outputs
    dut.ui_in.value = 2

    # Wait for one clock cycle
    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")

    # Check that the counter incremented from 20 to 21
    assert dut.uio_out.value == 21

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

    await ClockCycles(dut.clk, 1)
    await Timer(1, unit="ns")
    assert dut.uio_out.value == 22

    # Check that all bidirectional outputs are enabled
    assert dut.uio_oe.value == 0xFF

    # Disable the outputs
    dut.ui_in.value = 0
    await Timer(1, unit="ns")

    # Check that all bidirectional outputs are disabled
    assert dut.uio_oe.value == 0x00