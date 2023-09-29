/*
 * Created by SharpDevelop.
 * User: MYFAMILY
 * Date: 29 Sep 2023
 * Time: 4:51 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Diagnostics;

public class Finduplicate
{
    public static void Main(string[] args)
    {
        // Get the user input.
        string userInput = Console.ReadLine();

        // Check if the user input is "Finduplicate".
        if (userInput != "Finduplicate")
        {
            Console.WriteLine("Invalid program name.");
            return;
        }

        // Check if Ruby is installed.
        string rubyCommand = "ruby";
        if (Process.Start(rubyCommand).HasExited)
        {
            // If Ruby is not installed, call the Python file.
            string pythonCommand = "python foundmir/foundoublemirror/data/main.py";
            Process.Start(pythonCommand);
        }
        else
        {
            // If Ruby is installed, call the Ruby file.
            string rubyProgramPath = "foundmir/foundoublemirror/Program.rb";
            rubyCommand = rubyCommand + " " + rubyProgramPath;
            Process.Start(rubyCommand);
        }
    }
}
