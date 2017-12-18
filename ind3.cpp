#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <fstream>

using namespace std;
int f(int a, int b, int c,int n, int s){
    int rec = a; int i = 0;
    for(; i<n; ){
	i+=1;
        if(a>b){ 
	   rec -=a;
	   if(b>c){ rec+=3; }
	   //else  rec -=b; 
	}
	else{
	   i +=s;
	   rec+=b;
	}
	i+=1;
    }
   return i+rec;	

}


int main(int argc, char* argv[]){
	string inPath = argv[1];
	ifstream randData(inPath.c_str(), ios::binary);
	//srand(time(0));
	//randData.clear();
	int cnt = 0 ;// = rand()%10+10; // number of function calls
	randData.read(reinterpret_cast<char*>(&cnt), sizeof(cnt));
	for(int i=0; i<cnt; ++i){
		int a = 0;//rand()%6 +1;
		randData.read(reinterpret_cast<char*>(&a), sizeof(a));
		int b = 0 ; //rand()%5 +1;
		randData.read(reinterpret_cast<char*>(&b), sizeof(b));
		int c =0 ; //rand()%5;
		randData.read(reinterpret_cast<char*>(&c), sizeof(c));
		int step =0 ; // rand()%3+1;
		randData.read(reinterpret_cast<char*>(&step), sizeof(step));
		int n = 0 ; //rand()%100 + 21;
		randData.read(reinterpret_cast<char*>(&n), sizeof(n));
		cout<<"a = "<<a<<"\t b = "<<b<<"\tc = "<<c<<"\tstep = "<<step<<"\tn = "<<n<<"\t F() = "<<f(a,b,c,n,step)<<"\n";
	}
	randData.close();
	return 0;
}
