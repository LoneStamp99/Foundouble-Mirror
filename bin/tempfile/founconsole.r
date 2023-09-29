library(ncurses)

initscr()
addstr("Welcome to my terminal!")
refresh()

while (TRUE) {
    key <- getch()
    if (key == 27) { # Escape key
        break
    } else if (key == 32) { # Space bar
        addstr(" ")
    } else if (key == 10) { # Enter key
        addstr("\n")
        addstr("Enter a command: ")
        command <- scan("", what="", nmax=1, quiet=TRUE)
        if (command == "Finduplicate") {
            # Check if the Ruby interpreter is installed
            ruby_installed <- FALSE
            if (system("command -v ruby >/dev/null 2>&1") == 0) {
                ruby_installed <- TRUE
            }

            # Run the program using Ruby or Python
            if (ruby_installed) {
                c <- system("ruby foundmir/foundoublemirror/Program.rb", intern=TRUE)
            } else {
                c <- system("python foundmir/foundoublemirror/Program.rb/data/main.py", intern=TRUE)
            }
            addstr(c)
        } else {
            addstr("Invalid command.")
        }
        refresh()
    } else {
        addstr(charToRaw(as.character(key)))
    }

    refresh()
}

endwin()