#include<bits/stdc++.h>
//#include<windows.h>
using namespace std;
class matrix{
	public:
		double a[50][50];
		int s;
		void transpose(matrix);
		double cof(int p,int q);
		double det();
		matrix(matrix&);
		matrix()
		{
			s=0;
		}
		void inverse(matrix);
};
matrix::matrix(matrix& m)
{

	s=m.s;
	int i,j;
	for(i=0;i<s;i++)
		for(j=0;j<s;j++)
			a[i][j]=m.a[i][j];

}

double matrix::cof(int p,int q)
{
	matrix m;
	int j;
	double cofactor;
	m.s=s-1;

	for(int i=0;i<s;i++)
	{
		for(j=0;j<s;j++)
		{

			if(i==p||j==q)
				continue;
			else
			{
				if(i>p&&j<q)
					m.a[i-1][j]=a[i][j];
				else if(i<p&&j>q)
					m.a[i][j-1]=a[i][j];
				else if(i>p&&j>q)
					m.a[i-1][j-1]=a[i][j];
				else
					m.a[i][j]=a[i][j];
			}
		}
	}
	if((p+q)%2==0)
		cofactor=m.det();
	else
		cofactor=-1*m.det();
	return cofactor;
}

double matrix::det()
{
	double d=0;
	if(s==2)
		d=a[0][0]*a[1][1]-a[1][0]*a[0][1];
	else if(s==1)
		d=a[0][0];
	else
	{
		for(int i=0;i<s;i++)
			d+=a[0][i]*cof(0,i);
	}
	return d;
}


void matrix::transpose(matrix mat)
{
	s=mat.s;

	int i,j;
	for(i=0;i<s;i++)
		for(j=0;j<s;j++)
			a[j][i]=mat.a[i][j];

}

void matrix::inverse(matrix m1)
{
	int i,j;
	s=m1.s;
	for(i=0;i<s;i++)
		for(j=0;j<s;j++)
			a[i][j]=m1.cof(j,i)/m1.det();
}
matrix org,inv;
int n;
double coficient[50][50],equality[50],sol[50];
char eqs[50][50],var[50];
void input()
{
	cout<<"\n\n********************************************************************************************************************";
	cout<<"\n********************************************EQUATION SOLVER(MATRIX METHOD)******************************************";
	cout<<"\n********************************************************************************************************************";
	cout<<"\n\n\n\n\n\t\t\tEnter no. of variables(>1): ";
	cin>>n;
	cout<<"\n\t\t\tEnter "<<n<<" equation(s) (without space,integer coficients,'RHS should be positive constant only'!!)\n";
	for(int i=0;i<n;i++)
	{
		cout<<"\n\t\t\tEnter "<<i+1<<" equation: ";
		cin>>eqs[i];
	}

}
int checkvar(char c)
{
	for(int i=0;i<n;i++)
		if(c==var[i])
		{
			return i+1;
		}
	return 0;
}
void converteqs()
{
	int i,j,l,k=0,t,u,sign,p,temp;
	for(i=0;i<n;i++)
	{

		l=strlen(eqs[i]);
		for(j=0;j<l;j++)
		{
			if(isalpha(eqs[i][j]))
			{
				t=0;
				u=j;
				u--;
				while(isalnum(eqs[i][u])&&u>0)
					u--;
				if(u==-1)
				{
					u++;
					t+=1;
				}
				else if(j==u+1&&u!=0)
					t+=1;

				if(!isalnum(eqs[i][u]))
				{


					if(eqs[i][u]=='+')
						sign=1;
					else
						sign=-1;
					u++;
				}
				else
					sign=1;

				p=j-u-1;

				for(;u<j;u++,p--)
				{
					temp=eqs[i][u]-48;
					t+=temp*pow(10,p);
				}



				if(checkvar(eqs[i][j]))
					coficient[i][checkvar(eqs[i][j])-1]+=sign*t;
				else
				{
					var[k]=eqs[i][j];
					coficient[i][k++]=sign*t;
				}
			}
			if(eqs[i][j]=='=')
			{
				u=j;
				p=l-u-2;
				u++;
				for(;u<l;u++,p--)
				{
					temp=eqs[i][u]-48;
					equality[i]+=temp*pow(10,p);
				}


			}


		}
	}

}
void insertmatrices()
{
	org.s=n;

	int j;
	for(int i=0;i<n;i++)
		for(j=0;j<n;j++)
			org.a[i][j]=coficient[i][j];

}
void process()
{
	inv.inverse(org);
	int j;
	for(int i=0;i<n;i++)
	{

		for(j=0;j<n;j++)
			sol[i]+=inv.a[i][j]*equality[j];
	}
}
void output()
{
	cout<<"\n\t\t\tSolution: \n";
	for(int i=0;i<n;i++)
		cout<<"\n\t\t\t"<<var[i]<<"="<<sol[i];

}
int main()
{
	system("clear");
	int j;
	for(int i=0;i<50;i++)
		for(j=0;j<50;j++)
			coficient[i][j]=0;
	for(int v=0;v<50;v++)
	{

		equality[v]=0;sol[v]=0;
	}

	input();
	if(n==1)
	{
		cout<<"\n\t\t\tSolution: \n\t\t\t";
		cout<<eqs[0]<<"\n";
		return 0;
	}

	converteqs();
	insertmatrices();
	if(org.det()==0)
	{
		cout<<"\n\t\t\tError!!!!";
		cout<<"\n";
		return 0;
	}
	process();
	output();
	cout<<"\n\n";
	//system("pause");
	return 0;
}
