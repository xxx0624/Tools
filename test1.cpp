// INCLUDE HEADER FILES NEEDED BY YOUR PROGRAM
// SOME LIBRARY FUNCTIONALITY MAY BE RESTRICTED
// DEFINE ANY FUNCTION NEEDED
// FUNCTION SIGNATURE BEGINS, THIS FUNCTION IS REQUIRED

// FUNCTION SIGNATURE ENDS
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<algorithm>
#include<iostream>
#include<queue>
#include<math.h>
using namespace std;
typedef long long ll;
const int maxn = 105;
const int inf = 0x7fffffff;
const double pi=acos(-1.0);
const double eps = 1e-8;



struct Node
{
    int x, y;
    //x is worktime
    //y is starttime
    Node( int a = 0, int b = 0 ):
        x(a), y(b) {}
};
bool operator<( Node a, Node b )
{
    if( a.x == b.x ) return a.y > b.y;
    return a.x > b.x;
}


float waitingTimeSJF(int *requestTimes, int *durations, int n){
	int cur = 0;
	int tot = 0;
	Node no[ n ];
	int cnt_no = 0;
	no[cnt_no].x = durations[0];
	no[cnt_no].y = requestTimes[0];
	cnt_no ++;
	priority_queue<Node> q;
	q.push(no[0]);
	//tot += requestTimes[0] - cur;
	//cur = requestTimes[0];
	for( int i=1;i<n;i++ ){
		Node temp;
		temp.x = -1;
		while(q.size()>0){
			temp = q.top();
			printf("%d\n", temp.y);
			q.pop();
			break;
		}
		if(temp.x==-1){
			//cur = requestTimes[i];
			no[cnt_no].x = durations[i];
			no[cnt_no].y = requestTimes[i];
			q.push(no[cnt_no]);
			cnt_no ++;
		}
		else{
			if( cur>=temp.y ){
				tot += cur - temp.y;
				cur += temp.x;
			}
			else{
				cur = temp.x;
			}
		}
	}
	while(q.size()>0){
		Node temp = q.top();
		printf("%d\n", temp.y);
		if( cur>=temp.y ){
			tot += cur - temp.y;
			cur += temp.x;
		}
		else{
			cur = temp.x;
		}
		q.pop();
	}
	return 1.0*tot / (1.0*n);
}

int main()
{
	int a[4];
	int b[4];
	a[0] = 0;
	a[1] = 1;
	a[2] = 3;
	a[3] = 9;
	b[0] = 2;
	b[1] = 1;
	b[2] = 7;
	b[3] = 5;
	printf("%d\n", waitingTimeSJF(a, b, 4));
	printf("...\n");
	getchar();
	getchar();
	return 0;
}