#################################################################
# Project 3: Pipeline Datapath Simulator (Teh Zi Cong Nicholas) #
#################################################################

import copy

# OPCODE for I-format instruction
opcodes = {4:"beq", 5:"bne", 35:"lw", 43:"sw"}

# FUNC for R-format instruction
funcs = {32:"add", 34:"sub", 36:"and", 37:"or", 42:"slt"}

# Masks to extract a specific part
mask = {"opcode":0b11111100000000000000000000000000,
          "src1":0b00000011111000000000000000000000,
          "src2":0b00000000000111110000000000000000,
          "dest":0b00000000000000001111100000000000,
          "func":0b00000000000000000000000000111111,
          "offset":0b00000000000000001111111111111111}

Main_Mem = []
# Initialise Main_Mem
put_i = 0
for i in range(0x0, 0x7FF+1):
    if put_i > 0xFF:
        put_i = 0
    
    Main_Mem.append(put_i)
    put_i += 1

Regs = [0] * 32
# Intialise Registers
for i in range(32):
    if i == 0:
        Regs[i] = 0x0
    else:
        Regs[i] = 0x100 + i

def IF_stage(instruction, address):
    # Fetch instruction and put it into WRITE version of IF/ID pipeline register
    IF_ID_write.instruction = instruction
    IF_ID_write.IncrPC = address

def ID_stage():
    # Read instruction from READ version of IF/ID pipeline register
    # Decoding and register fetching
    # Write values to the WRITE version of ID/EX pipline register
    ID_EX_write.disassemble(IF_ID_read.instruction, IF_ID_read.IncrPC)

def EX_stage():
    # Perform requested instruction on operands read out of READ version of ID/EX pipeline register
    # Write appropriate values to the WRITE version of EX/MEM pipeline register
    EX_MEM_write.run(ID_EX_read)

def MEM_stage():
    MEM_WB_write.mm(EX_MEM_read)

def WB_stage():
    # Write to the registers based on information read out of the READ version of MEM_WB
    MEM_WB_read.wb()

def Print_out_everything():
    print("#############################################################################")
    print("Registers: ")
    for i in range(32):
        print("$" + str(i) + ": " + str(hex(Regs[i])))

    print()
    # IF/ID_Write (written to by the IF stage)
    print("IF/ID_Write (written to by the IF stage)")
    if IF_ID_write.instruction == 0:
        print("Inst = 0x00000000")
    else:
        print("Inst = " + hex(IF_ID_write.instruction) + "         IncrPC = " + hex(IF_ID_write.IncrPC))

    print()
        
    # IF/ID_Read (read by the ID stage)
    print("IF/ID_Read (read by the ID stage)")
    if IF_ID_read.instruction == 0:
        print("Inst = 0x00000000")
    else:
        print("Inst = " + hex(IF_ID_read.instruction) + "         IncrPC = " + hex(IF_ID_read.IncrPC))

    print()

    # ID/EX_Write (written to by the ID stage)
    print("ID/EX_Write (written to by the ID stage)")
    if ID_EX_write.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: RegDst = " + str(ID_EX_write.RegDst)
              + ", ALUSrc = " + str(ID_EX_write.ALUSrc)
              + ", ALUOp = " + str(bin(ID_EX_write.ALUOp))
              + ", MemRead = " + str(ID_EX_write.MemRead)
              + ", MemWrite = " + str(ID_EX_write.MemWrite))
        print("         Branch = " + str(ID_EX_write.Branch)
              + ", MemToReg = " + str(ID_EX_write.MemToReg)
              + ", RegWrite = " + str(ID_EX_write.RegWrite))
        
        print()

        print("Incr PC = " + str(hex(ID_EX_write.IncrPC))
              + ", ReadReg1Value = " + str(hex(ID_EX_write.ReadReg1Value))
              + ", ReadReg2Value = " + str(hex(ID_EX_write.ReadReg2Value)))
        print("SEOffset = " + str(hex(((abs(ID_EX_write.SEOffset) ^ 0xFFFF) + 1) & 0xFFFF))
              + ", WriteReg_20_16 = " + str(ID_EX_write.WriteReg_20_16)
              + ", WriteReg_15_11 = " + str(ID_EX_write.WriteReg_15_11)
              + ", Function = " + str(hex(ID_EX_write.Function)))

    print()

    # ID/EX_Read (read by the EX stage)
    print("ID/EX_Read (read by the EX stage)")
    if ID_EX_read.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: RegDst = " + str(ID_EX_read.RegDst)
              + ", ALUSrc = " + str(ID_EX_read.ALUSrc)
              + ", ALUOp = " + str(bin(ID_EX_read.ALUOp))
              + ", MemRead = " + str(ID_EX_read.MemRead)
              + ", MemWrite = " + str(ID_EX_read.MemWrite))
        print("         Branch = " + str(ID_EX_read.Branch)
              + ", MemToReg = " + str(ID_EX_read.MemToReg)
              + ", RegWrite = " + str(ID_EX_read.RegWrite))
        
        print()

        print("Incr PC = " + str(hex(ID_EX_read.IncrPC))
              + ", ReadReg1Value = " + str(hex(ID_EX_read.ReadReg1Value))
              + ", ReadReg2Value = " + str(hex(ID_EX_read.ReadReg2Value)))
        print("SEOffset = " + str(hex(((abs(ID_EX_read.SEOffset) ^ 0xFFFF) + 1) & 0xFFFF))
              + ", WriteReg_20_16 = " + str(ID_EX_read.WriteReg_20_16)
              + ", WriteReg_15_11 = " + str(ID_EX_read.WriteReg_15_11)
              + ", Function = " + str(hex(ID_EX_read.Function)))

    print()

    # EX/MEM_Write (written to by the EX stage)
    print("EX/MEM_Write (written to by the EX stage)")
    if EX_MEM_write.obj == None or EX_MEM_write.obj.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: MemRead = " + str(EX_MEM_write.MemRead)
              + ", MemWrite = " + str(EX_MEM_write.MemWrite)
              + ", Branch = " + str(EX_MEM_write.Branch)
              + ", MemToReg = " + str(EX_MEM_write.MemToReg)
              + ", RegWrite = " + str(EX_MEM_write.RegWrite))
        print("         CalcBTA = " + str(EX_MEM_write.CalcBTA)
              + ", Zero = " + str(EX_MEM_write.Zero)
              + ", ALUResult = " + str(hex(EX_MEM_write.ALUResult)))
        
        print()

        print("SWValue = " + str(hex(EX_MEM_write.SWValue))
              + ", WriteRegNum = " + str(EX_MEM_write.WriteRegNum))

    print()

    # EX/MEM_Read (read by the MEM stage)
    print("EX/MEM_Read (read by the MEM stage)")
    if EX_MEM_read.obj == None or EX_MEM_read.obj.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: MemRead = " + str(EX_MEM_read.MemRead)
              + ", MemWrite = " + str(EX_MEM_read.MemWrite)
              + ", Branch = " + str(EX_MEM_read.Branch)
              + ", MemToReg = " + str(EX_MEM_read.MemToReg)
              + ", RegWrite = " + str(EX_MEM_read.RegWrite))
        print("         CalcBTA = " + str(EX_MEM_read.CalcBTA)
              + ", Zero = " + str(EX_MEM_read.Zero)
              + ", ALUResult = " + str(hex(EX_MEM_read.ALUResult)))
        
        print()

        print("SWValue = " + str(hex(EX_MEM_read.SWValue))
              + ", WriteRegNum = " + str(EX_MEM_read.WriteRegNum))

    print()

    # MEM/WB_Write (written to by the MEM stage)
    print("MEM/WB_Write (written to by the MEM stage)")
    if MEM_WB_write.obj == None or MEM_WB_write.obj.obj == None or MEM_WB_write.obj.obj.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: MemToReg = " + str(MEM_WB_write.MemToReg)
              + ", RegWrite = " + str(MEM_WB_write.RegWrite))
        print("         LWDataValue = " + str(hex(MEM_WB_write.LWDataValue))
              + ", ALUResult = " + str(hex(MEM_WB_write.ALUResult))
              + ", WriteRegNum = " + str(MEM_WB_write.WriteRegNum))
    print()

    # MEM/WB (read by the WB stage)
    print("MEM/WB (read by the WB stage)")
    if MEM_WB_read.obj == None or MEM_WB_read.obj.obj == None or MEM_WB_read.obj.obj.instruction == 0:
        print("Control = 00000000")
    else:
        print("Control: MemToReg = " + str(MEM_WB_read.MemToReg)
              + ", RegWrite = " + str(MEM_WB_read.RegWrite))
        print("         LWDataValue = " + str(hex(MEM_WB_read.LWDataValue))
              + ", ALUResult = " + str(hex(MEM_WB_read.ALUResult))
              + ", WriteRegNum = " + str(MEM_WB_read.WriteRegNum))
    
    print("#############################################################################")
    
def Copy_write_to_read():
    # Copy from write to read in pipeline register
    global IF_ID_read, ID_EX_read, EX_MEM_read, MEM_WB_read
    IF_ID_read = copy.deepcopy(IF_ID_write)
    ID_EX_read = copy.deepcopy(ID_EX_write)
    EX_MEM_read = copy.deepcopy(EX_MEM_write)
    MEM_WB_read = copy.deepcopy(MEM_WB_write)

    ID_EX_write.clear()
    EX_MEM_write.clear()
    MEM_WB_write.clear()

class IF_ID:
    def __init__(self, instruction, IncrPC):
        self.instruction = instruction
        self.IncrPC = IncrPC

class ID_EX:
    def __init__(self):
        self.instruction = 0x0
        self.opcode = 0x0

        # Control Signals
        self.RegDst = 0
        self.ALUSrc = 0
        self.ALUOp = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Branch = 0
        self.MemToReg = 0
        self.RegWrite = 0
        self.IncrPC = 0
        self.ReadReg1Value = 0
        self.ReadReg2Value = 0
        self.SEOffset = 0
        self.WriteReg_20_16 = 0
        self.WriteReg_15_11 = 0
        self.Function = 0x0


    def disassemble(self, instruction, IncrPC):
        self.instruction = instruction
        self.IncrPC = IncrPC
        self.opcode = (instruction & mask["opcode"]) >> 26

        reg_src1 = (instruction & mask["src1"]) >> 21
        reg_src2 = (instruction & mask["src2"]) >> 16

        # OPCODE 0 means is R-format instruction (add or sub in our case)
        if self.opcode == 0:
            # Get the FUNC with the mask, there is no need to shift
            func = instruction & mask["func"]
            reg_dest = (instruction & mask["dest"]) >> 11

            self.RegDst = 1
            self.ALUSrc = 0
            self.ALUOp = 0b10
            self.MemRead = 0
            self.MemWrite = 0
            self.Branch = 0
            self.MemToReg = 0
            self.RegWrite = 1

            self.ReadReg1Value = Regs[reg_src1]
            self.ReadReg2Value = Regs[reg_src2]
            # leave the SEOffset garbage value as it is
            self.WriteReg_20_16 = reg_src2
            self.WriteReg_15_11 = reg_dest

            if func == 0x20: # Add
                self.Function = 0x20
            if func == 0x22: # Sub
                self.Function = 0x22
            
        # OPCODE 32 means is lb
        elif self.opcode == 32:
            offset = self.twos_complement(instruction & mask["offset"], 16)

            self.RegDst = 0
            self.ALUSrc = 1
            self.ALUOp = 0b00
            self.MemRead = 1
            self.MemWrite = 0
            self.Branch = 0
            self.MemToReg = 1
            self.RegWrite = 1

            self.ReadReg1Value = Regs[reg_src1]
            self.ReadReg2Value = Regs[reg_src2]
            self.SEOffset = offset
            self.WriteReg_20_16 = reg_src2
            # leave the WriteReg garbage value as it is
            # leave the Function garbage value as it is
            
        # OPCODE 43 means is sb
        elif self.opcode == 40:
            offset = self.twos_complement(instruction & mask["offset"], 16)

            # leave the RegDst garbage value as it is
            self.ALUSrc = 1
            self.ALUOp = 0b00
            self.MemRead = 0
            self.MemWrite = 1
            self.Branch = 0
            # leave the MemToReg garbage value as it is
            self.RegWrite = 0

            self.ReadReg1Value = Regs[reg_src1]
            self.ReadReg2Value = Regs[reg_src2]
            self.SEOffset = offset
            self.WriteReg_20_16 = reg_src2
            # leave the WriteReg garbage value as it is
            # leave the Function garbage value as it is
            
        else:
            return "OPCODE not found"
            
    # To handle negative offset
    def twos_complement(self, num, bits):
        most_significant_bit = num >> bits - 1
        # If most significant bit is 0, means is positive
        if most_significant_bit == 0:
            return num
        else: # negative, need to +1
            num <<= 1
            num >>= 1
            return num - 2**bits

    def clear(self):
        self.RegDst = 0
        self.ALUSrc = 0
        self.ALUOp = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Branch = 0
        self.MemToReg = 0
        self.RegWrite = 0
        self.IncrPC = 0
        self.ReadReg1Value = 0
        self.ReadReg2Value = 0
        self.SEOffset = 0
        self.WriteReg_20_16 = 0
        self.WriteReg_15_11 = 0
        self.Function = 0x0

class EX_MEM:
    def __init__(self):
        self.obj = None
        self.MemRead = 0
        self.MemWrite = 0
        self.Branch = 0
        self.MemToReg = 0
        self.RegWrite = 0
        self.CalcBTA = "X" # Not dealing with branches in this project
        self.Zero = False
        self.ALUResult = 0
        self.SWValue = 0
        self.WriteRegNum = 0

    def run(self, obj):
        self.obj = obj
        self.MemRead = obj.MemRead
        self.MemWrite = obj.MemWrite
        self.Branch = obj.Branch
        self.MemToReg = obj.MemToReg
        self.RegWrite = obj.RegWrite
        
        if self.obj.RegDst == 1: # R-Type instruction
            self.WriteRegNum = self.obj.WriteReg_15_11
        elif obj.RegDst == 0: # lb instruction
            self.WriteRegNum = self.obj.WriteReg_20_16
        else: # sb instruction
            self.WriteRegNum = "X" # WriteRegNum is garbage for store

        if self.obj.ALUOp == 0b10: #R-type instruction
            if self.obj.Function == 0x20: # Add
                self.ALUResult = self.obj.ReadReg1Value + self.obj.ReadReg2Value
                self.SWValue = self.obj.ReadReg2Value
            elif self.obj.Function == 0x22: # Sub
                self.ALUResult = self.obj.ReadReg1Value - self.obj.ReadReg2Value
                self.SWValue = self.obj.ReadReg2Value

        if self.obj.ALUOp == 0b00: #I-type instruction
            if self.obj.opcode == 32: # lb
                self.ALUResult = self.obj.ReadReg1Value + self.obj.SEOffset
                self.SWValue = self.obj.ReadReg2Value
            elif obj.opcode == 40: # sb
                self.ALUResult = self.obj.ReadReg1Value + self.obj.SEOffset
                self.SWValue = self.obj.ReadReg2Value

    def clear(self):
        self.obj = None
        self.MemRead = 0
        self.MemWrite = 0
        self.Branch = 0
        self.MemToReg = 0
        self.RegWrite = 0
        self.CalcBTA = "X" # Not dealing with branches in this project
        self.Zero = 0
        self.ALUResult = 0
        self.SWValue = 0
        self.WriteRegNum = 0       

class MEM_WB:
    def __init__(self):
        self.obj = None
        self.MemToReg = 0
        self.RegWrite = 0
        self.LWDataValue = 0
        self.ALUResult = 0
        self.WriteRegNum = 0
        self.MemWrite = 0

    def mm(self, obj):
        self.obj = obj
        self.MemToReg = obj.MemToReg
        self.RegWrite = obj.RegWrite
        self.ALUResult = obj.ALUResult
        self.WriteRegNum = obj.WriteRegNum
        self.MemWrite = obj.MemWrite

        if self.obj.MemRead == 1:
            self.LWDataValue = Main_Mem[self.ALUResult]
        elif self.obj.MemWrite == 1:
            Main_Mem[self.ALUResult] = self.obj.SWValue
        else:
            pass

    def wb(self):
        if self.MemWrite == 0 and self.MemToReg == 0: # R-Type
                Regs[int(self.WriteRegNum)] = self.ALUResult

        elif self.MemWrite == 0 and self.MemToReg == 1: # LB
                self.LWDataValue = Main_Mem[self.ALUResult]
                Regs[int(self.WriteRegNum)] = self.LWDataValue
        else: # SB dont care
            pass

    def clear(self):
        self.obj = None
        self.MemToReg = 0
        self.RegWrite = 0
        self.LWDataValue = 0
        self.ALUResult = 0
        self.WriteRegNum = 0
        self.MemWrite = 0

# Initial address
address = 0x7A000

# Initialise all the pipeline registers
IF_ID_write = IF_ID(0x0, address)
IF_ID_read = IF_ID(0x0, 0x0)
ID_EX_write = ID_EX()
ID_EX_read = ID_EX()
EX_MEM_write = EX_MEM()
EX_MEM_read = EX_MEM()
MEM_WB_write = MEM_WB()
MEM_WB_read = MEM_WB()


def main():
    global address
    instructions = [0xA1020000, 0x810AFFFC, 0x00831820, 0x01263820, 0x01224820, 0x81180000, 0x81510010, 0x00624022, 0x00000000, 0x00000000, 0x00000000, 0x00000000]

    # Printing out for Clock Cycle 0
    print("#############################################################################")
    print("############################### Clock Cycle 0 ###############################")
    Print_out_everything()

    for i in range(12):
        print("############################## Clock Cycle "+ str(i + 1) +" ##############################")
        IF_stage(instructions[i], address)
        ID_stage()
        EX_stage()
        MEM_stage()
        WB_stage()
        Print_out_everything()
        Copy_write_to_read()

        address += 4

if __name__ == '__main__':
    main()
