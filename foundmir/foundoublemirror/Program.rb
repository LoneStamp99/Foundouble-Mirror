while true do
  print "FoundMirror>> "
  user_input = gets.chomp
  if user_input.chomp == "Start"
 system("python ./data/banner.py")
    system("python ./data/main.py")
  else
    puts "Invalid input."
  end
end