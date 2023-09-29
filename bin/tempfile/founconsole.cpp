#include <iostream>
#include <string>
#include <cstdlib>
#include <unistd.h>

using namespace std;

int main() {
  // Get the user input.
  string userInput;
  cout << "Enter the name of the program to run: ";
  cin >> userInput;

  // Check if the user input is "Finduplicate".
  if (userInput != "Finduplicate") {
    cout << "Invalid program name." << endl;
    return 1;
  }

  // Check if Ruby is installed.
  string rubyCommand = "ruby";
  if (system(rubyCommand.c_str()) != 0) {
    // If Ruby is not installed, call the Python file.
    string pythonCommand = "python foundmir/founduplicatemirror/Program.rb/data/main.py";
    system(pythonCommand.c_str());
  } else {
    // If Ruby is installed, call the Ruby file.
    string rubyProgramPath = "foundmir/founduplicatemirror/Program.rb";
    string rubyCommand = rubyCommand + " " + rubyProgramPath;
    system(rubyCommand.c_str());
  }

  return 0;
}

