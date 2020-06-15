"""CPU functionality."""

import sys

""" Implments single-byte addressable guarded memory """
class Memory():
  def __init__(self, size):
    self.internal_memory = [0] * size
    self.size = size

  def read_byte(self, address):
    if address < 0 or address > self.size - 1:
      raise ReferenceError("Out of bounds memory reference.")
    return self.internal_memory[address]

  def write_byte(self, address, data):
    if address < 0 or address > self.size - 1:
      raise ReferenceError("Out of bounds memory reference.")
    try:
      real_byte = int(data)
      if real_byte < 0 or real_byte > 255:
        raise Exception()
      self.internal_memory[address] = real_byte
    except:
      raise TypeError("Data must be a number from 0-255.")

""" Virtual CPU """
class CPU:
  def __init__(self):
    # spec limits memory to 256 bytes
    self.ram = Memory(256)
    
    # this table maps an instruction number to its implementation
    self.instruction_set = {
      0x01: self.HLT,
      0x47: self.PRN,
      0x82: self.LDI,
    }
    
    # general purpose registers
    self.R0 = 0
    self.R1 = 0
    self.R2 = 0
    self.R3 = 0
    self.R4 = 0
    self.R5 = 0
    self.R6 = 0
    self.R7 = 0

    # special purpose registers
    self.PC = 0 # program counter (aka instruction pointer)
    self.IR = 0 # instruction register (the currently executing instruction)

    # flags register (each bit is a flag, up to 8)
    self.FLAGS = 0x00

    # list of flags with their position within the FLAGS register
    self.FLAG_RUNNING = 0x01 # then 2, 4, 8, ... F0

  def load(self):
    """Load a program into memory."""

    address = 0

    # For now, we've just hardcoded a program:

    program = [
      # From print8.ls8
      0b10000010, # LDI R0,8
      0b00000000,
      0b00001000,
      0b01000111, # PRN R0
      0b00000000,
      0b00000001, # HLT
    ]

    for instruction in program:
      self.ram.write_byte(address, instruction)
      address += 1

  def alu(self, op, reg_a, reg_b):
    pass
      # """ALU operations."""

      # if op == "ADD":
      #     self.reg[reg_a] += self.reg[reg_b]
      # #elif op == "SUB": etc
      # else:
      #     raise Exception("Unsupported ALU operation")

  def trace(self):
    """
    Handy function to print out the CPU state. You might want to call this
    from run() if you need help debugging.
    """
    pass

    # print(f"TRACE: %02X | %02X %02X %02X |" % (
    #   self.pc,
    #   #self.fl,
    #   #self.ie,
    #   self.ram_read(self.pc),
    #   self.ram_read(self.pc + 1),
    #   self.ram_read(self.pc + 2)), end='')

    # for i in range(8):
    #     print(" %02X" % self.reg[i], end='')

    # print()

  def run(self):
    self.FLAGS |= self.FLAG_RUNNING # CPU ON
    
    while self.FLAGS & self.FLAG_RUNNING == True: # while CPU ON
      self.IR = self.ram.read_byte(self.PC) # load instruction

      try:
        self.instruction_set[self.IR]() # execute
      except IndexError:
        print(f"Unknown instruction {self.IR} at address {self.PC}")

  # Implementation of CPU Instructions

  def HLT(self):
    self.FLAGS &= ~self.FLAG_RUNNING
    self.PC += 1

  def LDI(self):
    reg_num = self.PC + 1
    reg_val = self.PC + 2
    self.set_gp_register(reg_num, reg_val)
    self.PC += 3

  def PRN(self):
    print(self.PC + 1)
    self.PC += 2

  # Helpers

  def set_gp_register(self, reg_num, reg_val):
    if reg_num < 0 or reg_num > 7:
      raise Exception(f"Illegal Register R{reg_num}")

    if reg_num == 0:
      self.R0 = reg_val
    elif reg_num == 1:
      self.R1 = reg_val
    elif reg_num == 2:
      self.R2 = reg_val
    elif reg_num == 3:
      self.R3 = reg_val
    elif reg_num == 4:
      self.R4 = reg_val
    elif reg_num == 5:
      self.R5 = reg_val
    elif reg_num == 6:
      self.R6 = reg_val
    elif reg_num == 7:
      self.R7 = reg_val
    