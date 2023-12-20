#include <omp.h>

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    long long count = 0;
    // Beginning of parallel region
    #pragma omp parallel for
    for(int x=1;x<=4000;x++)
      for(int m=1;m<=4000;m++)
        for(int a=1;a<=4000;a++)
          for(int s=1;s<=4000;s++)
            if((m>838 && !s>2770 && m<1801 && !s<1351) || (!a>1716 && !m>838 && !s>2770 && m<1801 && !s<1351) || (s>3448 && s>2770 && !s<1351) || (m>1548 && !s>3448 && s>2770 && !s<1351) || (!m>1548 && !s>3448 && s>2770 && !s<1351) || (!a<2006 && m>2090 && s<1351) || (!s<537 && !x>2440 && !a<2006 && !m>2090 && s<1351) || (x<1416 && a<2006 && s<1351) || (x>2662 && !x<1416 && a<2006 && s<1351))
              count++;
    printf("%lld\n",count);
    return 0;
    // Ending of parallel region
}
