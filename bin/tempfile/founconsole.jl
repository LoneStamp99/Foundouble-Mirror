using Curses
using Libc

function main()
    Curses.initscr()
    Curses.addstr("Welcome to the my terminal!")
    Curses.refresh()

    while true
        key = Curses.getch()
        if key == 27 # Exit on press of the escape key
            break
        elseif key == 32 # Space bar
            Curses.addstr(" ")
        elseif key == 10 # Enter key
            Curses.addstr("\n")
            
            # Read user input
            command = Curses.getstr()
            
            # Check if the input is "Finduplicate"
            if command == "Finduplicate"
                # Check if Ruby is installed
                if; isdefined(Main, :Libc)
                        @static Libdl.dlopen(find_executable_file("ruby"), Libdl.RTLD_LAZY)
                end
                if isdefined(Main, :Ruby)
                    # If Ruby is installed, run the program using Ruby
                    c = `ruby foundmir/foundoublemirror/Program.rb`
                    Curses.addstr(c)
                else
                    # If Ruby is not installed, run the program using Python
                    c = `python foundmir/foundoublemirror/Program.rb/data/main.py`
                    Curses.addstr(c)
                end
            else
                Curses.addstr("Invalid command.")
            end

            Curses.refresh()
        else
            Curses.addstr(string(Char(key)))
        end

        Curses.refresh()
    end

    Curses.endwin()
end

main()