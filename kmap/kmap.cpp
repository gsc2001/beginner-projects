/******************************************************
*Writen by -Gurkirat Singh 
*******************************************************/
#include <iostream>
#include <vector>
#define pb push_back
#define f(i, l, r) for (int i = l; i <= r; i++)
using namespace std;
struct group {

	vector<pair<int, int>>index;
	pair<pair<int, int>, pair<int, int>> ans;
};

int sub(int a, int b)
{
	return ((a - b) + 4) % 4;
}
int main()
{

	cout << "\t\t\tKMAP SOLVER\n";
	cout << "\n\n\tEnter kmap :\n";
	int arr[4][4];
	int f = 1;
	f(i, 0, 3)
	{
		cout << "\t";
		f(j, 0, 3)
		{
			cin >> arr[i][j];
			if (arr[i][j] == 0)
				f = 0;
		}
	}
	cout << "\n\tYou entered\n\n";
	cout << "\t  \tC'D'\tC'D\tCD\tCD'\n";
	for (int i = 0; i < 4; i++)
	{
		if (i < 2)
		{
			cout << "\tA'";
			if (i % 2 == 0)
				cout << "B'";
			else
				cout << "B";
		}
		else
		{
			cout << "\tA";
			if (i % 2)
			{
				cout << "B'";
			}
			else
				cout << "B";
		}
		cout << "\t";
		for (int j = 0; j < 4; j++)
		{
			cout << arr[i][j] << "\t";

		}
		cout << "\n";

	}
	if (f)
	{
		cout << "F(A,B,C,D) = 1"; //whole map is 1
		return 0;
	}
	vector<group> grp;
	int done[4][4] = { 0 };

	// to choose 4x2	(hor)
	//    
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j] && arr[i][sub(j, 1)] && arr[i][sub(j, 2)] && arr[i][sub(j, 3)] && arr[sub(i, 1)][j] && arr[sub(i, 1)][sub(j, 1)] && arr[sub(i, 1)][sub(j, 2)] && arr[sub(i, 1)][sub(j, 3)])
			{
				if (!(done[i][j] && done[i][sub(j, 1)] && done[i][sub(j, 2)] && done[i][sub(j, 3)] && done[sub(i, 1)][j] && done[sub(i, 1)][sub(j, 1)] && done[sub(i, 1)][sub(j, 2)] && done[sub(i, 1)][sub(j, 3)]))
				{
					done[i][j]++;
					done[i][sub(j, 1)]++;
					done[i][sub(j, 2)]++;
					done[i][sub(j, 3)]++;
					done[sub(i, 1)][sub(j, 1)]++;
					done[sub(i, 1)][sub(j, 2)]++;
					done[sub(i, 1)][sub(j, 3)]++;
					done[sub(i, 1)][j]++;
					group g;
					if (i == 1 || i == 3)
					{
						g.ans = { {(i - 1) / 2,-1},{-1,-1} };

					}
					else
						g.ans = { {-1,i / 2},{-1,-1} };
					g.index.pb({ i,j });
					g.index.pb({ i,sub(j,1) });
					g.index.pb({ i,sub(j,2) });
					g.index.pb({ i,sub(j,3) });
					g.index.pb({ sub(i,1),j });
					g.index.pb({ sub(i,1),sub(j,1) });
					g.index.pb({ sub(i,1),sub(j,2) });
					g.index.pb({ sub(i,1),sub(j,3) });
					grp.pb(g);

				}

			}

		}
	}
	//end

	//to choose 2x4(ver)
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j] && arr[sub(i, 1)][j] && arr[sub(i, 2)][j] && arr[sub(i, 3)][j] && arr[i][sub(j, 1)] && arr[sub(i, 1)][sub(j, 1)] && arr[sub(i, 2)][sub(j, 1)] && arr[sub(i, 3)][sub(j, 1)])
			{
				if (!(done[i][j] && done[sub(i, 1)][j] && done[sub(i, 2)][j] && done[sub(i, 3)][j] && done[i][sub(j, 1)] && done[sub(i, 1)][sub(j, 1)] && done[sub(i, 2)][sub(j, 1)] && done[sub(i, 3)][sub(j, 1)]))
				{
					done[i][j]++;
					done[sub(i, 1)][j]++;
					done[sub(i, 2)][j]++;
					done[sub(i, 3)][j]++;
					done[sub(i, 1)][sub(j, 1)]++;
					done[sub(i, 2)][sub(j, 1)]++;
					done[sub(i, 3)][sub(j, 1)]++;
					done[i][sub(j, 1)]++;
					group g;
					if (j == 1 || j == 3)
					{
						g.ans = { {-1,-1},{(j - 1) / 2,-1} };

					}
					else
						g.ans = { {-1,-1},{-1,j / 2} };
					g.index.pb({ i,j });
					g.index.pb({ sub(i,1),j });
					g.index.pb({ sub(i,2),j });
					g.index.pb({ sub(i,3),j });
					g.index.pb({ i,sub(j,1) });
					g.index.pb({ sub(i,1),sub(j,1) });
					g.index.pb({ sub(i,2),sub(j,1) });
					g.index.pb({ sub(i,3),sub(j,1) });
					grp.pb(g);

				}

			}

		}
	}

	//end

	// to choose {..}
	//           {..} (square)
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j] && arr[((i - 1) + 4) % 4][j] && arr[i][((j - 1) + 4) % 4] && arr[((i - 1) + 4) % 4][((j - 1) + 4) % 4])
			{
				if (!done[i][j] || !done[((i - 1) + 4) % 4][j] || !done[i][((j - 1) + 4) % 4] || !done[((i - 1) + 4) % 4][((j - 1) + 4) % 4])
				{
					done[i][j]++;
					done[i][((j - 1) + 4) % 4]++;
					done[((i - 1) + 4) % 4][j]++;
					done[((i - 1) + 4) % 4][((j - 1) + 4) % 4]++;
					pair<pair<int, int>, pair<int, int>> a;

					if (i == 1 || i == 3)
					{
						a.first = { (i - 1) / 2, -1 };
					}
					else
					{
						a.first = { -1, i / 2 };
					}
					if (j == 1 || j == 3)
					{
						a.second = { (j - 1) / 2, -1 };
					}
					else
					{
						a.second = { -1, j / 2 };
					}
					group g;
					g.ans = a;
					g.index.pb({ i,j });
					g.index.pb({ ((i - 1) + 4) % 4,j });
					g.index.pb({ i,((j - 1) + 4) % 4 });
					g.index.pb({ ((i - 1) + 4) % 4,((j - 1) + 4) % 4 });
					grp.pb(g);
				}
			}
		}
	}
	//end

	//  to choose {....}
	for (int i = 0; i < 4; i++)
	{
		int temp = 1;
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j] == 0)
			{
				temp = 0;
				break;
			}
		}
		if (temp)
		{
			int ch = 0;
			for (int j = 0; j < 4; j++)
			{
				if (done[i][j] == 0)
				{
					ch = 1;
					break;
				}
			}
			if (ch)
			{
				group g;
				f(j, 0, 3)
					done[i][j]++;
				if (i < 2)
					g.ans = { {0, i}, {-1, -1} };
				else
				{
					g.ans = { {1, (i + 1)%2}, {-1, -1} };
				}
				g.index.pb({ i,0 });
				g.index.pb({ i,1 });
				g.index.pb({ i,2 });
				g.index.pb({ i,3 });
				grp.pb(g);
			}
		}
	}
	//end

	//to choose {
	//          .
	//          .
	//          .
	//          .
	//          }
	for (int j = 0; j < 4; j++)
	{
		int temp = 1;
		for (int i = 0; i < 4; i++)
		{
			if (arr[i][j] == 0)
			{
				temp = 0;
				break;
			}
		}
		if (temp)
		{
			int ch = 0;
			for (int i = 0; i < 4; i++)
			{
				if (done[i][j] == 0)
				{
					ch = 1;
					break;
				}
			}
			if (ch)
			{
				group g;
				f(i, 0, 3)
					done[i][j]++;
				if (j < 2)
					g.ans = { {-1, -1}, {0, j} };
				else
				{
					g.ans = { {-1, -1}, {1, (j+1)%2} };
				}
				g.index.pb({ 0,j });
				g.index.pb({ 1,j });
				g.index.pb({ 2,j });
				g.index.pb({ 3,j });
				grp.pb(g);
			}
		}
	}
	//end

	//to choose {..}

	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j] && arr[i][((j - 1) + 4) % 4])
			{
				if (!done[i][j] || !done[i][((j - 1) + 4) % 4])
				{
					done[i][j]++;
					done[i][((j - 1) + 4) % 4]++;
					group g;
					if (i < 2)
					{
						g.ans.first = { 0,i };
					}
					else
					{
						g.ans.first = { 1,(i+1)%2 };
					}
					if (j == 1 || j == 3)
					{
						g.ans.second = { (j - 1) / 2, -1 };
					}
					else
					{
						g.ans.second = { -1, j / 2 };
					}
					g.index.pb({ i,j });
					g.index.pb({ i,((j - 1) + 4) % 4 });
					grp.pb(g);
				}
			}
		}
	}
	//end

	// to select grp like { 
	//                     .
	//                     .
	//                    }
	for (int j = 0; j < 4; j++)
	{
		for (int i = 0; i < 4; i++)
		{
			if (arr[i][j] && arr[((i - 1) + 4) % 4][j])
			{
				if (!done[i][j] || !done[((i - 1) + 4) % 4][j])
				{
					done[i][j]++;
					done[((i - 1) + 4) % 4][j]++;
					group g;
					if (j < 2)
					{
						g.ans.second = { 0,j };
					}
					else
					{
						g.ans.second = { 1,(j + 1)%2 };
					}
					if (i == 1 || i == 3)
					{
						g.ans.first = { (i - 1) / 2, -1 };
					}
					else
					{
						g.ans.first = { -1, i / 2 };
					}
					g.index.pb({ i,j });
					g.index.pb({ ((i - 1) + 4) % 4,j });
					grp.pb(g);
				}
			}
		}
	}
	//end
	// to choose 1 element
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			if (arr[i][j])
			{
				if (!done[i][j])
				{
					done[i][j]++;
					group g;
					if (i < 2)
						g.ans.first = { i / 2,i % 2 };
					else
						g.ans.first = { i / 2,(i + 1) % 2 };
					if (j < 2)
					{
						g.ans.second = { 0,j % 2 };
					}
					else
						g.ans.second = { 1,(j + 1) % 2 };
					g.index.pb({ i,j });
					grp.pb(g);
				}
			}
		}
	}


	//end 


	cout << "\n\n\tF(A,B,C,D) = ";


	for (int j = 0; j < grp.size(); j++)
	{
		group g = grp[j];
		int flag = 0;
		for (auto i : g.index)
		{
			if (done[i.first][i.second] == 1)
			{
				flag = 1;
				break;
			}
		}
		if (flag)
		{
			if (g.ans.first.first == 0|| g.ans.first.first == 2)	cout << "A'";
			else if (g.ans.first.first == 1)	cout << "A";
			if (g.ans.first.second == 0|| g.ans.first.second == 2)	cout << "B'";
			else if (g.ans.first.second == 1)	cout << "B";
			if (g.ans.second.first == 0|| g.ans.second.first == 2)	cout << "C'";
			else if (g.ans.second.first == 1)	cout << "C";
			if (g.ans.second.second == 0|| g.ans.second.second == 2)	cout << "D'";
			else if (g.ans.second.second == 1)	cout << "D";
		}
		if (j != grp.size() - 1&&flag)
			cout << " + ";
	}
	cout << "\n\n\n";
	return 0;
}
// for any issues/suggestions
// contact. gurkiratsingh2001@gmail.com

