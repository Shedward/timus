import java.util.*;

public class example
{
   public static void main(String[] args)
   {
   		int x;
   		long sum = 0;
		Scanner in = new Scanner(System.in);

		try 
		{
			while (true)
			{
				x = in.nextInt();
				sum += x;
			}
		} catch (NoSuchElementException e) {
			System.out.println(sum);
		}
   }
}