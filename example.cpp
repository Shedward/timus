#include <iostream>
int main()
{
   int a;
   int sum = 0;
   while (std::cin >> a){
   	sum += a;
   }
   std::cout << sum << std::endl;
   return 0;
}