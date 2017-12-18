#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <fstream>
#include <string>

using namespace std;
int main(int argc, char* argv[]){
	string outPath = argv[1];
	ofstream randData (outPath, ios::binary);
	srand(time(0));
	randData.clear();
	int cnt = rand()%10+10; // number of function calls
	randData.write(reinterpret_cast<char*>(&cnt), sizeof(cnt));
	for(int i=0; i<cnt; ++i){
		int a = rand()%6 +1;
		randData.write(reinterpret_cast<char*>(&a), sizeof(a));
		int b = rand()%5 +1;
		randData.write(reinterpret_cast<char*>(&b), sizeof(b));
		int c = rand()%5;
		randData.write(reinterpret_cast<char*>(&c), sizeof(c));
		int step = rand()%3+1;
		randData.write(reinterpret_cast<char*>(&step), sizeof(step));
		int n = rand()%100 + 21;
		randData.write(reinterpret_cast<char*>(&n), sizeof(n));
		cout<<"a = "<<a<<"\t b = "<<b<<"\tc = "<<c<<"\tstep = "<<step<<"\tn = "<<n<<"\n";
	}
	randData.close();

}
