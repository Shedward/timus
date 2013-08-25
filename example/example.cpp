/**
 * Problem: 1001 (A+B problem) 
 * Url: http://acm.timus.ru/problem.aspx?space=1&num=1002
 * Author: 86286AA (Shed)
 * Compiler: G++ (g++)
 *
 * Mem. limit: 16M
 * Time limit: 2s
 **/

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