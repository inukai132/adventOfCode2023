#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    long long count = 0;
    for(int x=1;x<=4000;x++)
      for(int m=1;m<=4000;m++)
        for(int a=1;a<=4;a++)
          for(int s=1;s<=4;s++)
            if(x<1351 || x>2770 || m < 1801)
              count++;
    printf("%lld\n",count);
    return 0;
}
