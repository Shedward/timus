using System;

public class Sum
{
    private static void Main()
    {
    	long sum = 0;
    	string line;
        while ((line = Console.ReadLine()) != null){
        	string[] tokens = line.Split(new char[] {' ', '\t'}, StringSplitOptions.RemoveEmptyEntries);
        	foreach (string token in tokens) {
        		sum += int.Parse(token);
        	}
        }
        Console.WriteLine(sum);
    }
}
