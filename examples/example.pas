
var
  sum: int64;
  x: Integer; 
begin
	sum := 0;
	while not eof do
	begin
		read(x);
		sum := sum + x;
	end;
	writeln(sum);
end.
