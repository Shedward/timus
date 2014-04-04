#include <stdio.h>

int main()
{
	long x;
	long long sum = 0;
	while (scanf("%d", &x) != EOF){
		sum += x;
	}
	printf("%lld", sum);
	return 0;
}
