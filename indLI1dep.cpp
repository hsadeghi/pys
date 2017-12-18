int func(int a, int b, int c, int s){
  int sum=0, inv = a+b;
  for(int i=0; i<a; a+=s)
     if(a>b) {sum+=a; inv -=b;}
     else {sum+=b; inv -=a;}

  return sum;
}

//int main(){
  

