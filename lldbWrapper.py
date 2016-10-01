import sys
sys.path.append("/Library/Developer/CommandLineTools/Library/PrivateFrameworks/LLDB.framework/Resources/Python")
sys.path.append("/usr/local/lib/python2.7/site-packages/")
import time
import os
import lldb
import sys
import timeout_decorator
# from graph_tool.all import *


class lldbWrapper:
    # Global Variables
    pid = None
    file = None
    process = None
    thread = None
    target = None
    frame = None
    programGraph = None
    rootNode = None
    dbg = None
    listener = None
    timeout=0

    # user set variables
    file = "/Users/localhost/Desktop/Projects/Working/ExecTrace/Test Code/test"
    arguments = {}

    # Create debugger and target
    def __init__(self, timeout=1.5):
        global dbg, listener
        self.timeout=timeout
        dbg = lldb.SBDebugger.Create()
        dbg.SetAsync(False)
        listener = lldb.SBListener()
        errp = lldb.SBError()
        if str(errp) != "error: <NULL>":
        	print(errp)

    # Get the target
    def getTarget(self, pid = None, file=None, outputDir="/tmp/stdout.txt"):
        global dbg, errp, process, target
        globals()['pid'] = pid;
        globals()['file'] = file
        # if pid != None and file != None:
        #     while True:
        #         choice = input("File or pid? ")
        #         if choice.lower() == "file":
        #             file = input("Please enter file path: ")
        #         elif choice.lower() == "pid":
        #             pid = int(input("Please enter the pid: "))

        # set target
        errp=lldb.SBError()
        if file != None:
            target = dbg.CreateTargetWithFileAndArch(
                file, lldb.LLDB_ARCH_DEFAULT)
            process = target.Launch(
                dbg.GetListener(), None, None, None, outputDir, None,  None, 0, True, errp)
            sys.stdout.write("Chose File...")
        elif pid != None:
            target = dbg.CreateTarget(None)
            process = target.AttachToProcessWithID(listener, pid, errp)
            sys.stdout.write("Chose PID...")
        else:
            print("Error in getTarget()")
            sys.exit()
        if "No value" == str(process):
            print("PID or File doesn't exist")
            sys.exit()
        else:
            print("Connected to process or file!")
        sys.stdout.write("Pausing process...");
        self.pauseProcess()

    # pause process
    def pauseProcess(self):
        global process
        sys.stdout.write("Pausing Process...")
        process.Stop()
        if process.GetState() != lldb.eStateStopped:
            print("Failure")
            sys.exit()
        else:
            print("Success")

    # Dissasemble current frame
    def disassembleCurrentFrame(self):
        global frame
        thread = process.GetSelectedThread()
        frame = thread.GetFrameAtIndex(0)
        print(frame.Disassemble())

    # Step over
    @timeout_decorator.timeout(timeout)
    def stepOver(self):
        global frame, thread
        thread = process.GetSelectedThread()
        frame = thread.GetFrameAtIndex(0)
        thread.StepOver()
        return True

    # Step Into a function. It skips any frames that begin with an item in skipFrames.
    # For instance, dyld
    def stepInto(self, skipFrames=[]):
        global frame, thread
        thread = process.GetSelectedThread()
        frame = thread.GetFrameAtIndex(0)
        for i in range(len(skipFrames)):
            # print(skipFrames[i][:len(skipFrames[i])])
            while str(self.getCurrentInstruction().GetAddress())[:len(skipFrames[i])] == skipFrames[i]:
                self.__stepOverRaw()
                print("Skipping...")
        self.__stepIntoRaw
        return True

    #Private method to step over made so the timeout decerator may be applied
    @timeout_decorator.timeout(timeout)
    def __stepOverRaw(self):
        self.stepOver()

    #Private method to step into made so the timeout decerator may be applied
    @timeout_decorator.timeout(timeout)
    def __stepIntoRaw(self):
        thread.StepInto()

    #Checks whether an instruction is valid
    def instructionValid(self):
        instruction = self.getCurrentInstruction()
        return instruction.IsValid();

    #Checks whether an instruction branches
    def instructionBranches(self):
        instruction = self.getCurrentInstruction()
        return instruction.DoesBranch();

    # jump TODO: Implement.
    def jmp(self):
        #Just have to set pc
        setpc
        print("test")

    #Returns current address
    def getCurrentAddress(self):
        return hex(self.getCurrentInstruction().GetAddress())

    # Returns the current instruction
    def getCurrentInstruction(self):
        global frame, target
        thread = process.GetSelectedThread()
        frame = thread.GetFrameAtIndex(0)
        address = frame.GetPCAddress()
        currentInstruction = target.ReadInstructions(
            address, 1).GetInstructionAtIndex(0)
        return currentInstruction