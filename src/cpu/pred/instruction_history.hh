/**
 * instruction_history.hh defines a class that stores the n most recent instruction in a queue of size n
 * the output of the queue can be written to a history file at any point.
 * */

#ifndef __INSTRUCTION_HISTORY_HH__
#define __INSTRUCTION_HISTORY_HH__

#include <queue>
#include <deque>
#include <string>
#include <sstream>
#include <fstream>
#include <iterator>
#include <iostream>

// Stores the outcome of a branch, its sequence number and the executed instructions
struct BranchOutcome {
  public:
    BranchOutcome(bool tkn, int seq, std::deque<std::string> insts): taken(tkn), seq_num(seq), instructions(insts) {};
    bool taken;
    int seq_num;
    std::deque<std::string> instructions;
};

// Records the lkast QUEUE_SIZE instructions that have been processed.
template <unsigned int QUEUE_SIZE>
class InstructionHistory {
  public:
    // Default Constructor
    InstructionHistory() {} 
    void writeHistory(BranchOutcome branch);
    void addInstruction(std::string instruction);
    void saveBranchOutcome(bool taken, int seq_num);
    void updateBranchOutcome(int seq_num, bool taken);
    int  getHistorySize();
    std::string getInstructionAt(int position);
  private:
    std::deque<std::string> history;
    std::vector<BranchOutcome> branches;
};


// Copies the contents of the queue into a file for recording.
template <unsigned int QUEUE_SIZE>
void InstructionHistory<QUEUE_SIZE>::writeHistory(BranchOutcome branch)
{
  std::ostringstream oss;
  oss << branch.taken;
  for (auto& inst: branch.instructions)
  {
    oss << " ";
    oss << inst;
  }
  
  // Write the history to file
  std::ofstream file("branch_history.txt", std::ios_base::app);
  //file.open("branch_history.txt", std::ios_base::app);
  file << oss.str() << std::endl;
  //std::cout << oss.str() << std::endl;

  return;
}

// Adds a new instruction ot the queue and ensures that the queue size is maintained.
template <unsigned int QUEUE_SIZE>
void InstructionHistory<QUEUE_SIZE>::addInstruction(std::string instruction)
{
  // Check the current size to see if the oldest instruction must be removed
  if (history.size() >= QUEUE_SIZE)
      history.pop_front();

  // Add the new instruction to the back of the queue
  history.emplace_back(instruction);
  
  return;
}

// Saves the outcome of a branch along with the sequence number and the current instruction history.
template <unsigned int QUEUE_SIZE>
void InstructionHistory<QUEUE_SIZE>::saveBranchOutcome(bool taken, int seq_num)
{
  branches.push_back(BranchOutcome(taken, seq_num, history));
  
  return;
}

// Once the actual outcome of a branch is known, it must be updated.
// Also adds the history to the results file.
template <unsigned int QUEUE_SIZE>
void InstructionHistory<QUEUE_SIZE>::updateBranchOutcome(int seq_num, bool taken)
{
  bool found = false;
  std::vector<BranchOutcome>::iterator it = branches.begin();

  while (!found && it != branches.end())
  {
      if ((*it).seq_num == seq_num)
      {
        writeHistory(*it);
        (*it).taken = taken;
        found = true;
      }
      it++;
  }

  return;
}

template <unsigned int QUEUE_SIZE>
int InstructionHistory<QUEUE_SIZE>::getHistorySize()
{
    return history.size();
}

template <unsigned int QUEUE_SIZE>
std::string InstructionHistory<QUEUE_SIZE>::getInstructionAt(int position)
{
    return history.at(position);
}
#endif
