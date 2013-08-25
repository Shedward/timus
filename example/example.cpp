#include <iostream>

int main()
{
   int a;
   long long sum = 0;
   while (std::cin >> a){
   	sum += a;
   }
   std::cout << sum;
   return 0;
}