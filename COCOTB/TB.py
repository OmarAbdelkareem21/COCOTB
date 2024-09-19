import cocotb
from cocotb.clock import Clock
from cocotb.triggers import *
from cocotb.handle import Force, Release, Freeze, Deposit


async def driving_stimilus(dut):
    for i in range(16):
        await FallingEdge(dut.CLK)
        dut.RST.value= 0 if(i==0) else 1
        dut.EN.value= 1 if(i!=5) else 0
        dut.A.value= 9 
        dut.B.value= 1
        dut.ALU_FUN.value = 0 if i == 0 else (i - 1 if i != 5 else 3)
        await RisingEdge(dut.CLK)
        await ReadOnly()
        cocotb.log.info(f"rst: {dut.RST.value},en: {dut.EN.value},A: {dut.A.value}, B: {dut.B.value}, ALUFUN: {dut.ALU_FUN.value}, ALU_OUT: {dut.ALU_OUT.value}")


@cocotb.test()
async def tb_top(dut):
    cocotb.log.info(" STARTING SIMULATION ")
    CLK = Clock(dut.CLK, 10, units="ns")
    dut.RST.value = 0 
    await cocotb.start(CLK.start())
    await cocotb.start_soon(driving_stimilus(dut))
    cocotb.log.info(" After Driving Stimilus")