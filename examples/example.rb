
sum = 0
while string = gets do
   string.split().each do |token|
      sum += token.to_i
   end
end
puts sum